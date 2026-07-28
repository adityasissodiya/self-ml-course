# Course Environment Setup

The supported setup is a VS Code devcontainer. It gives every student the same
Python, numpy, pytest, TeX, git, bash, and curl environment, including Windows
users who do not have TeX or Python installed natively.

## Recommended: VS Code Devcontainer

Install:

- Docker Desktop
- Visual Studio Code
- VS Code extension: Dev Containers

Then:

1. Open this repo in VS Code.
2. Choose **Dev Containers: Reopen in Container**.
3. Wait for the container build to finish.
4. Start the course hub:

   ```sh
   python tools/course.py serve
   ```

VS Code forwards port 8000 automatically. Open the forwarded **Course hub** URL
in your browser.

## Docker Without VS Code

```sh
docker build -t dlgpt-course .
docker run --rm -it -p 8000:8000 -v "$(pwd):/workspace" dlgpt-course
```

On Windows Command Prompt, use `%cd%`:

```bat
docker run --rm -it -p 8000:8000 -v "%cd%:/workspace" dlgpt-course
```

On PowerShell, `%cd%` may need to be replaced with `${PWD}`:

```powershell
docker run --rm -it -p 8000:8000 -v "${PWD}:/workspace" dlgpt-course
```

Then open `http://127.0.0.1:8000/`.

## Native Fallback

Native setup is useful if you already have Python and TeX installed. The
devcontainer is still the expected path for students who want the fewest moving
parts.

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tools/course.py doctor
python tools/course.py serve
```

macOS/Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/course.py doctor
python tools/course.py serve
```

TeX is optional for learning. If TeX is missing, quiz progress is still saved;
only local PDF rebuilds are skipped until TeX is installed or the course is run
inside the devcontainer.

## Useful Commands

```sh
python tools/course.py doctor
python tools/course.py serve
python tools/course.py test-project
python tools/course.py test-project --milestone P3
python tools/course.py test-project --all
python tools/course.py test-exercise concepts/01-perceptron/exercise
python tools/course.py test-exercise --all
python tools/course.py pdf
python tools/course.py validate
python tools/course.py local-ci
```

Notes:

- `test-project` defaults to P0, which should pass on a fresh clone.
- `test-project --all` fails on a fresh clone by design because P1-P9 are the
  learner's work.
- `local-ci` runs the CI runner without `git pull` or publishing.

## Instructor CI Dependencies

The instructor/server runner uses:

- Python 3.10+
- TeX Live with `latexmk` or `pdflatex`
- `git` for pull-based updates
- `bash` for `ci/build.sh` and `ci/publish.sh`
- `curl` for the example WebDAV/Nextcloud publish step

The devcontainer includes all of these. A production server can also follow
`ci/SERVER_SETUP.md`.
