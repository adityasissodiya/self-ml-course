"""E3.3  Benchmark four enforcement designs on ground-truth delegation cases.

    B0  token passthrough: signature and expiry only, coarse scopes
    B1  OAuth best practice: audience (RFC 8707) and scope checks, RFC 8693 delegation
    B2  B1 + introspection, workload binding, ReBAC check on the acting agent
    B3  hybrid: ReBAC on the human principal at decision time, attenuated
        capability, cascading cross-organization revocation

Ground truth is defined in agentsim/bench.py. Costs are simulated from the
assumed per-operation latencies in agentsim/runtime.py, not measured.

Hands-on: ``python e3_benchmark.py --cases my_cases.json`` adds your cases.
Outputs: results/bench_metrics.tex, results/bench_matrix.tex, results/benchmark.json
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.bench import load_cases, metrics, run_suite  # noqa: E402
from agentsim.report import Results, mark, tabular  # noqa: E402
from agentsim.world import CONFIGS  # noqa: E402

HERE = Path(__file__).resolve().parent


def pct(x) -> str:
    return "--" if x is None else f"{round(100 * x)}%"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases", type=Path, action="append", default=[], help="extra case file(s)")
    args = parser.parse_args()
    cases = load_cases(HERE / "cases.json", *args.cases)
    results = run_suite(cases)
    m = metrics(cases, results)

    print(f"{len(cases)} cases x {len(CONFIGS)} configurations\n")
    header = f"{'case':22} {'category':16} {'expect':6} " + " ".join(f"{c.key:>4}" for c in CONFIGS)
    print(header + "\n" + "-" * len(header))
    matrix = []
    for c in cases:
        ok = {cfg.key: all(a["allowed"] == (c["expected"] == "allow") for a in results[cfg.key][c["id"]])
              for cfg in CONFIGS}
        matrix.append((c, ok))
        print(f"{c['id']:22} {c['category']:16} {c['expected']:6} "
              + " ".join(f"{'ok' if ok[k] else 'XX':>4}" for k in ok))
    print()
    for key, v in m.items():
        print(f"{key} {v['label']:42} unauthorized-allow={pct(v['unauthorized_allow']):>4} "
              f"false-deny={pct(v['false_deny']):>4} deputy-resistance={pct(v['deputy_resistance']):>4} "
              f"revocation-exposure={v['revocation_exposure']} over-privilege={v['over_privilege']} "
              f"cost={v['mean_cost_ms']}ms correct={v['cases_correct']}/{len(cases)}")

    if args.cases:
        print("\nExtra cases supplied: results/ not updated, so the slides keep the reference suite.")
        return
    out = Results(__file__)
    out.json("benchmark", {"cases": cases, "results": results, "metrics": m})
    out.tex("bench_metrics", tabular(
        ["", "Design", "Unauthorized allowed", "False denies", "Injection contained", "Calls after revocation",
         "Excess authority", "Cost (ms)", "Cases right"],
        [[k, v["label"], pct(v["unauthorized_allow"]), pct(v["false_deny"]), pct(v["deputy_resistance"]),
          v["revocation_exposure"], v["over_privilege"], v["mean_cost_ms"], f"{v['cases_correct']}/{len(cases)}"]
         for k, v in m.items()],
        "l p{3.3cm} p{1.3cm} p{0.9cm} p{1.2cm} p{1.3cm} p{1.1cm} r r", size=r"\tiny"))
    out.tex("bench_matrix", tabular(
        ["Case", "Category", "Expected", *(c.key for c in CONFIGS)],
        [[c["id"], c["category"], c["expected"], *(mark(ok[cfg.key]) for cfg in CONFIGS)] for c, ok in matrix],
        "l l l c c c c", size=r"\tiny"))


if __name__ == "__main__":
    main()
