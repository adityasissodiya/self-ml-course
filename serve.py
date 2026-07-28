#!/usr/bin/env python3
"""One-command launcher for the course: `python tools/course.py serve`.

Why this exists: the quizzes are static pages that `fetch("questions.json")`.
Opening them as `file://` makes the browser block that fetch, so the page hangs
on "Loading...". Serving the repo over HTTP fixes it. This script:

  1. serves the whole repo on http://127.0.0.1:<port> (one server covers every
     quiz - their relative fetches just work);
  2. opens a hub page that links every concept's quiz and exercise, and shows
     which modules you have already submitted;
  3. accepts the shard line back via POST /save-key, verifies the answers are
     correct locally, writes progress/NN.key, and rebuilds the course PDF - all
     on your machine. No git push, no server.

Everything happens locally. Answer-checking uses the answer key in
ci/answers.json (if present) or the bundled ci/answers.example.json. The PDF is
rebuilt with latexmk/pdflatex when TeX Live is installed; if it is not, your
progress is still recorded and you are told the PDF step was skipped.

Standard library only - no pip install, matching the rest of the repo.

    python serve.py                  # serve + open the hub in your browser
    python serve.py --port 9000     # pick a port
    python serve.py --no-browser    # don't auto-open a browser
"""
import argparse
import datetime
import hashlib
import html
import hmac
import http.server
import importlib.util
import os
import json
import pathlib
import re
import shutil
import socket
import socketserver
import subprocess
import sys
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "course.manifest.json").read_text())
PALETTE = dict(bg="#0f1117", fg="#e6e6e6", accent="#7c5cff", ok="#3ddc84",
               panel="#161922", border="#2a2f3a", muted="#9aa0aa")

# A key looks like "handle:DLX-03-0123456789AB". We need the handle, the
# two-digit module id, and the 12-char shard core to verify it locally.
SHARD_RE = re.compile(
    r"^(?P<handle>[a-z0-9_-]+):(?P<prefix>[A-Za-z0-9]+)-(?P<mod>\d{2})-(?P<core>[A-Za-z0-9]{12})$")

CI_DIR = ROOT / "ci"
TEX_DIR = ROOT / "tex"


def answer_key():
    """Local answer key: ci/answers.json if present, else the bundled example."""
    for name in ("answers.json", "answers.example.json"):
        p = CI_DIR / name
        if p.exists():
            try:
                return json.loads(p.read_text())
            except Exception:
                pass
    return {}


def in_container():
    """Best-effort detection for Docker/devcontainer defaults."""
    return (
        pathlib.Path("/.dockerenv").exists()
        or os.environ.get("REMOTE_CONTAINERS") == "true"
        or bool(os.environ.get("CODESPACES"))
        or bool(os.environ.get("DEVCONTAINER"))
    )


def has_module(name):
    return importlib.util.find_spec(name) is not None


