#!/usr/bin/env python3
"""scaffold.py — idempotent generator for the dlgpt course repo.

This is the build tool described by COURSE_BUILD_SPEC.md. Re-running it is safe:
 - files whose first line contains the token "AUTHORED" are never touched;
 - generated/stub files are rewritten only when their content actually changes;
 - per-quiz salts already present in questions.json are preserved (so re-running
   produces a byte-identical tree apart from build artifacts).

Usage:  python3 scaffold.py
"""
import json
import pathlib
import secrets

ROOT = pathlib.Path(__file__).resolve().parent

STATS = {"written": [], "unchanged": [], "authored_skipped": []}


# --------------------------------------------------------------------------- #
# write helper (sentinel-aware idempotency)
# --------------------------------------------------------------------------- #
def write(path: pathlib.Path, content: str):
    """Write content unless the target is AUTHORED or already identical."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        first = existing.splitlines()[:1]
        if first and "AUTHORED" in first[0]:
            STATS["authored_skipped"].append(str(path.relative_to(ROOT)))
            return
        if existing == content:
            STATS["unchanged"].append(str(path.relative_to(ROOT)))
            return
    path.write_text(content, encoding="utf-8")
    STATS["written"].append(str(path.relative_to(ROOT)))


def touch(path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")
        STATS["written"].append(str(path.relative_to(ROOT)))
    else:
        STATS["unchanged"].append(str(path.relative_to(ROOT)))


# --------------------------------------------------------------------------- #
# manifest (verbatim from spec §3)
# --------------------------------------------------------------------------- #
MANIFEST = {
    "course": {
        "id": "dlgpt",
        "title": "From Perceptron to GPT: Deep Learning From Scratch",
        "key_prefix": "DLX",
        "endpoint": "decoder-only transformer doing next-token prediction",
        "version": "1.0.0",
    },
    "canonicalization": {
        "question_id_format": "q%02d",
        "option_labels": ["a", "b", "c", "d"],
        "answer_join": ";",
        "pair_format": "{id}={letter}",
        "message_format": "{handle}|{module_id}|{canonical}",
        "shard_hex_len": 12,
        "shard_case": "upper",
        "handle_charset": "[a-z0-9_-]+",
    },
    "concepts": [
        {"id": "00", "slug": "prerequisites",        "title": "Math & tooling prerequisites",                   "quiz": False, "exercise": False, "prereq": [],            "milestones": [],     "sources": ["GBC Ch.2-4"]},
        {"id": "01", "slug": "perceptron",            "title": "The perceptron / linear unit",                   "quiz": True,  "exercise": True,  "prereq": ["00"],        "milestones": [],     "sources": ["3B1B-nn"]},
        {"id": "02", "slug": "linear-limits-xor",     "title": "Limits of linearity (XOR)",                      "quiz": True,  "exercise": True,  "prereq": ["01"],        "milestones": [],     "sources": ["3B1B-nn"]},
        {"id": "03", "slug": "softmax-cross-entropy", "title": "Softmax, cross-entropy, and the p-y gradient",   "quiz": True,  "exercise": True,  "prereq": ["01"],        "milestones": ["P2"], "sources": ["GBC Ch.4", "d2l 4.1", "karpathy-micrograd"]},
        {"id": "04", "slug": "mlp",                   "title": "Multi-layer perceptron",                         "quiz": True,  "exercise": True,  "prereq": ["02", "03"],  "milestones": ["P2"], "sources": ["karpathy-makemore", "GBC Ch.6"]},
        {"id": "05", "slug": "backprop-autograd",     "title": "Backpropagation / autograd over a graph",        "quiz": True,  "exercise": False, "prereq": ["04"],        "milestones": ["P1"], "sources": ["karpathy-micrograd", "GBC Ch.6.5"]},
        {"id": "06", "slug": "optimization",          "title": "Gradient descent, SGD, Adam",                    "quiz": True,  "exercise": True,  "prereq": ["05"],        "milestones": ["P2"], "sources": ["GBC Ch.8", "d2l 12"]},
        {"id": "07", "slug": "embeddings",            "title": "Embeddings / token vectors",                     "quiz": True,  "exercise": True,  "prereq": ["03"],        "milestones": ["P3"], "sources": ["karpathy-makemore", "3B1B-attention", "alammar"]},
        {"id": "08", "slug": "self-attention",        "title": "Scaled dot-product self-attention",              "quiz": True,  "exercise": True,  "prereq": ["06", "07"],  "milestones": ["P4"], "sources": ["alammar", "annotated-transformer", "d2l 11", "vaswani-2017"]},
        {"id": "09", "slug": "causal-masking",        "title": "Causal masking",                                 "quiz": True,  "exercise": True,  "prereq": ["08"],        "milestones": ["P5"], "sources": ["karpathy-nanogpt", "alammar"]},
        {"id": "10", "slug": "multi-head-attention",  "title": "Multi-head attention",                           "quiz": True,  "exercise": False, "prereq": ["09"],        "milestones": ["P6"], "sources": ["annotated-transformer", "d2l 11.5"]},
        {"id": "11", "slug": "positional-encoding",   "title": "Positional encoding",                            "quiz": True,  "exercise": True,  "prereq": ["08"],        "milestones": ["P7"], "sources": ["vaswani-2017", "d2l 11.6"]},
        {"id": "12", "slug": "transformer-block",     "title": "Transformer block (residual + LayerNorm + FFN)", "quiz": True,  "exercise": False, "prereq": ["10", "11"],  "milestones": ["P8"], "sources": ["annotated-transformer", "karpathy-nanogpt"]},
        {"id": "13", "slug": "decoder-lm-head",       "title": "Decoder-only LM head + sampling",                "quiz": True,  "exercise": False, "prereq": ["12"],        "milestones": ["P9"], "sources": ["karpathy-nanogpt", "raschka"]},
    ],
    "milestones": [
        {"id": "P0", "title": "Bootstrap",                     "depends_on": [],      "uses": [],                  "implement": True},
        {"id": "P1", "title": "Autograd engine",               "depends_on": ["P0"],  "uses": ["05"],              "implement": False},
        {"id": "P2", "title": "NN primitives",                 "depends_on": ["P1"],  "uses": ["03", "04", "06"],  "implement": False},
        {"id": "P3", "title": "Embeddings + char LM baseline", "depends_on": ["P2"],  "uses": ["07"],              "implement": False},
        {"id": "P4", "title": "Single-head self-attention",    "depends_on": ["P3"],  "uses": ["08"],              "implement": False},
        {"id": "P5", "title": "Causal masking",                "depends_on": ["P4"],  "uses": ["09"],              "implement": False},
        {"id": "P6", "title": "Multi-head attention",          "depends_on": ["P5"],  "uses": ["10"],              "implement": False},
        {"id": "P7", "title": "Positional encoding",           "depends_on": ["P6"],  "uses": ["11"],              "implement": False},
        {"id": "P8", "title": "Transformer block",             "depends_on": ["P7"],  "uses": ["12"],              "implement": False},
        {"id": "P9", "title": "Decoder-only GPT + sampling",   "depends_on": ["P8"],  "uses": ["13"],              "implement": False},
    ],
}

KEY_PREFIX = MANIFEST["course"]["key_prefix"]
CONCEPTS = MANIFEST["concepts"]
MILESTONES = MANIFEST["milestones"]


# --------------------------------------------------------------------------- #
# static file bodies
# --------------------------------------------------------------------------- #
QUIZ_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Quiz</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main id="app">
    <h1 id="title">Loading…</h1>
    <label class="handle">Your handle (a-z, 0-9, _ or -):
      <input id="handle" autocomplete="off" spellcheck="false">
    </label>
    <form id="quiz"></form>
    <button id="submit" type="button">Get my shard</button>
    <section id="result" hidden>
      <p>Commit this line to <code id="path"></code>:</p>
      <pre id="shard"></pre>
      <button id="copy" type="button">Copy</button>
      <p class="note">The CI runner validates it server-side and updates the course PDF.</p>
    </section>
  </main>
  <script src="quiz.js"></script>
</body>
</html>
"""

