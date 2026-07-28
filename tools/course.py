#!/usr/bin/env python3
"""Cross-platform course helper.

This wraps the repo's existing commands without requiring a POSIX shell. It is
the preferred entry point for students on Windows and for devcontainer users.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Iterable


ROOT = pathlib.Path(__file__).resolve().parents[1]


def in_container() -> bool:
    return (
        pathlib.Path("/.dockerenv").exists()
        or os.environ.get("REMOTE_CONTAINERS") == "true"
        or bool(os.environ.get("CODESPACES"))
        or bool(os.environ.get("DEVCONTAINER"))
    )


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def executable(name: str) -> str | None:
    return shutil.which(name)


def run(cmd: list[str], *, env: dict[str, str] | None = None, cwd: pathlib.Path = ROOT) -> int:
    print("+ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, env=env).returncode


def status_line(ok: bool, label: str, detail: str) -> None:
    mark = "OK" if ok else "MISSING"
    print(f"{mark:7} {label:<18} {detail}")


def command_doctor(args: argparse.Namespace) -> int:
    checks: list[tuple[bool, str, str, bool]] = []
    checks.append((
        sys.version_info >= (3, 10),
        "Python",
        f"{sys.version.split()[0]} at {sys.executable}",
        True,
    ))
    checks.append((has_module("numpy"), "numpy", "coding exercises", True))
    checks.append((has_module("pytest"), "pytest", "project and exercise tests", True))

    latexmk = executable("latexmk")
    pdflatex = executable("pdflatex")
    checks.append((
        bool(latexmk or pdflatex),
        "TeX",
        latexmk or pdflatex or "PDF rebuilds will be skipped",
        False,
    ))

    for tool, detail, required in (
        ("git", "needed by instructor CI runner", False),
        ("curl", "needed by publish.sh on instructor server", False),
        ("bash", "needed by ci/build.sh and publish.sh", False),
    ):
        found = executable(tool)
        checks.append((bool(found), tool, found or detail, required and args.strict))

    print("Course environment")
    print(f"Root: {ROOT}")
    print(f"Container: {'yes' if in_container() else 'no'}")
    print()

    failed = False
    for ok, label, detail, required in checks:
        status_line(ok, label, detail)
        if required and not ok:
            failed = True

    print()
    if failed:
        print("Install the missing required items, or use the supplied devcontainer.")
        return 1
    print("Environment is usable. Missing optional tools only affect the features named above.")
    return 0


def command_serve(args: argparse.Namespace) -> int:
    host = args.host
    if host is None:
        host = "0.0.0.0" if in_container() else "127.0.0.1"

    browser = args.browser
    if browser is None:
        browser = not in_container()

    cmd = [
        sys.executable,
        str(ROOT / "serve.py"),
        "--host",
        host,
        "--port",
        str(args.port),
    ]
    if browser:
        cmd.append("--browser")
    else:
        cmd.append("--no-browser")
    return run(cmd)


def project_test_path(milestone: str) -> pathlib.Path:
    key = milestone.upper()
    if key == "P0":
        return ROOT / "project" / "tests" / "test_p0_data.py"
    if key.startswith("P") and key[1:].isdigit():
        return ROOT / "project" / "tests" / f"test_p{int(key[1:])}.py"
    raise ValueError(f"Unknown milestone {milestone!r}; use P0 through P9.")


def command_test_project(args: argparse.Namespace) -> int:
    if not has_module("pytest"):
        print("pytest is not installed. Run `python -m pip install -r requirements.txt`.")
        return 1

    if args.all:
        targets = [str(ROOT / "project" / "tests")]
    else:
        try:
            targets = [str(project_test_path(args.milestone))]
        except ValueError as exc:
            print(exc)
            return 2
    return run([sys.executable, "-m", "pytest", *targets])


def exercise_tests() -> Iterable[pathlib.Path]:
    return sorted((ROOT / "concepts").glob("*/exercise/test_exercise.py"))


def resolve_exercise_target(value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    if not path.is_absolute():
        path = ROOT / path
    if path.is_dir():
        path = path / "test_exercise.py"
    return path


def command_test_exercise(args: argparse.Namespace) -> int:
    if args.all:
        tests = list(exercise_tests())
        if not tests:
            print("No exercise tests found.")
            return 1
    elif args.path:
        tests = [resolve_exercise_target(args.path)]
    else:
        print("Pass an exercise directory/test file, or use --all.")
        return 2

    missing = [path for path in tests if not path.exists()]
    if missing:
        for path in missing:
            print(f"Missing: {rel(path)}")
        return 1

    if has_module("pytest"):
        return run([sys.executable, "-m", "pytest", *map(str, tests)])

    code = 0
    for test in tests:
        code = run([sys.executable, str(test)], cwd=test.parent) or code
    return code


def command_pdf(args: argparse.Namespace) -> int:
    sys.path.insert(0, str(ROOT))
    import serve  # pylint: disable=import-error,import-outside-toplevel

    completed = serve.rebuild_progress_tex()
    built, reason = serve.rebuild_pdf()
    if built:
        print(f"PDF rebuilt: {rel(ROOT / 'tex' / 'main.pdf')} ({completed} modules complete)")
        return 0
    print(reason)
    return 1


def command_validate(args: argparse.Namespace) -> int:
    answers = pathlib.Path(args.answers)
    if not answers.is_absolute():
        answers = ROOT / answers
    return run([sys.executable, str(ROOT / "ci" / "validate.py"), str(answers)])


def command_local_ci(args: argparse.Namespace) -> int:
    answers = pathlib.Path(args.answers)
    if not answers.is_absolute():
        answers = ROOT / answers

    env = os.environ.copy()
    env["DLGPT_SKIP_GIT"] = "1"
    env["DLGPT_SKIP_PUBLISH"] = "1"
    env["DLGPT_ANSWERS"] = str(answers)
    return run([sys.executable, str(ROOT / "ci" / "runner.py")], env=env)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the dlgpt course locally.")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check local tools and Python packages.")
    doctor.add_argument("--strict", action="store_true", help="Fail when optional CI tools are missing.")
    doctor.set_defaults(func=command_doctor)

    serve = sub.add_parser("serve", help="Start the local course hub.")
    serve.add_argument("--host", default=None, help="Bind host. Defaults to 0.0.0.0 in containers.")
    serve.add_argument("--port", type=int, default=8000)
    browser = serve.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="browser", action="store_true", default=None)
    browser.add_argument("--no-browser", dest="browser", action="store_false")
    serve.set_defaults(func=command_serve)

    test_project = sub.add_parser("test-project", help="Run project milestone tests.")
    test_project.add_argument("--milestone", default="P0", help="Milestone to test, P0 through P9. Default: P0.")
    test_project.add_argument("--all", action="store_true", help="Run every project test. Fresh clones fail by design.")
    test_project.set_defaults(func=command_test_project)

    test_exercise = sub.add_parser("test-exercise", help="Run one or all standalone exercise tests.")
    test_exercise.add_argument("path", nargs="?", help="Exercise directory or test_exercise.py path.")
    test_exercise.add_argument("--all", action="store_true", help="Run all exercise tests.")
    test_exercise.set_defaults(func=command_test_exercise)

    pdf = sub.add_parser("pdf", help="Regenerate progress.tex and rebuild tex/main.pdf.")
    pdf.set_defaults(func=command_pdf)

    validate = sub.add_parser("validate", help="Validate progress shards against an answer key.")
    validate.add_argument("--answers", default="ci/answers.example.json")
    validate.set_defaults(func=command_validate)

    local_ci = sub.add_parser("local-ci", help="Run the CI runner locally without pull or publish.")
    local_ci.add_argument("--answers", default="ci/answers.example.json")
    local_ci.set_defaults(func=command_local_ci)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
