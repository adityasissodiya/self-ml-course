<!-- GENERATED -->
# From Perceptron to GPT: Deep Learning From Scratch

A self-paced course that walks you from a single perceptron all the way to a
**decoder-only transformer doing next-token prediction**, built from scratch. No CNNs, no RNNs, no diffusion,
no pretrained weights - just the line from linear units to a working GPT.

## Recommended setup

For Windows users and for the lowest-friction setup, use the supplied VS Code devcontainer. It ships Python, numpy, pytest, TeX, git, bash, and curl in one reproducible environment. See `SETUP.md` for the full setup path, native fallback, Docker CLI usage, and instructor CI notes.

## Quick start

```
python tools/course.py serve
```

That serves the whole repo and opens a **course hub** in your browser with a
one-click link to every quiz. (Quizzes load their questions with `fetch`, which
browsers block over `file://`, so opening the `.html` directly just hangs on
"Loading..." - always go through `python tools/course.py serve` or `serve.py`.) Stop it with Ctrl-C.

Everything is Python standard library - no `pip install` needed to take quizzes.
`numpy` (and optionally `pytest`) are only needed for the coding exercises.

You learn by doing two things together: **answer the concept quizzes** (which
record your progress) and **grow one real codebase** from a perceptron into a
working GPT.

## How the course is organized

Two tracks share this one repo:

- **Concept track** (`concepts/NN-slug/`) - the "textbook". One folder per
  concept, each with a short lesson, a browser quiz, and (for most) a small numpy
  exercise. The quizzes are the gamified progress system.
- **Project track** (`project/`) - one cumulative codebase you grow across ten
  milestones (P0-P9) into a working GPT. Milestones *reference* concepts but
  advance on their own cadence, so a single milestone can span several concept
  folders. That is why the numbering "jumps" between the tracks - it is
  intentional.

Pick a **handle** (lowercase `a-z`, digits, `_`, `-`) and use the same one
everywhere - your quiz progress is tied to it.

## Anatomy of a concept module

Each `concepts/NN-slug/` folder contains:

| File / folder | What it is | What you do with it |
|---------------|------------|---------------------|
| `README.md`   | The module's objectives, prerequisites, and sources. | Read it first. |
| `module.tex`  | The lesson - prose and math (also compiled into the course PDF). | Read it; this is the "textbook page". |
| `quiz/`       | A short browser quiz (3-5 questions). | Take it to record progress (below). |
| `exercise/`   | A standalone numpy drill (most modules). | Implement it until its tests pass. |

Work a module in that order: read `README.md` -> read `module.tex` -> do the
`exercise/` -> take the `quiz/`.

## Taking a quiz (how progress is recorded)

Everything is **local** - no server, no git push.

1. Run `python tools/course.py serve` and click a quiz on the hub (or open
   `http://127.0.0.1:8000/concepts/NN-slug/quiz/`).
2. Answer every question and enter your **handle**.
3. Click **Get my shard** and copy the `handle:shard` line it produces.
4. Paste that line into the **Submit a shard** box on the hub. It checks your
   answers locally; if they are correct it saves `progress/NN.key` and rebuilds
   your course PDF (`tex/main.pdf`) on the spot. If they are wrong it tells you,
   and nothing is recorded.

Your shard is HMAC-bound to your handle, so pasting someone else's line records
progress under *their* handle, not yours.

A module can be verified once its quiz has an answer key (see
`ci/answers.example.json`). The bundled example key now covers all quiz modules
01-13; copy it to `ci/answers.json` on a grading server or for local validation.

## Doing the coding exercises

Exercises are disposable practice for the concept. They do **not** become part of
the project and are **not** submitted, but the same operations reappear in a
milestone later, so write them cleanly.

1. `cd concepts/NN-slug/exercise` and read its `README.md`.
2. Implement the functions in `starter.py` - **numpy only**; the point is to
   write them yourself, so don't import a library version.
3. Run the tests:
   ```
   python tools/course.py test-exercise concepts/NN-slug/exercise
   ```
4. Iterate until every test passes. There is no solution in the repo - by design.

## The project track (build the GPT)

`project/` is one package, `dlgpt/`, grown across ten milestones:

- **P0 is already implemented** - the plumbing (char tokenizer, batching, a
  passing test). Everything after it is yours.
- **P1-P9 ship as failing tests** in `project/tests/` that encode each spec. Make
  them pass **in order**, building on what came before, until P9 generates text.

```
python tools/course.py test-project        # P0 smoke test
python tools/course.py test-project --all  # P1..P9 fail until you build them
```

When you start implementing a stub file in `dlgpt/`, **flip its first line to
`# AUTHORED`**. Re-running `scaffold.py` then never overwrites your work (the same
guard protects authored concept files and quizzes).