QUIZ_JS = r"""async function hmacHex(keyStr, msgStr) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(keyStr), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(msgStr));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

function canonical(answers) {
  // answers: { q01: "b", q02: "a", ... } -> "q01=b;q02=a" sorted by id
  return Object.keys(answers).sort()
    .map(id => `${id}=${answers[id].toLowerCase()}`).join(";");
}

let DATA = null;

async function init() {
  DATA = await (await fetch("questions.json")).json();
  document.getElementById("title").textContent = DATA.title;
  document.getElementById("path").textContent = `progress/${DATA.module_id}.key`;
  const form = document.getElementById("quiz");
  for (const q of DATA.questions) {
    const fs = document.createElement("fieldset");
    fs.innerHTML = `<legend>${q.text}</legend>`;
    for (const [letter, label] of Object.entries(q.options)) {
      const id = `${q.id}_${letter}`;
      fs.insertAdjacentHTML("beforeend",
        `<label><input type="radio" name="${q.id}" value="${letter}" id="${id}"> ${label}</label>`);
    }
    form.appendChild(fs);
  }
  document.getElementById("submit").addEventListener("click", onSubmit);
  document.getElementById("copy").addEventListener("click", () => {
    navigator.clipboard.writeText(document.getElementById("shard").textContent);
  });
}

async function onSubmit() {
  const handle = document.getElementById("handle").value.trim().toLowerCase();
  if (!/^[a-z0-9_-]+$/.test(handle)) { alert("Invalid handle. Use a-z, 0-9, _ or -."); return; }
  const answers = {};
  for (const q of DATA.questions) {
    const sel = document.querySelector(`input[name="${q.id}"]:checked`);
    if (!sel) { alert("Answer every question first."); return; }
    answers[q.id] = sel.value;
  }
  const canon = canonical(answers);
  const msg = `${handle}|${DATA.module_id}|${canon}`;
  const hex = (await hmacHex(DATA.salt, msg)).slice(0, 12).toUpperCase();
  const line = `${handle}:${DATA.course_prefix || "DLX"}-${DATA.module_id}-${hex}`;
  document.getElementById("shard").textContent = line;
  document.getElementById("result").hidden = false;
}

init();
"""

QUIZ_CSS = """:root { --bg:#0f1117; --fg:#e6e6e6; --accent:#7c5cff; --ok:#3ddc84; }
* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--fg);
       max-width: 640px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
h1 { color: var(--accent); }
fieldset { border: 1px solid #2a2f3a; border-radius: 8px; margin: 1rem 0; padding: 1rem; }
legend { font-weight: 600; }
label { display: block; margin: .35rem 0; cursor: pointer; }
.handle input { width: 100%; padding: .5rem; margin-top: .25rem;
                background: #161922; color: var(--fg); border: 1px solid #2a2f3a; border-radius: 6px; }
button { background: var(--accent); color: #fff; border: 0; border-radius: 6px;
         padding: .6rem 1rem; font-size: 1rem; cursor: pointer; }
pre { background: #161922; padding: .75rem; border-radius: 6px; color: var(--ok); overflow-x: auto; }
.note { color: #9aa0aa; font-size: .9rem; }
"""

VALIDATE_PY = r'''"""Validate committed shards against the server-side answer key."""
import hmac, hashlib, json, re, pathlib, glob

ROOT = pathlib.Path(__file__).resolve().parent.parent
HANDLE_RE = re.compile(r"^[a-z0-9_-]+$")

def shard(salt: str, handle: str, module_id: str, canonical: str) -> str:
    msg = f"{handle}|{module_id}|{canonical}".encode()
    return hmac.new(salt.encode(), msg, hashlib.sha256).hexdigest()[:12].upper()

def load_salt(module_id: str) -> str:
    matches = list(ROOT.glob(f"concepts/{module_id}-*/quiz/questions.json"))
    if not matches:
        raise FileNotFoundError(f"no quiz for module {module_id}")
    return json.loads(matches[0].read_text())["salt"]

def parse_keyfile(path: pathlib.Path):
    """File content: 'handle:DLX-NN-XXXXXXXXXXXX'. Returns (handle, core_hex)."""
    line = path.read_text().strip()
    handle, token = line.split(":", 1)
    handle = handle.strip().lower()
    core = token.strip().split("-")[-1].upper()
    return handle, core

def validate_all(answers_path: str):
    answers = json.loads(pathlib.Path(answers_path).read_text())  # {"03": "q01=b;q02=b;q03=c", ...}
    results = []  # (handle, module_id, ok)
    for kf in sorted(glob.glob(str(ROOT / "progress" / "*.key"))):
        p = pathlib.Path(kf)
        module_id = p.stem  # "03"
        if module_id not in answers:
            results.append((None, module_id, False)); continue
        try:
            handle, core = parse_keyfile(p)
            if not HANDLE_RE.match(handle):
                results.append((handle, module_id, False)); continue
            expected = shard(load_salt(module_id), handle, module_id, answers[module_id])
            ok = hmac.compare_digest(core, expected)
            results.append((handle, module_id, ok))
        except Exception:
            results.append((None, module_id, False))
    return results

if __name__ == "__main__":
    import sys
    for handle, mod, ok in validate_all(sys.argv[1] if len(sys.argv) > 1 else "ci/answers.json"):
        print(f"{mod:>4} {handle or '?':<20} {'OK' if ok else 'FAIL'}")
'''

RUNNER_PY = r'''"""Pull, validate, regenerate progress.tex, build PDF, publish. Run on a timer.

Two environment switches let the self-test run offline (spec self-test C):
  DLGPT_SKIP_GIT=1      skip `git pull`
  DLGPT_SKIP_PUBLISH=1  skip the publish step
  DLGPT_ANSWERS=<path>  override the answer-key path (default ci/answers.json)
In production none of these are set, so the runner pulls, validates, builds and
publishes exactly as described in ci/SERVER_SETUP.md.
"""
import os, subprocess, datetime, pathlib
from validate import validate_all

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANSWERS = pathlib.Path(os.environ.get("DLGPT_ANSWERS", ROOT / "ci" / "answers.json"))
PROGRESS_TEX = ROOT / "tex" / "progress.tex"

def sh(cmd, cwd=ROOT):
    subprocess.run(cmd, cwd=cwd, check=True, shell=isinstance(cmd, str))

def main():
    if os.environ.get("DLGPT_SKIP_GIT") != "1":
        sh(["git", "pull", "--ff-only"])
    results = validate_all(str(ANSWERS))
    today = datetime.date.today().isoformat()
    lines = ["% GENERATED by ci/runner.py - do not edit, do not commit.", ""]
    for handle, mod, ok in results:
        if ok:
            lines.append(f"\\moduledone{{{handle}}}{{{mod}}}{{{today}}}")
    PROGRESS_TEX.write_text("\n".join(lines) + "\n")
    sh(["bash", "ci/build.sh"])
    # Publish step is environment-specific; see publish.sh.example.
    pub = ROOT / "ci" / "publish.sh"
    if pub.exists() and os.environ.get("DLGPT_SKIP_PUBLISH") != "1":
        sh(["bash", str(pub)])

if __name__ == "__main__":
    main()
'''

