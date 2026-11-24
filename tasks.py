#!/usr/bin/env python3
"""Course task runner: experiments, slides, and preparation evidence.

    python tasks.py test                         unit tests for the simulator
    python tasks.py run [w1|w2|w3|all]           run experiments, regenerate results/
    python tasks.py slides [wN|all] [--final | --notes | --handout]
    python tasks.py activity [wN|all]            build the participant activity sheets
    python tasks.py build [wN|all]               test, run, dossier, slides, activity
    python tasks.py note R1.7                    start a reading note from the template
    python tasks.py log w1 1.5 reading "Read RFC 8693 sections 1-4" [--output notes/R1.7.md]
    python tasks.py rehearsal w1 40 "two PhD peers" "what they said" "what I changed"
    python tasks.py dossier [wN|all]             preparation evidence, per workshop
    python tasks.py links                        check every link in the Markdown files
    python tasks.py clean                        remove build/ and every results/ folder

Only the Python standard library is needed, plus TeX Live (latexmk, pdflatex, biber)
for the slides.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSHOPS = ROOT / "workshops"
BUILD = ROOT / "build"
ACTIVITIES = ("reading", "notes", "simulation", "slides", "rehearsal", "delivery", "follow-up")

READING_ROW = re.compile(r"^\|\s*(R\d\.\d+)\s*\|\s*\[(LB|BG)\]\s*(.+?)\s*\|\s*\[([ABC])\]\s*\|\s*([A-Z-]+)\s*\|"
                         r"\s*(.+?)\s*\|\s*(.*?)\s*\|\s*$")
OUTCOME_ROW = re.compile(r"^\|\s*([KSJ]\d\.\d)\s*\|")
LOG_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([\d.]+)\s*\|\s*([\w-]+)\s*\|")
REHEARSAL_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)\s*\|")

NOTE_TEMPLATE = """# {id} — {title}

Tier: [{tier}] · Access: {access} · Link: {link}
Read on: YYYY-MM-DD · Time spent: ? h · Logged with `python tasks.py log`

## What it claims or specifies

TODO: the two or three claims I will rely on, with section or page numbers.

## Evidence and limits

TODO: peer-reviewed, preprint, normative standard, or grey literature? What does it not cover?

## What it says about delegated authority

TODO: principal, actor, attenuation, revocation, provenance, cross-organization trust.

## Where it appears in the workshop

TODO: slide, demo, or discussion, and the exact claim made there.

## Questions to raise

