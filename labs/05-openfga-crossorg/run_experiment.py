"""Load and check the synthetic DPP model against a local OpenFGA API."""
import json
from pathlib import Path
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

BASE = "http://localhost:8080"
ROOT = Path(__file__).resolve().parent


def request(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode() or "{}")


for attempt in range(20):
    try:
        with urlopen(BASE + "/healthz", timeout=5) as response:
            if response.status >= 400:
                raise URLError(f"health check returned {response.status}")
        break
    except URLError:
        if attempt == 19:
            raise SystemExit("OpenFGA is unavailable; run docker compose up -d first")
        time.sleep(1)

store = request("POST", "/stores", {"name": "agentic-ac-course"})
store_id = store["id"]
model = json.loads((ROOT / "model.json").read_text(encoding="utf-8"))
model_id = request("POST", f"/stores/{store_id}/authorization-models", model)["authorization_model_id"]
tuples = json.loads((ROOT / "tuples.json").read_text(encoding="utf-8"))
request("POST", f"/stores/{store_id}/write", tuples)

results = []
for case in json.loads((ROOT / "cases.json").read_text(encoding="utf-8")):
    payload = {key: case[key] for key in ("user", "relation", "object")}
    payload["authorization_model_id"] = model_id
    allowed = request("POST", f"/stores/{store_id}/check", payload)["allowed"]
    results.append({**case, "actual": allowed, "pass": allowed == case["expected"]})

print(json.dumps({"store_id": store_id, "model_id": model_id, "results": results}, indent=2))
if not all(item["pass"] for item in results):
    raise SystemExit("One or more authorization decisions did not match ground truth")