BUILD_SH = """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../tex"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
"""

PUBLISH_EXAMPLE = """#!/usr/bin/env bash
set -euo pipefail
# Fill in and rename to publish.sh on the server. Do NOT commit real credentials.
NEXTCLOUD_URL="https://cloud.example.org/remote.php/dav/files/USER/course/main.pdf"
NEXTCLOUD_USER="USER"
NEXTCLOUD_PASS="APP_PASSWORD"   # use a Nextcloud app password, not the login password
curl -fsS -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS" -T ../tex/main.pdf "$NEXTCLOUD_URL"
"""

GITIGNORE = """tex/progress.tex
tex/main.pdf
tex/*.aux
tex/*.toc
tex/*.fls
tex/*.fdb_latexmk
tex/*.log
tex/*.out
ci/answers.json
ci/publish.sh
__pycache__/
*.pyc
"""

PREAMBLE_STY = r"""% GENERATED
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{preamble}[2026/06/18 v1.0 dlgpt course preamble]

\RequirePackage{xcolor}
\RequirePackage{booktabs}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{pgffor}

\definecolor{badgedone}{HTML}{3DDC84}
\definecolor{badgetodo}{HTML}{9AA0AA}
\definecolor{dlgptaccent}{HTML}{7C5CFF}

% --- internal completion store -------------------------------------------- %
\newcounter{dlgptdone}
\setcounter{dlgptdone}{0}
\newcommand{\dlgptrows}{}

% \moduledone{handle}{NN}{date}: record one completion.
\newcommand{\moduledone}[3]{%
  \expandafter\gdef\csname dlgptdone@#2\endcsname{1}%
  \stepcounter{dlgptdone}%
  \g@addto@macro\dlgptrows{#1 & #2 & #3 \\}%
}

% \conceptbadge{NN}: tick if a completion was recorded for NN, else circle.
\newcommand{\conceptbadge}[1]{%
  \ifcsname dlgptdone@#1\endcsname
    \colorbox{badgedone}{\textcolor{white}{\textbf{#1~\checkmark}}}%
  \else
    \colorbox{badgetodo}{\textcolor{white}{\textbf{#1~\ensuremath{\circ}}}}%
  \fi
}

% \progressdashboard: table of completions + count / percentage of 14 concepts.
\newcommand{\progressdashboard}{%
  \begin{center}
  \begin{tabular}{lll}
  \toprule
  \textbf{Handle} & \textbf{Module} & \textbf{Date} \\
  \midrule
  \dlgptrows
  \bottomrule
  \end{tabular}
  \end{center}
  \begin{center}
  Completed \thedlgptdone{} of 14 concepts
  (\fpeval{round(100*\thedlgptdone/14,0)}\%).
  \end{center}
}
"""

CONFTEST_PY = """# GENERATED — makes `dlgpt` importable when running `python -m pytest project/tests`.
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
"""

INIT_PY = '''"""dlgpt — the cumulative GPT-from-scratch package (built across P0-P9)."""
__all__ = ["data", "autograd", "nn", "attention", "model"]
'''

DATA_PY = r'''# GENERATED
"""P0 plumbing: character tokenizer + batch loader. Fully implemented.

This is the only project module that ships implemented: it is infrastructure
(tokenization, batching, corpus loading), not the pedagogical core. Everything
in P1-P9 is yours to write.
"""
import pathlib
import random


class CharTokenizer:
    """Maps the characters of a corpus to integer ids and back."""

    def __init__(self, text: str):
        chars = sorted(set(text))
        self.itos = {i: c for i, c in enumerate(chars)}
        self.stoi = {c: i for i, c in enumerate(chars)}
        self.vocab_size = len(chars)

    def encode(self, s: str):
        return [self.stoi[c] for c in s]

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids)


def load_corpus(path=None) -> str:
    """Read the tiny public-domain corpus shipped with the repo."""
    if path is None:
        path = pathlib.Path(__file__).resolve().parent.parent / "corpus" / "tiny.txt"
    return pathlib.Path(path).read_text(encoding="utf-8")


def get_batch(data, batch_size: int, block_size: int, rng=None):
    """Sample `batch_size` contiguous windows of length `block_size`.

    Returns (xb, yb) where each is a list of `batch_size` lists of `block_size`
    ints, and yb is xb shifted by one position (next-character targets).
    """
    if rng is None:
        rng = random.Random()
    assert len(data) > block_size + 1, "corpus shorter than block_size + 1"
    hi = len(data) - block_size - 1
    xb, yb = [], []
    for _ in range(batch_size):
        i = rng.randint(0, hi)
        xb.append(list(data[i:i + block_size]))
        yb.append(list(data[i + 1:i + block_size + 1]))
    return xb, yb
'''

TEST_P0 = r'''# GENERATED — P0 is real, this test must PASS.
import random

from dlgpt import data


def test_tokenizer_roundtrip():
    tok = data.CharTokenizer("hello world")
    assert tok.decode(tok.encode("hello")) == "hello"
    assert tok.vocab_size == len(set("hello world"))


def test_corpus_loads():
    text = data.load_corpus()
    assert len(text) > 200


def test_get_batch_shapes_and_shift():
    tok = data.CharTokenizer(data.load_corpus())
    ids = tok.encode(data.load_corpus())
    xb, yb = data.get_batch(ids, batch_size=4, block_size=8, rng=random.Random(0))
    assert len(xb) == 4 and len(yb) == 4
    assert all(len(r) == 8 for r in xb)
    assert all(len(r) == 8 for r in yb)
    for r in range(4):
        for t in range(7):
            assert yb[r][t] == xb[r][t + 1]


def test_get_batch_deterministic():
    ids = list(range(1000))
    a = data.get_batch(ids, 4, 8, random.Random(42))
    b = data.get_batch(ids, 4, 8, random.Random(42))
    assert a == b
'''

# project package stubs (P1-P9) ------------------------------------------------
AUTOGRAD_PY = '''# STUB
"""P1 - reverse-mode autograd over a scalar graph (concept 05).

Flip the first line of this file to "# AUTHORED" once you start implementing,
so scaffold.py never regenerates over your work.
"""


class Value:
    """A scalar node in the autograd graph. Supports +, *, and .backward().

    P1 spec:
      * Value(x) wraps a float in `.data`, with `.grad` initialised to 0.0.
      * a + b and a * b build the graph and return new Values.
      * c.backward() does reverse-mode autodiff, filling `.grad` on every node.
    """

    def __init__(self, data, _children=(), _op=""):
        raise NotImplementedError(
            "P1: implement Value - see concepts/05-backprop-autograd"
        )

    def __add__(self, other):
        raise NotImplementedError("P1: implement __add__")

    def __mul__(self, other):
        raise NotImplementedError("P1: implement __mul__")

    def backward(self):
        raise NotImplementedError("P1: implement reverse-mode backprop")
'''

