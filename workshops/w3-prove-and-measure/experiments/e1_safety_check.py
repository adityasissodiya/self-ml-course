"""E3.1  Check three safety properties of four delegation rule sets.

The instance: Alice (recycler), an orchestrator (recycler), the XRF agent
(lab), and a broker agent. The data owner consents to Alice using
``materials`` within the recycler and the lab. Exhaustive breadth-first
search over all reachable states decides each property for this instance and
returns the shortest counterexample. The closure column checks that the
polynomial fixpoint method agrees on the properties it can decide.

Outputs: results/safety_rules.tex, results/safety_traces.tex, results/safety.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.report import Raw, Results, mark, tabular, verbatim_lines  # noqa: E402
from agentsim.safety import PROPERTIES, RULESETS, closure_verdicts, default_system, explore  # noqa: E402

SHOWCASE = (("R0", "P1"), ("R1", "P2"), ("R2", "P3"))  # weakest rule set that violates each property


def main() -> None:
    system = default_system(3)
    print("principals:", system.principals)
    print("consent:", system.consent, "\n")
    data, rows = {}, []
    for rules in RULESETS:
        e = explore(system, rules)
        cl = closure_verdicts(system, rules)
        agrees = all(cl[k] == (e.counterexamples[k] is None) for k in cl)
        data[rules.key] = {"label": rules.label, "states": e.states, "transitions": e.transitions,
                           "counterexamples": e.counterexamples, "closure": cl, "closure_agrees": agrees}
        verdicts = {k: e.counterexamples[k] is None for k in PROPERTIES}
        print(f"{rules.key} {rules.label:38} states={e.states:4} transitions={e.transitions:5} "
              + " ".join(f"{k}={'holds' if v else 'VIOLATED'}" for k, v in verdicts.items())
              + f" closure agrees={agrees}")
        rows.append([rules.key, rules.label, e.states, *(mark(verdicts[k]) for k in PROPERTIES), mark(agrees)])

    lines = []
    for rkey, pkey in SHOWCASE:
        trace = data[rkey]["counterexamples"][pkey]
        lines.append(f"{pkey} ({PROPERTIES[pkey][0]}) fails under {rkey}:")
        lines += [f"  {i}. {step}" for i, step in enumerate(trace, 1)]
    print("\n" + "\n".join(lines))

    out = Results(__file__)
    out.json("safety", data)
    out.tex("safety_rules", tabular(
        ["", "Rule set", "States", Raw(r"\textbf{P1}"), Raw(r"\textbf{P2}"), Raw(r"\textbf{P3}"), "Closure agrees"],
        rows, "l p{5cm} r c c c c"))
    out.tex("safety_traces", verbatim_lines(lines))


if __name__ == "__main__":
    main()