def environment_checks():
    """Return small diagnostic checks for the local course environment."""
    latex = shutil.which("latexmk") or shutil.which("pdflatex")
    checks = [
        ("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0]),
        ("numpy", has_module("numpy"), "coding exercises"),
        ("pytest", has_module("pytest"), "project and exercise tests"),
        ("TeX", bool(latex), latex or "PDF rebuilds skipped"),
        ("git", bool(shutil.which("git")), "instructor CI pull"),
        ("curl", bool(shutil.which("curl")), "instructor publish"),
    ]
    return checks


def environment_html():
    items = []
    for label, ok, detail in environment_checks():
        cls = "good" if ok else "bad"
        mark = "OK" if ok else "Missing"
        items.append(
            f'<div class="envitem"><span class="pill {cls}">{mark}</span>'
            f'<strong>{html.escape(label)}</strong>'
            f'<small>{html.escape(str(detail))}</small></div>'
        )
    return "".join(items)


def module_salt(module_id):
    """The HMAC salt for a module, read from its quiz/questions.json."""
    for p in ROOT.glob(f"concepts/{module_id}-*/quiz/questions.json"):
        return json.loads(p.read_text())["salt"]
    raise FileNotFoundError(f"no quiz for module {module_id}")


def expected_core(salt, handle, module_id, canonical):
    """Recompute the 12-char shard core the quiz page would have produced."""
    msg = f"{handle}|{module_id}|{canonical}".encode()
    return hmac.new(salt.encode(), msg, hashlib.sha256).hexdigest()[:12].upper()


def verify(handle, module_id, core):
    """(ok, reason) - does this shard encode the correct answers for the module?"""
    answers = answer_key()
    if module_id not in answers:
        return False, f"No answer key for module {module_id} yet (is its quiz authored?)."
    try:
        salt = module_salt(module_id)
    except FileNotFoundError as e:
        return False, str(e)
    ok = hmac.compare_digest(core.upper(), expected_core(salt, handle, module_id, answers[module_id]))
    if ok:
        return True, None
    return False, "Those answers are not all correct (or the handle does not match the shard). Re-take the quiz."


def rebuild_progress_tex():
    """Regenerate tex/progress.tex from every valid progress/*.key. Returns count."""
    answers = answer_key()
    today = datetime.date.today().isoformat()
    lines = ["% GENERATED locally by serve.py - do not edit, do not commit.", ""]
    done = 0
    for kf in sorted((ROOT / "progress").glob("*.key")):
        try:
            m = SHARD_RE.match(kf.read_text().strip())
            if not m or m["mod"] != kf.stem or m["mod"] not in answers:
                continue
            salt = module_salt(m["mod"])
            if hmac.compare_digest(m["core"].upper(),
                                   expected_core(salt, m["handle"], m["mod"], answers[m["mod"]])):
                lines.append(f"\\moduledone{{{m['handle']}}}{{{m['mod']}}}{{{today}}}")
                done += 1
        except Exception:
            continue
    (TEX_DIR / "progress.tex").write_text("\n".join(lines) + "\n")
    return done


def rebuild_pdf():
    """Rebuild tex/main.pdf if TeX is installed. Returns (built, reason)."""
    if shutil.which("latexmk"):
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        passes = 1
    elif shutil.which("pdflatex"):
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        passes = 2  # pdflatex needs a second pass to resolve the ToC / badges
    else:
        return False, "TeX Live not found - progress saved, but the PDF was not rebuilt."

    # A fatal LaTeX error makes latexmk delete the output, which would wipe the
    # last good PDF. Keep a backup and restore it if the build fails.
    pdf = TEX_DIR / "main.pdf"
    backup = TEX_DIR / "main.pdf.bak"
    if pdf.exists():
        shutil.copy2(pdf, backup)

    def _restore():
        if backup.exists() and not pdf.exists():
            shutil.copy2(backup, pdf)

    try:
        for _ in range(passes):
            r = subprocess.run(cmd, cwd=TEX_DIR, capture_output=True, timeout=180)
            if r.returncode != 0:
                _restore()
                return False, "LaTeX reported an error - progress saved; see tex/main.log."
        return True, None
    except subprocess.TimeoutExpired:
        _restore()
        return False, "LaTeX timed out - progress saved, but the PDF was not rebuilt."
    finally:
        backup.unlink(missing_ok=True)


def run_p0_tests():
    """Run the one project smoke test that should pass on a fresh clone."""
    if not has_module("pytest"):
        return False, "pytest is not installed. Run `python -m pip install -r requirements.txt`."
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "project/tests/test_p0_data.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=90,
        )
    except subprocess.TimeoutExpired:
        return False, "P0 smoke test timed out."

    output = (result.stdout + "\n" + result.stderr).strip()
    if len(output) > 5000:
        output = output[-5000:]
    return result.returncode == 0, output or "No output."


def submitted_modules():
    """Set of module ids that already have a non-empty progress/NN.key."""
    out = set()
    for p in (ROOT / "progress").glob("*.key"):
        if p.stat().st_size > 0:
            out.add(p.stem)
    return out