TEST_P1 = '''# GENERATED — failing spec for milestone P1 (the learner makes it pass).
from dlgpt import autograd


def test_autograd_add_mul_backward():
    a = autograd.Value(2.0)
    b = autograd.Value(-3.0)
    c = a * b + a            # c = a*b + a
    c.backward()
    # dc/da = b + 1 = -2 ; dc/db = a = 2
    assert abs(a.grad - (-2.0)) < 1e-6
    assert abs(b.grad - 2.0) < 1e-6
'''

NN_PY = '''# STUB
"""P2 - NN primitives (concepts 03, 04, 06).

Build on your P1 autograd: a Linear layer, ReLU, a numerically stable
softmax + cross-entropy returning the (p - y) gradient, and SGD / Adam.

Flip the first line to "# AUTHORED" once you start implementing.
"""


class Linear:
    """Affine layer: y = W x + b. (P2)"""

    def __init__(self, n_in, n_out):
        raise NotImplementedError("P2: implement Linear - concepts 03/04")

    def __call__(self, x):
        raise NotImplementedError("P2: implement Linear.__call__")


def relu(x):
    raise NotImplementedError("P2: implement relu")


def softmax_cross_entropy(logits, target):
    """Return (loss, dlogits) where dlogits == p - y. (P2, concept 03)"""
    raise NotImplementedError("P2: implement softmax_cross_entropy")


class SGD:
    def __init__(self, params, lr):
        raise NotImplementedError("P2: implement SGD - concept 06")

    def step(self):
        raise NotImplementedError("P2: implement SGD.step")


class Adam:
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8):
        raise NotImplementedError("P2: implement Adam - concept 06")

    def step(self):
        raise NotImplementedError("P2: implement Adam.step")
'''

TEST_P2 = '''# GENERATED — failing spec for milestone P2.
from dlgpt import nn


def test_linear_forward_shape():
    layer = nn.Linear(3, 2)
    out = layer([1.0, 2.0, 3.0])
    assert len(out) == 2


def test_softmax_cross_entropy_returns_p_minus_y():
    loss, dlogits = nn.softmax_cross_entropy([2.0, 1.0, 0.0], 0)
    assert isinstance(loss, float)
    assert len(dlogits) == 3
    # gradient must sum to ~0 (it is p - y with a one-hot y)
    assert abs(sum(dlogits)) < 1e-6
'''

ATTENTION_PY = '''# STUB
"""P4-P7 - attention machinery.

  P4 (concept 08): scaled dot-product self-attention.
  P5 (concept 09): causal masking (no future leakage).
  P6 (concept 10): multi-head attention (parallel heads, concat + projection).
  P7 (concept 11): positional encoding added to embeddings.

Flip the first line to "# AUTHORED" once you start implementing.
"""


def self_attention(Q, K, V):
    """Scaled dot-product attention: softmax(Q Kᵀ / sqrt(d)) V. (P4)"""
    raise NotImplementedError("P4: implement self_attention - concept 08")


def causal_mask(scores):
    """Set scores[i][j] = -inf for j > i (no attending to the future). (P5)"""
    raise NotImplementedError("P5: implement causal_mask - concept 09")


def multi_head_attention(x, num_heads):
    """Run `num_heads` attention heads in parallel, concat, project. (P6)"""
    raise NotImplementedError("P6: implement multi_head_attention - concept 10")


def positional_encoding(seq_len, d_model):
    """Return a (seq_len, d_model) table of positional encodings. (P7)"""
    raise NotImplementedError("P7: implement positional_encoding - concept 11")
'''

TEST_P4 = '''# GENERATED — failing spec for milestone P4.
from dlgpt import attention


def test_self_attention_output_shape():
    Q = [[1.0, 0.0], [0.0, 1.0]]
    K = [[1.0, 0.0], [0.0, 1.0]]
    V = [[1.0, 2.0], [3.0, 4.0]]
    out = attention.self_attention(Q, K, V)
    assert len(out) == 2 and len(out[0]) == 2
'''

TEST_P5 = '''# GENERATED — failing spec for milestone P5.
from dlgpt import attention


def test_causal_mask_blocks_future():
    scores = [[1.0, 1.0], [1.0, 1.0]]
    masked = attention.causal_mask(scores)
    assert masked[0][1] == float("-inf")   # token 0 cannot see token 1
    assert masked[1][0] == 1.0             # token 1 may see token 0
'''

TEST_P6 = '''# GENERATED — failing spec for milestone P6.
from dlgpt import attention


def test_multi_head_attention_runs():
    x = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0]]
    out = attention.multi_head_attention(x, num_heads=2)
    assert len(out) == 2
'''

TEST_P7 = '''# GENERATED — failing spec for milestone P7.
from dlgpt import attention


def test_positional_encoding_shape():
    pe = attention.positional_encoding(seq_len=5, d_model=8)
    assert len(pe) == 5
    assert all(len(row) == 8 for row in pe)
'''

MODEL_PY = '''# STUB
"""P8-P9 - the transformer block and the decoder-only GPT.

  P8 (concept 12): TransformerBlock = residual + LayerNorm + FFN; stack N of them.
  P9 (concept 13): GPT with an LM head + greedy/temperature/top-k generation.

Flip the first line to "# AUTHORED" once you start implementing.
"""


class TransformerBlock:
    """Pre-norm transformer block: x + attn(ln(x)), then x + ffn(ln(x)). (P8)"""

    def __init__(self, d_model, num_heads):
        raise NotImplementedError("P8: implement TransformerBlock - concept 12")

    def __call__(self, x):
        raise NotImplementedError("P8: implement TransformerBlock.__call__")


class GPT:
    """Decoder-only language model: embeddings + N blocks + LM head. (P9)"""

    def __init__(self, vocab_size, d_model, num_heads, num_layers, block_size):
        raise NotImplementedError("P9: implement GPT - concept 13")

    def __call__(self, idx):
        raise NotImplementedError("P9: implement GPT.__call__ (logits)")


def generate(model, idx, max_new_tokens, temperature=1.0, top_k=None):
    """Autoregressively sample `max_new_tokens` new ids. (P9)"""
    raise NotImplementedError("P9: implement generate - concept 13")
'''

TEST_P8 = '''# GENERATED — failing spec for milestone P8.
from dlgpt import model


def test_transformer_block_constructs_and_runs():
    block = model.TransformerBlock(d_model=4, num_heads=2)
    out = block([[1.0, 0.0, 1.0, 0.0]])
    assert len(out) == 1 and len(out[0]) == 4
'''

TEST_P9 = '''# GENERATED — failing spec for milestone P9.
from dlgpt import model


def test_gpt_generate_extends_sequence():
    gpt = model.GPT(vocab_size=16, d_model=8, num_heads=2, num_layers=2, block_size=8)
    out = model.generate(gpt, [1, 2, 3], max_new_tokens=5)
    assert len(out) == 3 + 5
'''

