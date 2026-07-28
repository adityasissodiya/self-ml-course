"""Validate committed shards against the server-side answer key."""
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