def hub_html():
    done = submitted_modules()
    rows = []
    for c in MANIFEST["concepts"]:
        cid, slug = c["id"], c["slug"]
        folder = f"concepts/{cid}-{slug}"
        title = c["title"]
        prereq = ", ".join(c.get("prereq", [])) or "&mdash;"
        miles = ", ".join(c.get("milestones", [])) or "&mdash;"

        if c.get("quiz"):
            badge = ('<span class="ok">&#10003; submitted</span>' if cid in done
                     else '<span class="todo">not yet</span>')
            quiz = f'<a class="btn" href="/{folder}/quiz/index.html" target="_blank">Take quiz &#8599;</a>'
        else:
            badge, quiz = '<span class="muted">no quiz</span>', '<span class="muted">&mdash;</span>'

        if c.get("exercise"):
            ex = (f'<code>python tools/course.py test-exercise {folder}/exercise</code><br>'
                  f'<span class="muted">runs pytest when installed; otherwise uses the fallback test runner</span>')
        else:
            ex = '<span class="muted">&mdash;</span>'

        rows.append(f"""
      <tr>
        <td class="id">{cid}</td>
        <td><div class="ttl">{title}</div>
            <div class="meta">prereq {prereq} &middot; milestones {miles}</div></td>
        <td>{quiz}<div class="status">{badge}</div></td>
        <td class="ex">{ex}</td>
      </tr>""")

    course = MANIFEST["course"]
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{course['title']}</title>
<style>
  :root {{ --bg:{PALETTE['bg']}; --fg:{PALETTE['fg']}; --accent:{PALETTE['accent']};
          --ok:{PALETTE['ok']}; --panel:{PALETTE['panel']}; --border:{PALETTE['border']};
          --muted:{PALETTE['muted']}; }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--fg); margin: 0;
         font: 16px/1.5 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
  main {{ max-width: 980px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
  h1 {{ font-size: 1.5rem; margin: 0 0 .25rem; }}
  .sub {{ color: var(--muted); margin: 0 0 1.75rem; }}
  .card {{ background: var(--panel); border: 1px solid var(--border);
          border-radius: 10px; padding: 1rem 1.1rem; margin-bottom: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; padding: .7rem .6rem; border-bottom: 1px solid var(--border);
           vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 600; font-size: .82rem; text-transform: uppercase;
       letter-spacing: .04em; }}
  td.id {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
  .ttl {{ font-weight: 600; }}
  .meta {{ color: var(--muted); font-size: .82rem; }}
  .btn {{ display: inline-block; background: var(--accent); color: #fff; text-decoration: none;
         padding: .4rem .7rem; border-radius: 6px; font-size: .9rem; white-space: nowrap; }}
  .btn:hover {{ filter: brightness(1.1); }}
  .status {{ margin-top: .35rem; font-size: .82rem; }}
  .ok {{ color: var(--ok); }}
  .todo {{ color: #e0b341; }}
  .muted {{ color: var(--muted); }}
  .envgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
             gap: .6rem; margin-top: .9rem; }}
  .envitem {{ background: #0c0e14; border: 1px solid var(--border); border-radius: 7px;
             padding: .55rem .65rem; min-height: 4.3rem; }}
  .envitem strong {{ display: block; margin-top: .35rem; }}
  .envitem small {{ display: block; color: var(--muted); font-size: .78rem; overflow-wrap: anywhere; }}
  .pill {{ display: inline-block; border-radius: 999px; padding: .08rem .45rem;
          font-size: .7rem; font-weight: 700; }}
  .pill.good {{ background: rgba(61,220,132,.14); color: var(--ok); }}
  .pill.bad {{ background: rgba(255,107,107,.14); color: #ff6b6b; }}
  .actions {{ display: flex; flex-wrap: wrap; gap: .6rem; margin-top: .75rem; }}
  pre.output {{ white-space: pre-wrap; overflow: auto; max-height: 18rem; background: #0c0e14;
               border: 1px solid var(--border); border-radius: 7px; padding: .75rem; }}
  td.ex code {{ background: #0c0e14; border: 1px solid var(--border); border-radius: 5px;
               padding: .1rem .35rem; font-size: .8rem; }}
  input {{ width: 100%; padding: .55rem; background: #0c0e14; color: var(--fg);
          border: 1px solid var(--border); border-radius: 6px; font-size: 1rem; }}
  button {{ background: var(--accent); color: #fff; border: 0; border-radius: 6px;
           padding: .55rem 1rem; font-size: 1rem; cursor: pointer; margin-top: .6rem; }}
  #msg {{ margin-top: .6rem; min-height: 1.2em; }}
  code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
</style></head>
<body><main>
  <h1>{course['title']}</h1>
  <p class="sub">Local course hub &middot; served from this repo. Take a quiz, then
     paste the shard line below to record it.</p>

  <div class="card">
    <strong>Environment</strong>
    <p class="sub" style="margin:.4rem 0 0">
      Recommended command: <code>python tools/course.py serve</code>. On Windows,
      open the repo in the supplied VS Code devcontainer for the full Python + TeX setup.
    </p>
    <div class="envgrid">{environment_html()}</div>
    <div class="actions">
      <button id="rebuild" type="button">Rebuild PDF</button>
      <button id="smoke" type="button">Run P0 smoke test</button>
    </div>
    <div id="action-msg"></div>
  </div>

  <div class="card">
    <strong>Submit a shard</strong>
    <p class="sub" style="margin:.4rem 0 .8rem">
      After a quiz gives you a <code>handle:{course.get('key_prefix','DLX')}-NN-XXXX</code>
      line, paste it here. It is checked locally; if the answers are correct it is
      saved to <code>progress/NN.key</code> and your course PDF
      (<code>tex/main.pdf</code>) is rebuilt - all on your machine, no push.
    </p>
    <input id="shard" placeholder="e.g. alice:{course.get('key_prefix','DLX')}-03-0123456789AB"
           autocomplete="off" spellcheck="false">
    <button id="save" type="button">Save to progress/NN.key</button>
    <div id="msg"></div>
  </div>

  <div class="card" style="padding:0">
  <table>
    <thead><tr><th>#</th><th>Concept</th><th>Quiz</th><th>Exercise</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  </div>

<script>
const msg = document.getElementById("msg");
const actionMsg = document.getElementById("action-msg");

async function postAction(path, pending) {{
  actionMsg.textContent = pending;
  actionMsg.className = "";
  try {{
    const r = await fetch(path, {{ method: "POST" }});
    const data = await r.json();
    const output = data.output ? '<pre class="output">' + escapeHtml(data.output) + '</pre>' : '';
    if (r.ok) {{
      actionMsg.innerHTML = '<span style="color:var(--ok)">&#10003; ' +
        escapeHtml(data.message || 'Done') + '</span>' + output;
    }} else {{
      actionMsg.innerHTML = '<span style="color:#ff6b6b">' +
        escapeHtml(data.error || 'Command failed') + '</span>' + output;
    }}
  }} catch (e) {{
    actionMsg.innerHTML = '<span style="color:#ff6b6b">Server unreachable. Is serve.py running?</span>';
  }}
}}

function escapeHtml(s) {{
  return String(s).replace(/[&<>"']/g, c => ({{
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }}[c]));
}}

document.getElementById("rebuild").addEventListener("click", () =>
  postAction("/rebuild-pdf", "Rebuilding PDF..."));
document.getElementById("smoke").addEventListener("click", () =>
  postAction("/run-p0-tests", "Running P0 smoke test..."));

document.getElementById("save").addEventListener("click", async () => {{
  const line = document.getElementById("shard").value.trim();
  msg.textContent = "Saving...";
  msg.className = "";
  try {{
    const r = await fetch("/save-key", {{
      method: "POST", headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ line }})
    }});
    const data = await r.json();
    if (r.ok) {{
      const pdf = data.pdf_built
        ? 'PDF rebuilt (tex/main.pdf).'
        : (data.pdf_note || 'Progress saved.');
      msg.innerHTML = '<span style="color:var(--ok)">&#10003; Verified &mdash; ' +
        data.completed + '/13 quiz modules done. ' + pdf + '</span>';
      setTimeout(() => location.reload(), 1200);
    }} else {{
      msg.innerHTML = '<span style="color:#ff6b6b">' + (data.error || "Could not save") + '</span>';
    }}
  }} catch (e) {{
    msg.innerHTML = '<span style="color:#ff6b6b">Server unreachable. Is serve.py running?</span>';
  }}
}});
</script>
</main></body></html>"""


class ThreadingHTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, fmt, *args):  # quieter console
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = hub_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/rebuild-pdf":
            completed = rebuild_progress_tex()
            built, reason = rebuild_pdf()
            if built:
                return self._json(200, {
                    "ok": True,
                    "message": f"PDF rebuilt at tex/main.pdf ({completed}/13 quiz modules complete).",
                })
            return self._json(500, {"error": reason})

        if self.path == "/run-p0-tests":
            ok, output = run_p0_tests()
            if ok:
                return self._json(200, {"ok": True, "message": "P0 smoke test passed.", "output": output})
            return self._json(500, {"error": "P0 smoke test failed.", "output": output})

        if self.path != "/save-key":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            line = str(payload.get("line", "")).strip()
        except Exception:
            return self._json(400, {"error": "Bad request"})

        m = SHARD_RE.match(line)
        if not m:
            return self._json(400, {"error": "That does not look like a handle:PREFIX-NN-XXXX line."})
        module_id = m["mod"]
        if not list(ROOT.glob(f"concepts/{module_id}-*")):
            return self._json(400, {"error": f"No concept {module_id} in this repo."})

        # Verify the answers locally before recording anything.
        ok, reason = verify(m["handle"], module_id, m["core"])
        if not ok:
            return self._json(400, {"error": reason})

        (ROOT / "progress" / f"{module_id}.key").write_text(line + "\n", encoding="utf-8")

        # Trigger the local build: regenerate progress, then rebuild the PDF.
        completed = rebuild_progress_tex()
        built, build_note = rebuild_pdf()
        return self._json(200, {
            "ok": True,
            "path": f"progress/{module_id}.key",
            "completed": completed,
            "pdf_built": built,
            "pdf_note": build_note,
        })

    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def free_port(preferred, host):
    for port in [preferred] + list(range(preferred + 1, preferred + 50)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return port
            except OSError:
                pass
    return preferred


def main():
    ap = argparse.ArgumentParser(description="Serve the course locally.")
    default_host = os.environ.get("DLGPT_HOST") or ("0.0.0.0" if in_container() else "127.0.0.1")
    ap.add_argument("--host", default=default_host)
    ap.add_argument("--port", type=int, default=8000)
    browser = ap.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="browser", action="store_true")
    browser.add_argument("--no-browser", dest="browser", action="store_false")
    ap.set_defaults(browser=None)
    args = ap.parse_args()

    port = free_port(args.port, args.host)
    display_host = "127.0.0.1" if args.host in ("0.0.0.0", "") else args.host
    url = f"http://{display_host}:{port}/"
    open_browser = (not in_container()) if args.browser is None else args.browser
    with ThreadingHTTPServer((args.host, port), Handler) as httpd:
        httpd.daemon_threads = True
        print(f"\n  Course hub:  {url}")
        print(f"  Bound to:    {args.host}:{port}")
        print(f"  Serving:     {ROOT}")
        print("  Stop:        Ctrl-C\n")
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Stopped.\n")


if __name__ == "__main__":
    main()