# A short, public-domain corpus: three of Aesop's fables (translation public domain).
TINY_TXT = """The North Wind and the Sun disputed as to which was the most powerful, and
agreed that he should be declared the victor who could first strip a wayfaring
man of his clothes. The North Wind first tried his power and blew with all his
might, but the keener his blasts, the closer the traveler wrapped his cloak
around him, till at last, resigning all hope of victory, the Wind called upon
the Sun to see what he could do. The Sun suddenly shone out with all his
warmth. The traveler no sooner felt his genial rays than he took off one
garment after another, and at last, fairly overcome with heat, undressed and
bathed in a stream that lay in his path. Persuasion is better than force.

A Crow, having stolen a piece of cheese from a cottage window, flew up into a
high tree to enjoy her prize. A Fox, seeing this, longed to possess the cheese,
and by a wily stratagem succeeded. How handsome is the Crow, he exclaimed, in
the beauty of her shape and in the fairness of her feathers! If only her voice
were as sweet as her looks are fair, she ought without doubt to be the Queen of
Birds. The Crow, anxious to refute his doubts, set up a loud caw, and dropped
the cheese. The Fox quickly picked it up, and said: My good Crow, your voice is
right enough, but your wit is wanting.

A Hare one day ridiculed the short feet and slow pace of the Tortoise, who
replied, laughing: Though you be swift as the wind, I will beat you in a race.
The Hare, believing her assertion to be simply impossible, agreed to the
proposal; and they agreed that the Fox should choose the course and fix the
goal. On the day appointed for the race the two started together. The Tortoise
never for a moment stopped, but went on with a slow but steady pace straight to
the end of the course. The Hare, lying down by the wayside, fell fast asleep.
At last waking up, and moving as fast as he could, he saw the Tortoise had
reached the goal, and was comfortably dozing after her fatigue. Slow but steady
wins the race.
"""

# SAMPLE quiz questions for concept 03 (spec §5).
SAMPLE_Q03 = [
    {"id": "q01", "text": "softmax(z)_i is proportional to:",
     "options": {"a": "z_i", "b": "exp(z_i)", "c": "log(z_i)", "d": "1/z_i"}},
    {"id": "q02", "text": "Why subtract max(z) before exponentiating in softmax?",
     "options": {"a": "to speed it up", "b": "numerical stability (avoid overflow)",
                 "c": "it changes the result favourably", "d": "to normalise to 1"}},
    {"id": "q03", "text": "With one-hot label y and probs p=softmax(logits), the gradient of cross-entropy w.r.t. the logits is:",
     "options": {"a": "p", "b": "y - p", "c": "p - y", "d": "log(p) - y"}},
    {"id": "q04", "text": "Cross-entropy against a one-hot target reduces to:",
     "options": {"a": "the squared error between p and y",
                 "b": "the negative log-probability assigned to the correct class",
                 "c": "the entropy of the predicted distribution p",
                 "d": "the KL divergence from p to the uniform distribution"}},
    {"id": "q05", "text": "For a constant c, softmax(z + c) equals:",
     "options": {"a": "softmax(z), unchanged", "b": "softmax(z) + c",
                 "c": "c · softmax(z)", "d": "undefined"}},
]

ANSWERS_EXAMPLE = {"03": "q01=b;q02=b;q03=c;q04=b;q05=a"}


# --------------------------------------------------------------------------- #
# per-concept standalone numpy exercises (STUB starter + GENERATED failing test)
# --------------------------------------------------------------------------- #
EXERCISES = {
    "01": {
        "prompt": "Implement a single perceptron: `step_perceptron(x, w, b)` returns 1 "
                  "if w.x + b > 0 else 0. Make the AND-gate test pass.",
        "starter": '''# STUB
"""Concept 01 exercise - the perceptron. Flip line 1 to "# AUTHORED" to keep your work."""
import numpy as np


def step_perceptron(x, w, b):
    """Return 1 if (w . x) + b > 0 else 0."""
    # TODO: implement the perceptron decision rule.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import step_perceptron


def test_and_gate():
    w, b = np.array([1.0, 1.0]), -1.5
    truth = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
    for (a, c), y in truth.items():
        assert step_perceptron(np.array([a, c]), w, b) == y
''',
    },
    "02": {
        "prompt": "Implement the forward pass of a 2-layer ReLU network: "
                  "`mlp_forward(x, W1, b1, W2, b2)`. With the weights given in the test it "
                  "must compute XOR - proof that depth + nonlinearity beats a single linear unit.",
        "starter": '''# STUB
"""Concept 02 exercise - escaping linearity (XOR). Flip line 1 to "# AUTHORED"."""
import numpy as np


def mlp_forward(x, W1, b1, W2, b2):
    """Two layers with a ReLU in between: relu(W1 x + b1) -> W2 . h + b2.

    Return the scalar output of the second layer.
    """
    # TODO: implement the forward pass (use np.maximum for ReLU).
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import mlp_forward


def test_xor():
    W1 = np.array([[1.0, 1.0], [1.0, 1.0]])
    b1 = np.array([0.0, -1.0])
    W2 = np.array([1.0, -2.0])
    b2 = 0.0
    truth = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}
    for (a, c), y in truth.items():
        out = mlp_forward(np.array([a, c], dtype=float), W1, b1, W2, b2)
        assert round(float(out)) == y
''',
    },
    "03": {
        "prompt": "Implement `softmax(z)` (numerically stable). The test checks it sums to 1, "
                  "is uniform on equal logits, and preserves the argmax.",
        "starter": '''# STUB
"""Concept 03 exercise - softmax. Flip line 1 to "# AUTHORED"."""
import numpy as np


def softmax(z):
    """Return the softmax of a 1-D array z. Subtract max(z) for stability."""
    # TODO: implement a numerically stable softmax.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import softmax


def test_softmax_properties():
    p = softmax(np.array([0.0, 0.0]))
    assert np.allclose(p, [0.5, 0.5])
    p = softmax(np.array([2.0, 1.0, 0.1]))
    assert abs(float(p.sum()) - 1.0) < 1e-9
    assert int(np.argmax(p)) == 0
    # stable on large inputs (no overflow)
    assert np.all(np.isfinite(softmax(np.array([1000.0, 1000.0]))))
''',
    },
    "04": {
        "prompt": "Implement one MLP layer `mlp_layer(x, W, b)` returning relu(W x + b). "
                  "The test checks a known numeric result.",
        "starter": '''# STUB
"""Concept 04 exercise - an MLP layer. Flip line 1 to "# AUTHORED"."""
import numpy as np


def mlp_layer(x, W, b):
    """Return relu(W x + b)."""
    # TODO: implement an affine layer followed by ReLU.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import mlp_layer


def test_layer():
    W = np.array([[1.0, -1.0], [-1.0, -1.0]])
    b = np.array([0.0, 0.5])
    out = mlp_layer(np.array([2.0, 1.0]), W, b)
    # W x = [1, -3]; + b = [1, -2.5]; relu = [1, 0]
    assert np.allclose(out, [1.0, 0.0])
''',
    },
    "06": {
        "prompt": "Implement a single SGD update `sgd_step(params, grads, lr)` returning "
                  "params - lr * grads.",
        "starter": '''# STUB
"""Concept 06 exercise - the SGD step. Flip line 1 to "# AUTHORED"."""
import numpy as np


def sgd_step(params, grads, lr):
    """Return the updated parameters after one gradient-descent step."""
    # TODO: implement params - lr * grads.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import sgd_step


def test_sgd_step():
    p = np.array([1.0, 2.0, 3.0])
    g = np.array([0.5, 0.5, 0.5])
    out = sgd_step(p, g, lr=0.1)
    assert np.allclose(out, [0.95, 1.95, 2.95])
''',
    },
    "07": {
        "prompt": "Implement `embedding_lookup(ids, table)` returning the rows of `table` "
                  "selected by integer `ids`.",
        "starter": '''# STUB
"""Concept 07 exercise - embedding lookup. Flip line 1 to "# AUTHORED"."""
import numpy as np


def embedding_lookup(ids, table):
    """Return a (len(ids), d) array of the embedding rows for the given ids."""
    # TODO: implement the lookup (an embedding is just indexing into a table).
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import embedding_lookup


def test_lookup():
    table = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    out = embedding_lookup([2, 0, 1], table)
    assert np.allclose(out, [[2.0, 2.0], [0.0, 0.0], [1.0, 1.0]])
''',
    },
    "08": {
        "prompt": "Implement `scaled_dot_product_attention(Q, K, V)` = "
                  "softmax(Q Kᵀ / sqrt(d)) V. The test checks shape and a single-key average.",
        "starter": '''# STUB
"""Concept 08 exercise - scaled dot-product attention. Flip line 1 to "# AUTHORED"."""
import numpy as np


def scaled_dot_product_attention(Q, K, V):
    """Return softmax(Q K^T / sqrt(d_k)) @ V (no masking)."""
    # TODO: implement scaled dot-product attention.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import scaled_dot_product_attention


def test_attention():
    Q = np.array([[1.0, 0.0], [0.0, 1.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    out = scaled_dot_product_attention(Q, K, V)
    assert out.shape == (2, 2)
    # identical queries/keys -> rows are convex combinations of V rows
    assert np.all(out >= V.min() - 1e-9) and np.all(out <= V.max() + 1e-9)
''',
    },
    "09": {
        "prompt": "Implement `apply_causal_mask(scores)` that sets scores[i, j] = -inf for "
                  "j > i, so a position never attends to the future.",
        "starter": '''# STUB
"""Concept 09 exercise - causal masking. Flip line 1 to "# AUTHORED"."""
import numpy as np


def apply_causal_mask(scores):
    """Return scores with the strict upper triangle (j > i) set to -inf."""
    # TODO: build a causal mask and apply it.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import apply_causal_mask


def test_mask():
    s = np.ones((3, 3))
    m = apply_causal_mask(s)
    assert m[0, 1] == float("-inf") and m[0, 2] == float("-inf")
    assert m[1, 2] == float("-inf")
    assert m[2, 0] == 1.0 and m[1, 1] == 1.0
''',
    },
    "11": {
        "prompt": "Implement `sinusoidal_encoding(seq_len, d_model)` from Vaswani et al. "
                  "The test checks the (seq_len, d_model) shape and the [-1, 1] range.",
        "starter": '''# STUB
"""Concept 11 exercise - sinusoidal positional encoding. Flip line 1 to "# AUTHORED"."""
import numpy as np


def sinusoidal_encoding(seq_len, d_model):
    """Return a (seq_len, d_model) array of sinusoidal positional encodings."""
    # TODO: even dims use sin, odd dims use cos, with the 1/10000^(2i/d) frequency.
    raise NotImplementedError
''',
        "test": '''# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import sinusoidal_encoding


def test_encoding():
    pe = sinusoidal_encoding(5, 8)
    assert pe.shape == (5, 8)
    assert np.all(pe >= -1.0 - 1e-9) and np.all(pe <= 1.0 + 1e-9)
''',
    },
}