## Recommended path

Work the concepts **roughly in numeric order** - per-module prereqs are in the
table below. For each: read it, do the exercise if there is one, then take the
quiz and paste the key into the hub. Tackle the matching project milestone when
you reach it (the "Milestones" column links them). The two tracks reinforce each
other; doing them together is the intended experience.

## Concepts

| ID | Title | Quiz | Exercise | Prereqs | Milestones |
|----|-------|------|----------|---------|------------|
| 00 | Math & tooling prerequisites | no | no | - | - |
| 01 | The perceptron / linear unit | yes | yes | 00 | - |
| 02 | Limits of linearity (XOR) | yes | yes | 01 | - |
| 03 | Softmax, cross-entropy, and the p-y gradient | yes | yes | 01 | P2 |
| 04 | Multi-layer perceptron | yes | yes | 02, 03 | P2 |
| 05 | Backpropagation / autograd over a graph | yes | no | 04 | P1 |
| 06 | Gradient descent, SGD, Adam | yes | yes | 05 | P2 |
| 07 | Embeddings / token vectors | yes | yes | 03 | P3 |
| 08 | Scaled dot-product self-attention | yes | yes | 06, 07 | P4 |
| 09 | Causal masking | yes | yes | 08 | P5 |
| 10 | Multi-head attention | yes | no | 09 | P6 |
| 11 | Positional encoding | yes | yes | 08 | P7 |
| 12 | Transformer block (residual + LayerNorm + FFN) | yes | no | 10, 11 | P8 |
| 13 | Decoder-only LM head + sampling | yes | no | 12 | P9 |

## Project milestones

| ID | Title | Depends on | Uses concepts | Implemented? |
|----|-------|-----------|----------------|--------------|
| P0 | Bootstrap | - | - | **yes (plumbing)** |
| P1 | Autograd engine | P0 | 05 | no (learner) |
| P2 | NN primitives | P1 | 03, 04, 06 | no (learner) |
| P3 | Embeddings + char LM baseline | P2 | 07 | no (learner) |
| P4 | Single-head self-attention | P3 | 08 | no (learner) |
| P5 | Causal masking | P4 | 09 | no (learner) |
| P6 | Multi-head attention | P5 | 10 | no (learner) |
| P7 | Positional encoding | P6 | 11 | no (learner) |
| P8 | Transformer block | P7 | 12 | no (learner) |
| P9 | Decoder-only GPT + sampling | P8 | 13 | no (learner) |

Only **P0** ships implemented. **You implement P1-P9** by making their tests pass
in order (see "The project track" above).

## Where your progress lives

There is no website to log into. The course **PDF is the dashboard**: each time
you submit a correct key on the hub, `serve.py` regenerates `tex/progress.tex`
and rebuilds `tex/main.pdf` locally. Open `tex/main.pdf` to see your completed
modules under your handle. (No TeX Live installed? Your keys are still saved;
the PDF rebuild is simply skipped until you install it.)

## Prerequisites

- Recommended: VS Code devcontainer (see `SETUP.md`) for Python, numpy, pytest, TeX, git, bash, and curl.
- Native fallback: Python 3.10+; serving and quizzes use only the standard library.
- `numpy` for the coding exercises; `pytest` is optional (each exercise's test
  file has a stdlib fallback: `python test_exercise.py`).
- A browser (the quizzes are static vanilla HTML/CSS/JS - no Node required).
- TeX Live (`latexmk` or `pdflatex`) **if you want the PDF dashboard** rebuilt
  locally. Optional - progress is recorded with or without it.

## Troubleshooting

- **Quiz stuck on "Loading..."** - you opened it as a `file://` path. Start
  `python tools/course.py serve` and reach it through the hub instead.
- **"Those answers are not all correct"** - the shard did not match the answer
  key; re-take the quiz. (Only modules with an authored answer key can be
  verified.)
- **"No answer key for module NN yet"** - the active `ci/answers.json` is
  missing that module. Copy/update entries from `ci/answers.example.json`.
- **PDF did not rebuild** - install TeX Live (`latexmk`/`pdflatex`); your keys
  are saved regardless. On a LaTeX error, see `tex/main.log`.
- **`No module named pytest`** - run the test directly:
  `python test_exercise.py` (built-in stdlib fallback).
- **Port 8000 already in use** - `python tools/course.py serve --port 9000` (it also
  auto-picks the next free port).

## For instructors / hosted setups

The local flow above is fully self-contained. If you instead want a shared,
server-graded deployment (students push keys; a runner validates and publishes
one central PDF), that pipeline still ships in `ci/` - see `ci/SERVER_SETUP.md`.
Never commit the real answer key (`ci/answers.json`).
