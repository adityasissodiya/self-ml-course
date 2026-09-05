"""Check local Markdown links and external URLs; write LINK_REPORT.md."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

try:
    import requests
except ImportError:  # The standard-library fallback keeps a fresh clone runnable.
    requests = None

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s<>\])}]+")
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".venv", "node_modules"}


def markdown_files():
    return [p for p in ROOT.rglob("*.md") if p.name != "LINK_REPORT.md" and not any(part in SKIP_DIRS for part in p.parts)]


def external_urls(files):
    found = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in URL_RE.finditer(text):
            url = match.group(0).rstrip(".,;:'\"`")
            if urlsplit(url).hostname in {"localhost", "127.0.0.1"}:
                continue
            line = text.count("\n", 0, match.start()) + 1
            context = text.splitlines()[line - 1]
            entry = found.setdefault(url, {"refs": [], "gated": False, "institutional": False, "unverified": False})
            entry["refs"].append(f"{path.relative_to(ROOT).as_posix()}:{line}")
            entry["gated"] = entry["gated"] or "GATED" in context
            entry["institutional"] = entry["institutional"] or "INST" in context
            entry["unverified"] = entry["unverified"] or "UNVERIFIED" in context
    return found


def local_links(files):
    rows = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1).strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = unquote(target.split("#", 1)[0])
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            rows.append((path.relative_to(ROOT).as_posix(), target, resolved.exists()))
    return rows


def check_one(item):
    url, meta = item
    headers = {"User-Agent": "agentic-ac-course-link-checker/1.0"}
    status, final, error = "—", "", ""
    try:
        if requests is not None:
            response = requests.head(url, allow_redirects=True, timeout=15, headers=headers)
            if response.status_code in {403, 405, 429} or response.status_code >= 500:
                response = requests.get(url, allow_redirects=True, timeout=20, headers=headers, stream=True)
            status, final = response.status_code, response.url
            response.close()
        else:
            try:
                response = urlopen(Request(url, method="HEAD", headers=headers), timeout=15)
            except HTTPError as exc:
                if exc.code not in {403, 405, 429} and exc.code < 500:
                    raise
                response = urlopen(Request(url, method="GET", headers=headers), timeout=20)
            status, final = response.status, response.geturl()
            response.close()
    except HTTPError as exc:
        status, final, error = exc.code, exc.geturl(), str(exc)
    except (URLError, OSError, TimeoutError) as exc:
        error = str(exc)
    except Exception as exc:
        if requests is not None and isinstance(exc, requests.RequestException):
            error = str(exc)
        else:
            error = str(exc)
    if meta["gated"]:
        verdict = "GATED (landing reachable)" if isinstance(status, int) and status < 400 else "GATED (expected)"
    elif meta["institutional"] and status in {401, 403}:
        verdict = "INST (expected)"
    elif meta["unverified"] and (status == "—" or (isinstance(status, int) and status >= 400)):
        verdict = "UNVERIFIED (flagged)"
    elif isinstance(status, int) and status < 400:
        verdict = "OK"
    else:
        verdict = "FAIL"
    return url, status, verdict, final, error.replace("\n", " ")[:180]


def main():
    files = markdown_files()
    urls = external_urls(files)
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(check_one, item) for item in urls.items()]
        checked = sorted((future.result() for future in as_completed(futures)), key=lambda row: row[0])
    locals_ = local_links(files)
    bad_local = [row for row in locals_ if not row[2]]
    bad_external = [row for row in checked if row[2] == "FAIL"]
    gated = [row for row in checked if row[2].startswith(("GATED", "INST"))]
    unverified = [row for row in checked if row[2].startswith("UNVERIFIED")]
    lines = [
        "# Link report", "", f"Last verified: {date.today().isoformat()}", "",
        f"Checked {len(urls)} unique external URLs and {len(locals_)} relative links.", "",
        f"- External OK: {len(checked) - len(bad_external) - len(gated) - len(unverified)}",
        f"- External failed/unreachable: {len(bad_external)}",
        f"- Gated: {len(gated)}",
        f"- Explicitly unverified: {len(unverified)}",
        f"- Broken relative links: {len(bad_local)}", "",
        "## External links", "",
        "| URL | HTTP | Verdict | Referenced from | Note |", "|---|---:|---|---|---|",
    ]
    for url, status, verdict, final, note in checked:
        refs = ", ".join(urls[url]["refs"][:4])
        redirect = f"Redirects to {final}" if final and final.rstrip("/") != url.rstrip("/") else note
        lines.append(f"| {url} | {status} | {verdict} | {refs} | {redirect} |")
    lines += ["", "## Relative links", "", "| Source | Target | Verdict |", "|---|---|---|"]
    for source, target, exists in sorted(locals_):
        lines.append(f"| {source} | `{target}` | {'OK' if exists else 'FAIL'} |")
    (ROOT / "LINK_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Link report: {len(bad_external)} external failures, {len(gated)} gated, {len(bad_local)} broken relative links")
    if bad_local:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