# --------------------------------------------------------------------------- #
# templated text bodies
# --------------------------------------------------------------------------- #
MODULE_TEX_TMPL = r"""% STUB
% AUTHOR: write the concept explanation below. Flip line 1 to "% AUTHORED" once
% you start, so scaffold.py never regenerates over your prose.
\section{__TITLE__}\label{sec:__NN__}
\conceptbadge{__NN__}

% AUTHOR: load-bearing math and the standalone-exercise reference belong here.
"""


def concept_readme(c):
    sources = "\n".join(f"- {s}" for s in c["sources"]) or "- (none)"
    ms = ", ".join(c["milestones"]) if c["milestones"] else "none (concept-only)"
    quiz_note = (
        "Open `quiz/index.html` in a browser, answer every question, enter your "
        "handle, copy the `handle:shard` line, and commit it to "
        f"`progress/{c['id']}.key`."
        if c["quiz"] else
        "This concept has no quiz (no shard to earn)."
    )
    ex_note = (
        "This concept has a standalone numpy exercise - see `exercise/`."
        if c["exercise"] else
        "This concept has no standalone exercise."
    )
    return f"""<!-- STUB -->
# Concept {c['id']} - {c['title']}

> STUB: author fills the prose. Flip the first line to `<!-- AUTHORED -->` once
> you start writing, so scaffold.py never regenerates over your work.

## Learning objectives

- TODO: author writes 3-5 objectives for this concept.

## Maps to project milestone(s)

{ms}

## Standalone exercise

{ex_note}

## Quiz

{quiz_note}

## Sources

{sources}
"""


def exercise_readme(c, prompt):
    return f"""<!-- STUB -->
# Exercise - Concept {c['id']} ({c['title']})

> STUB: this is a self-contained numpy drill. There is NO solution in the repo.
> Implement `starter.py` until `python -m pytest test_exercise.py` passes, then
> flip the first line of `starter.py` to `# AUTHORED` to protect your work.

## Task

{prompt}

## Run the test

```
cd concepts/{c['id']}-{c['slug']}/exercise
python -m pytest test_exercise.py
```
"""


def render_concept_table():
    rows = ["| ID | Title | Quiz | Exercise | Prereqs | Milestones |",
            "|----|-------|------|----------|---------|------------|"]
    for c in CONCEPTS:
        rows.append(
            f"| {c['id']} | {c['title']} | {'yes' if c['quiz'] else 'no'} | "
            f"{'yes' if c['exercise'] else 'no'} | "
            f"{', '.join(c['prereq']) or '-'} | "
            f"{', '.join(c['milestones']) or '-'} |"
        )
    return "\n".join(rows)


def render_milestone_table():
    rows = ["| ID | Title | Depends on | Uses concepts | Implemented? |",
            "|----|-------|-----------|----------------|--------------|"]
    for m in MILESTONES:
        rows.append(
            f"| {m['id']} | {m['title']} | {', '.join(m['depends_on']) or '-'} | "
            f"{', '.join(m['uses']) or '-'} | "
            f"{'**yes (plumbing)**' if m['implement'] else 'no (learner)'} |"
        )
    return "\n".join(rows)