TODO
"""


# --- helpers ---------------------------------------------------------------------
def workshop_dirs(selector: str | None = "all") -> list[Path]:
    dirs = sorted(p for p in WORKSHOPS.glob("w[0-9]-*") if p.is_dir())
    if selector in (None, "all"):
        return dirs
    found = [d for d in dirs if d.name.split("-", 1)[0] == selector]
    if not found:
        sys.exit(f"unknown workshop {selector!r}; use one of {[d.name[:2] for d in dirs]} or 'all'")
    return found


def short(w: Path) -> str:
    return w.name.split("-", 1)[0]


def py_env() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def need(tool: str) -> None:
    if not shutil.which(tool):
        sys.exit(f"{tool} not found. Install TeX Live with latexmk and biber to build slides.")


def read_workshop(w: Path) -> dict:
    text = (w / "README.md").read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    budget = re.search(r"\|\s*\*\*Hours budget\*\*\s*\|\s*(\d+)", text)
    readings = []
    for line in text.splitlines():
        m = READING_ROW.match(line)
        if m:
            rid, role, title_, tier, access, link, use = m.groups()
            readings.append({"id": rid, "core": role == "LB", "title": title_, "tier": tier,
                             "access": access, "link": link, "use": use})
    outcomes = [m.group(1) for line in text.splitlines() if (m := OUTCOME_ROW.match(line))]
    return {"title": title, "budget": int(budget.group(1)) if budget else None,
            "readings": readings, "outcomes": outcomes}


def section_rows(path: Path, heading: str, pattern: re.Pattern) -> list[re.Match]:
    if not path.exists():
        return []
    rows, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == heading
        elif inside and (m := pattern.match(line)):
            rows.append(m)
    return rows


def append_row(path: Path, heading: str, cells: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        sys.exit(f"{path} has no '{heading}' section")
    sep = next(i for i in range(start, len(lines)) if lines[i].startswith("|---"))
    end = sep + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    clean = [c.replace("|", "/").replace("\n", " ").strip() for c in cells]
    lines.insert(end, "| " + " | ".join(clean) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def latexmk(tex: Path, outdir: Path, jobname: str, pretex: str | None = None, biber: bool = True) -> Path:
    need("latexmk")
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={outdir}",
           f"-jobname={jobname}"]
    if pretex:
        cmd.append(f"-usepretex={pretex}")
    if not biber:
        cmd.append("-bibtex-")
    cmd.append(tex.name)
    log = outdir / f"{jobname}.latexmk.txt"
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.call(cmd, cwd=tex.parent, stdout=fh, stderr=subprocess.STDOUT)
    if rc:
        tail = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-25:])
        sys.exit(f"LaTeX build failed for {tex.name} ({jobname}). Last lines of {log}:\n{tail}")
    return outdir / f"{jobname}.pdf"


def prep_markers(tex: Path) -> list[str]:
    return [line.strip() for line in tex.read_text(encoding="utf-8").splitlines()
            if r"\prep{" in line and not line.lstrip().startswith("%")]


# --- commands -----------------------------------------------------------------------
def cmd_test(_args) -> None:
    rc = subprocess.call([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                         cwd=ROOT, env=py_env())
    if rc:
        sys.exit(rc)


def cmd_run(args) -> None:
    for w in workshop_dirs(args.workshop):
        for script in sorted((w / "experiments").glob("e[0-9]*_*.py")):
            print(f"\n=== {w.name}/experiments/{script.name}", flush=True)
            rc = subprocess.call([sys.executable, script.name], cwd=script.parent, env=py_env())
            if rc:
                sys.exit(f"{script.relative_to(ROOT)} failed (exit {rc})")


def cmd_slides(args) -> None:
    variant = "final" if args.final else "notes" if args.notes else "handout" if args.handout else "draft"
    pretex = {"draft": None, "final": r"\def\finalbuild{}", "notes": r"\def\withnotes{}",
              "handout": r"\PassOptionsToClass{handout}{beamer}\def\finalbuild{}"}[variant]
    for w in workshop_dirs(args.workshop):
        tex = w / "slides" / f"{short(w)}.tex"
        if variant == "final" and (markers := prep_markers(tex)):
            sys.exit(f"{tex.relative_to(ROOT)} still has {len(markers)} PREP item(s); resolve them first:\n  "
                     + "\n  ".join(m[:110] for m in markers))
        write_dossier(w)
        job = short(w) if variant == "draft" else f"{short(w)}-{variant}"
        pdf = latexmk(tex, BUILD / short(w), job, pretex)
        print(f"{variant:8} {pdf.relative_to(ROOT)}")


def cmd_activity(args) -> None:
    for w in workshop_dirs(args.workshop):
        for tex in sorted((w / "activity").glob("*.tex")):
            pdf = latexmk(tex, BUILD / short(w), tex.stem, biber=False)
            print(f"activity {pdf.relative_to(ROOT)}")


def cmd_build(args) -> None:
    cmd_test(args)
    cmd_run(args)
    args.final = args.notes = args.handout = False
    cmd_slides(args)
    cmd_activity(args)
    cmd_dossier(args)


def cmd_note(args) -> None:
    rid = args.reading_id
    m = re.fullmatch(r"R(\d)\.\d+", rid)
    if not m:
        sys.exit("reading ids look like R1.7")
    w = workshop_dirs(f"w{m.group(1)}")[0]
    reading = next((r for r in read_workshop(w)["readings"] if r["id"] == rid), None)
    if reading is None:
        sys.exit(f"{rid} is not in {w.name}/README.md")
    path = w / "notes" / f"{rid}.md"
    if path.exists():
        print(f"exists: {path.relative_to(ROOT)}")
        return
    path.write_text(NOTE_TEMPLATE.format(**reading), encoding="utf-8")
    print(f"created: {path.relative_to(ROOT)}")


def cmd_log(args) -> None:
    w = workshop_dirs(args.workshop)[0]
    if args.hours <= 0:
        sys.exit("hours must be positive")
    date = args.date or dt.date.today().isoformat()
    append_row(w / "log.md", "## Preparation log",
               [date, f"{args.hours:g}", args.activity, args.description, args.output or ""])
    print(f"logged {args.hours:g} h of {args.activity} for {w.name} on {date}")


def cmd_rehearsal(args) -> None:
    w = workshop_dirs(args.workshop)[0]
    date = args.date or dt.date.today().isoformat()
    append_row(w / "log.md", "## Rehearsals", [date, str(args.minutes), args.audience, args.feedback, args.changes])
    print(f"recorded a {args.minutes}-minute rehearsal for {w.name} on {date}")


def evidence(w: Path) -> dict:
    info = read_workshop(w)
    log = w / "log.md"
    hours: dict[str, float] = {}
    for m in section_rows(log, "## Preparation log", LOG_ROW):
        hours[m.group(3)] = hours.get(m.group(3), 0.0) + float(m.group(2))
    rehearsals = len(section_rows(log, "## Rehearsals", REHEARSAL_ROW))
    core = [r for r in info["readings"] if r["core"]]
    done, missing = [], []
    for r in core:
        note = w / "notes" / f"{r['id']}.md"
        (done if note.exists() and "TODO" not in note.read_text(encoding="utf-8") else missing).append(r["id"])
    scripts = sorted((w / "experiments").glob("e[0-9]*_*.py"))
    results = [p for p in (w / "results").glob("*.tex") if p.stem != "prep_summary"] if (w / "results").exists() else []
    sources = scripts + list((ROOT / "agentsim").glob("*.py")) + list((w / "experiments").glob("*.json"))
    current = bool(results) and min(p.stat().st_mtime for p in results) >= max(p.stat().st_mtime for p in sources)
    tex = w / "slides" / f"{short(w)}.tex"
    src = tex.read_text(encoding="utf-8")
    frames = src.count(r"\begin{frame}") + src.count(r"\discussion{")
    final_pdf = BUILD / short(w) / f"{short(w)}-final.pdf"
    return {
        "title": info["title"], "budget": info["budget"], "outcomes": len(info["outcomes"]),
        "hours": hours, "hours_total": round(sum(hours.values()), 2), "rehearsals": rehearsals,
        "core": len(core), "notes_done": done, "notes_missing": missing,
        "scripts": len(scripts), "results_current": current, "frames": frames,
        "prep_markers": len(prep_markers(tex)), "final_pdf": final_pdf.exists(),
    }


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
        return out.stdout.strip() + (" + uncommitted changes" if dirty.strip() else "") if out.returncode == 0 else "n/a"
    except OSError:
        return "n/a"


def write_dossier(w: Path) -> dict:
    """Write results/prep_summary.tex, shown on the deck's 'How this workshop was prepared' slide."""
    e = evidence(w)
    split = ", ".join(f"{k} {v:g}" for k, v in sorted(e["hours"].items())) or "none logged yet"
    rows = [
        ("Hours logged", f"{e['hours_total']:g} of {e['budget']} budgeted ({split})"),
        ("Reading notes", f"{len(e['notes_done'])} of {e['core']} core readings"),
        ("Experiments", f"{e['scripts']} scripts; results {'current' if e['results_current'] else 'out of date'}"),
        ("Slides", f"{e['frames']} frames; {e['prep_markers']} open preparation items"),
        ("Rehearsals", f"{e['rehearsals']} recorded"),
        ("Repository", f"commit {git_commit()}"),
    ]
    esc = lambda s: s.replace("_", r"\_").replace("%", r"\%").replace("#", r"\#").replace("&", r"\&")  # noqa: E731
    body = "\n".join(rf"{esc(k)} & {esc(v)} \\" for k, v in rows)
    (w / "results").mkdir(exist_ok=True)
    (w / "results" / "prep_summary.tex").write_text(
        "% generated by tasks.py dossier\n{\\small\\begin{tabular}{@{}l l@{}}\n\\toprule\n" + body
        + f"\n\\bottomrule\n\\end{{tabular}}}}\n\n\\vspace{{2mm}}{{\\scriptsize Generated "
        + f"{dt.date.today().isoformat()} by \\texttt{{python tasks.py dossier}}.}}\n", encoding="utf-8")
    return e