def root_readme():
    course = MANIFEST["course"]
    return f"""<!-- GENERATED -->
# {course['title']}

A self-paced course that walks you from a single perceptron all the way to a
**{course['endpoint']}**, built from scratch. No CNNs, no RNNs, no diffusion,
no pretrained weights - just the line from linear units to a working GPT.

## Quick start

```
python3 serve.py
```

That serves the whole repo and opens a **course hub** in your browser with a
one-click link to every quiz. (Quizzes load their questions with `fetch`, which
browsers block over `file://`, so opening the `.html` directly just hangs on
"Loading..." - always go through `serve.py`.) Stop it with Ctrl-C.

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

1. Run `python3 serve.py` and click a quiz on the hub (or open
   `http://127.0.0.1:8000/concepts/NN-slug/quiz/`).
2. Answer every question and enter your **handle**.
3. Click **Get my shard** and copy the `handle:shard` line it produces.
4. Paste that line into the **Submit a shard** box on the hub. It checks your
   answers locally; if they are correct it saves `progress/NN.key` and rebuilds
   your course PDF (`tex/main.pdf`) on the spot. If they are wrong it tells you,
   and nothing is recorded.

Your shard is HMAC-bound to your handle, so pasting someone else's line records
progress under *their* handle, not yours.

A module can be verified only once its quiz has an answer key (see
`ci/answers.example.json`). The bundled key covers the authored modules; an
unauthored quiz cannot be checked and will not count.

## Doing the coding exercises

Exercises are disposable practice for the concept. They do **not** become part of
the project and are **not** submitted, but the same operations reappear in a
milestone later, so write them cleanly.

1. `cd concepts/NN-slug/exercise` and read its `README.md`.
2. Implement the functions in `starter.py` - **numpy only**; the point is to
   write them yourself, so don't import a library version.
3. Run the tests:
   ```
   python3 -m pytest test_exercise.py     # or, with no pytest installed:
   python3 test_exercise.py               # stdlib fallback, same checks
   ```
4. Iterate until every test passes. There is no solution in the repo - by design.

## The project track (build the GPT)

`project/` is one package, `dlgpt/`, grown across ten milestones:

- **P0 is already implemented** - the plumbing (char tokenizer, batching, a
  passing test). Everything after it is yours.
- **P1-P9 ship as failing tests** in `project/tests/` that encode each spec. Make
  them pass **in order**, building on what came before, until P9 generates text.

```
python3 -m pytest project/tests          # P0 passes; P1..P9 fail until you build them
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

{render_concept_table()}

## Project milestones

{render_milestone_table()}

Only **P0** ships implemented. **You implement P1-P9** by making their tests pass
in order (see "The project track" above).

## Where your progress lives

There is no website to log into. The course **PDF is the dashboard**: each time
you submit a correct key on the hub, `serve.py` regenerates `tex/progress.tex`
and rebuilds `tex/main.pdf` locally. Open `tex/main.pdf` to see your completed
modules under your handle. (No TeX Live installed? Your keys are still saved;
the PDF rebuild is simply skipped until you install it.)

## Prerequisites

- Python 3.10+ (standard library only - no `pip install`).
- `numpy` for the coding exercises; `pytest` is optional (each exercise's test
  file has a stdlib fallback: `python3 test_exercise.py`).
- A browser (the quizzes are static vanilla HTML/CSS/JS - no Node required).
- TeX Live (`latexmk` or `pdflatex`) **if you want the PDF dashboard** rebuilt
  locally. Optional - progress is recorded with or without it.

## Troubleshooting

- **Quiz stuck on "Loading..."** - you opened it as a `file://` path. Start
  `python3 serve.py` and reach it through the hub instead.
- **"Those answers are not all correct"** - the shard did not match the answer
  key; re-take the quiz. (Only modules with an authored answer key can be
  verified.)
- **"No answer key for module NN yet"** - that quiz is not authored yet, so it
  cannot be checked or counted.
- **PDF did not rebuild** - install TeX Live (`latexmk`/`pdflatex`); your keys
  are saved regardless. On a LaTeX error, see `tex/main.log`.
- **`No module named pytest`** - run the test directly:
  `python3 test_exercise.py` (built-in stdlib fallback).
- **Port 8000 already in use** - `python3 serve.py --port 9000` (it also
  auto-picks the next free port).

## For instructors / hosted setups

The local flow above is fully self-contained. If you instead want a shared,
server-graded deployment (students push keys; a runner validates and publishes
one central PDF), that pipeline still ships in `ci/` - see `ci/SERVER_SETUP.md`.
Never commit the real answer key (`ci/answers.json`).
"""


def project_readme():
    return f"""<!-- GENERATED -->
# Project track - build a decoder-only GPT

One cumulative package, `dlgpt/`, grown across ten milestones. Each milestone
adds a layer to the same codebase; later milestones depend on earlier ones.

## Roadmap

{render_milestone_table()}

## Cumulative-build philosophy

You are not writing ten throwaway scripts - you are growing **one** package.
P0 hands you the plumbing (tokenizer, batching, a passing test). From P1 on,
every milestone has a failing test in `tests/` that encodes its spec; you make
it pass, building on everything before it, until P9 is a working GPT that
generates text.

## Running the tests

```
python -m pytest project/tests
```

`test_p0_data.py` passes today (P0 is real). `test_p1.py` ... `test_p9.py`
**fail by design** - they are your specifications. Make them pass in order.

## What is implemented vs. yours

- **Implemented:** P0 only - `dlgpt/data.py`, `corpus/tiny.txt`, `tests/test_p0_data.py`.
- **Yours (P1-P9):** `dlgpt/autograd.py`, `dlgpt/nn.py`, `dlgpt/attention.py`,
  `dlgpt/model.py`. Each ships as a stub that raises `NotImplementedError`.
  When you start a file, flip its first line to `# AUTHORED` so re-running
  `scaffold.py` never clobbers your work.
"""


SERVER_SETUP_MD = r"""<!-- GENERATED -->
# Deploying the dlgpt CI runner

The runner is **stateless**: the source of truth is the set of committed
`progress/NN.key` files. Every run recomputes everything from scratch and
publishes. It never pushes to git and needs no database, no inbound ports, and
no server software beyond Python and TeX Live.

## 1. Clone the repo (read-only is enough)

```
git clone <repo-url> /opt/dlgpt
```

A **read-only deploy key** suffices - the runner only `git pull`s; it never
pushes. Generated artifacts (`tex/progress.tex`, `tex/main.pdf`, aux files) are
gitignored and regenerated every run.

## 2. Create the server-side answer key

The real answer key is **never** in the repo. Copy the template and fill it in
as quizzes are authored:

```
cp ci/answers.example.json ci/answers.json
$EDITOR ci/answers.json     # {"03": "q01=b;q02=b;q03=c", ...}
```

`ci/answers.json` is gitignored - keep it that way.

## 3. Dependencies

- **Python:** standard library only. `pip install` nothing.
- **TeX Live:** ensure `latexmk` and `pdflatex` are on `PATH`.

## 4. Configure publishing

```
cp ci/publish.sh.example ci/publish.sh
$EDITOR ci/publish.sh       # fill in Nextcloud URL + app password
```

Use a Nextcloud **app password**, not the account login. `ci/publish.sh` is
gitignored so credentials never reach git.

## 5. Schedule the runner (every 5 minutes)

### Option A - cron

```
*/5 * * * * cd /opt/dlgpt && /usr/bin/python3 ci/runner.py >> /var/log/dlgpt-ci.log 2>&1
```

### Option B - systemd

`/etc/systemd/system/dlgpt-ci.service`:

```ini
[Unit]
Description=dlgpt course CI runner (validate + build + publish)

[Service]
Type=oneshot
WorkingDirectory=/opt/dlgpt
ExecStart=/usr/bin/python3 ci/runner.py
```

`/etc/systemd/system/dlgpt-ci.timer`:

```ini
[Unit]
Description=Run dlgpt-ci every 5 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

Enable it:

```
systemctl daemon-reload
systemctl enable --now dlgpt-ci.timer
```

## 6. Operating notes

- Expect ~5 minutes of latency between a learner's commit and the PDF update.
- A manual run is just `python3 ci/runner.py`.
- To validate without building, run `python3 ci/validate.py ci/answers.json`.

## Why not Jenkins or GitHub Actions

The pipeline must run on department-owned hardware with minimal setup. A stdlib
Python script on a timer needs no server software, no plugins, and no inbound
network ports - it *pulls*, it does not receive webhooks, which sidesteps
departmental firewall/NAT issues entirely. Jenkins can later wrap this same
script if a dashboard is ever wanted.
"""


def main_tex():
    inputs = []
    for c in CONCEPTS:
        if c["id"] == "00":
            continue  # prerequisites: no \section in the build (matches spec main.tex)
        inputs.append(f"\\input{{../concepts/{c['id']}-{c['slug']}/module.tex}}")
    body = "\n".join(inputs)
    return (
        "% GENERATED\n"
        "\\documentclass[11pt]{article}\n"
        "\\usepackage{preamble}\n"
        "\\IfFileExists{progress.tex}{\\input{progress.tex}}{}  % generated by CI; absent on fresh clone\n"
        "\\title{From Perceptron to GPT: Deep Learning From Scratch}\n"
        "\\author{}\n"
        "\\date{\\today}\n"
        "\\begin{document}\n"
        "\\maketitle\n"
        "\\section*{Progress}\n"
        "\\progressdashboard\n"
        "\\tableofcontents\n"
        "% --- concept modules, in manifest order ---\n"
        f"{body}\n"
        "\\end{document}\n"
    )


# --------------------------------------------------------------------------- #
# questions.json (salt-preserving)
# --------------------------------------------------------------------------- #
def build_questions(c):
    path = ROOT / "concepts" / f"{c['id']}-{c['slug']}" / "quiz" / "questions.json"
    salt = None
    if path.exists():
        try:
            existing = json.loads(path.read_text())
            salt = existing["salt"]
            # JSON cannot carry an "AUTHORED" first line, so the author marks a
            # hand-written quiz with "authored": true. Honour it: return the file
            # verbatim so write() treats it as unchanged and never regenerates
            # over authored questions.
            if existing.get("authored"):
                return path, path.read_text()
        except Exception:
            salt = None
    if not salt or salt == "GENERATE_16_RANDOM_HEX_BYTES":
        salt = secrets.token_hex(16)
    data = {
        "module_id": c["id"],
        "salt": salt,
        "course_prefix": KEY_PREFIX,
        "title": c["title"],
        "questions": SAMPLE_Q03 if c["id"] == "03" else [],
    }
    return path, json.dumps(data, indent=2) + "\n"


# --------------------------------------------------------------------------- #
# build everything
# --------------------------------------------------------------------------- #
def main():
    # manifest + root files
    write(ROOT / "course.manifest.json", json.dumps(MANIFEST, indent=2) + "\n")
    write(ROOT / ".gitignore", GITIGNORE)
    write(ROOT / "README.md", root_readme())

    # concepts
    for c in CONCEPTS:
        cdir = ROOT / "concepts" / f"{c['id']}-{c['slug']}"
        write(cdir / "README.md", concept_readme(c))
        write(cdir / "module.tex",
              MODULE_TEX_TMPL.replace("__TITLE__", c["title"]).replace("__NN__", c["id"]))
        if c["quiz"]:
            qdir = cdir / "quiz"
            write(qdir / "index.html", QUIZ_HTML)
            write(qdir / "quiz.js", QUIZ_JS)
            write(qdir / "style.css", QUIZ_CSS)
            qpath, qcontent = build_questions(c)
            write(qpath, qcontent)
        if c["exercise"]:
            edir = cdir / "exercise"
            ex = EXERCISES[c["id"]]
            write(edir / "README.md", exercise_readme(c, ex["prompt"]))
            write(edir / "starter.py", ex["starter"])
            write(edir / "test_exercise.py", ex["test"])

    # tex
    write(ROOT / "tex" / "preamble.sty", PREAMBLE_STY)
    write(ROOT / "tex" / "main.tex", main_tex())

    # project
    pdir = ROOT / "project"
    write(pdir / "README.md", project_readme())
    write(pdir / "conftest.py", CONFTEST_PY)
    write(pdir / "dlgpt" / "__init__.py", INIT_PY)
    write(pdir / "dlgpt" / "data.py", DATA_PY)
    write(pdir / "dlgpt" / "autograd.py", AUTOGRAD_PY)
    write(pdir / "dlgpt" / "nn.py", NN_PY)
    write(pdir / "dlgpt" / "attention.py", ATTENTION_PY)
    write(pdir / "dlgpt" / "model.py", MODEL_PY)
    write(pdir / "corpus" / "tiny.txt", TINY_TXT)
    write(pdir / "tests" / "test_p0_data.py", TEST_P0)
    write(pdir / "tests" / "test_p1.py", TEST_P1)
    write(pdir / "tests" / "test_p2.py", TEST_P2)
    write(pdir / "tests" / "test_p4.py", TEST_P4)
    write(pdir / "tests" / "test_p5.py", TEST_P5)
    write(pdir / "tests" / "test_p6.py", TEST_P6)
    write(pdir / "tests" / "test_p7.py", TEST_P7)
    write(pdir / "tests" / "test_p8.py", TEST_P8)
    write(pdir / "tests" / "test_p9.py", TEST_P9)
    # P3 has no new module file (embeddings live in nn/model); spec test still needed.
    write(pdir / "tests" / "test_p3.py", '''# GENERATED — failing spec for milestone P3.
from dlgpt import nn


def test_embedding_table_exists():
    # P3: a trainable embedding lookup built on your P2 primitives.
    emb = nn.Linear(8, 4)          # placeholder API the learner may replace
    out = emb([0.0] * 8)
    assert len(out) == 4
''')

    # progress
    touch(ROOT / "progress" / ".gitkeep")

    # ci
    cidir = ROOT / "ci"
    write(cidir / "validate.py", VALIDATE_PY)
    write(cidir / "runner.py", RUNNER_PY)
    write(cidir / "build.sh", BUILD_SH)
    write(cidir / "answers.example.json", json.dumps(ANSWERS_EXAMPLE, indent=2) + "\n")
    write(cidir / "publish.sh.example", PUBLISH_EXAMPLE)
    write(cidir / "SERVER_SETUP.md", SERVER_SETUP_MD)

    # make shell scripts executable
    for sh_path in [cidir / "build.sh", cidir / "publish.sh.example"]:
        if sh_path.exists():
            sh_path.chmod(0o755)

    # report
    print(f"written:          {len(STATS['written'])}")
    print(f"unchanged:        {len(STATS['unchanged'])}")
    print(f"authored-skipped: {len(STATS['authored_skipped'])}")
    if STATS["authored_skipped"]:
        for p in STATS["authored_skipped"]:
            print(f"  kept authored: {p}")


if __name__ == "__main__":
    main()