def cmd_dossier(args) -> None:
    lines = [f"# Preparation dossier", "", f"Generated {dt.date.today().isoformat()} · commit {git_commit()}", ""]
    for w in workshop_dirs(getattr(args, "workshop", "all")):
        e = write_dossier(w)
        checks = [
            ("Every core reading has a completed note", not e["notes_missing"]),
            ("Preparation hours are logged", e["hours_total"] > 0),
            ("At least one rehearsal is recorded", e["rehearsals"] >= 1),
            ("Experiment results are current", e["results_current"]),
            ("No open PREP items in the deck", e["prep_markers"] == 0),
            ("Final deck is built", e["final_pdf"]),
        ]
        lines += [f"## {e['title']}", "",
                  "| Evidence | Status |", "|---|---|",
                  f"| Hours logged | {e['hours_total']:g} of {e['budget']} |",
                  f"| By activity | {', '.join(f'{k} {v:g}' for k, v in sorted(e['hours'].items())) or '—'} |",
                  f"| Learning outcomes | {e['outcomes']} |",
                  f"| Core reading notes | {len(e['notes_done'])} of {e['core']} |",
                  f"| Experiments | {e['scripts']} scripts, results {'current' if e['results_current'] else 'out of date'} |",
                  f"| Slides | {e['frames']} frames, {e['prep_markers']} open PREP items |",
                  f"| Rehearsals | {e['rehearsals']} |", "",
                  "Ready for examination:", ""]
        lines += [f"- [{'x' if ok else ' '}] {label}" for label, ok in checks]
        if e["notes_missing"]:
            lines += ["", f"Notes still needed: {', '.join(e['notes_missing'])}"]
        lines.append("")
    report = "\n".join(lines)
    BUILD.mkdir(exist_ok=True)
    (BUILD / "dossier.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"written to {(BUILD / 'dossier.md').relative_to(ROOT)}")


def cmd_links(_args) -> None:
    sys.exit(subprocess.call([sys.executable, "scripts/check_links.py"], cwd=ROOT))


def cmd_clean(_args) -> None:
    shutil.rmtree(BUILD, ignore_errors=True)
    for w in workshop_dirs("all"):
        shutil.rmtree(w / "results", ignore_errors=True)
    print("removed build/ and results/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def with_workshop(p):
        p.add_argument("workshop", nargs="?", default="all", help="w1, w2, w3, or all")
        return p

    sub.add_parser("test").set_defaults(func=cmd_test)
    with_workshop(sub.add_parser("run")).set_defaults(func=cmd_run)
    p = with_workshop(sub.add_parser("slides"))
    g = p.add_mutually_exclusive_group()
    g.add_argument("--final", action="store_true", help="presentation copy; refuses while PREP items remain")
    g.add_argument("--notes", action="store_true", help="speaker notes on a second screen")
    g.add_argument("--handout", action="store_true", help="participant copy without overlays")
    p.set_defaults(func=cmd_slides)
    with_workshop(sub.add_parser("activity")).set_defaults(func=cmd_activity)
    with_workshop(sub.add_parser("build")).set_defaults(func=cmd_build)
    p = sub.add_parser("note")
    p.add_argument("reading_id")
    p.set_defaults(func=cmd_note)
    p = sub.add_parser("log")
    p.add_argument("workshop")
    p.add_argument("hours", type=float)
    p.add_argument("activity", choices=ACTIVITIES)
    p.add_argument("description")
    p.add_argument("--output", help="file the work produced, e.g. notes/R1.7.md")
    p.add_argument("--date", help="YYYY-MM-DD; defaults to today")
    p.set_defaults(func=cmd_log)
    p = sub.add_parser("rehearsal")
    p.add_argument("workshop")
    p.add_argument("minutes", type=int)
    p.add_argument("audience")
    p.add_argument("feedback")
    p.add_argument("changes")
    p.add_argument("--date")
    p.set_defaults(func=cmd_rehearsal)
    with_workshop(sub.add_parser("dossier")).set_defaults(func=cmd_dossier)
    sub.add_parser("links").set_defaults(func=cmd_links)
    sub.add_parser("clean").set_defaults(func=cmd_clean)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
