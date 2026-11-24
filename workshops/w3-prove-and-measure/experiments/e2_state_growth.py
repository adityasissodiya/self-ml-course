"""E3.2  How the cost of deciding safety grows with the number of agents.

Exhaustive search visits every reachable state, and the number of states
grows exponentially with the agents involved. For the monotone fragment
(no revocation) the closure algorithm decides P1 and P3 with a number of
rule checks that grows only quadratically. P2 is about revocation, so it
still needs search.

Outputs: results/growth_table.tex, results/growth_plot.tex, results/growth.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.report import Results, tabular  # noqa: E402
from agentsim.safety import RULESETS, closure, default_system, explore  # noqa: E402

R0, R2 = RULESETS[0], RULESETS[2]
MAX_N, MAX_N_R0 = 10, 5


def coords(points) -> str:
    return " ".join(f"({n},{v})" for n, v in points)


def main() -> None:
    rows = []
    for n in range(1, MAX_N + 1):
        system = default_system(n)
        e2 = explore(system, R2)
        _, ops = closure(system, R2)
        r0 = explore(system, R0).states if n <= MAX_N_R0 else None
        rows.append({"n": n, "r0_states": r0, "r2_states": e2.states, "r2_transitions": e2.transitions,
                     "closure_checks": ops})
        print(f"n={n:2}  R0 states={r0 if r0 is not None else '-':>6}  R2 states={e2.states:5}  "
              f"R2 transitions={e2.transitions:6}  closure checks={ops:4}")

    plot = "\n".join([
        r"\begin{tikzpicture}",
        r"\begin{semilogyaxis}[width=0.62\textwidth, height=0.5\textheight, xlabel={agents besides Alice},",
        r"  ylabel={count (log scale)}, legend pos=north west, legend style={font=\tiny},",
        r"  tick label style={font=\tiny}, label style={font=\scriptsize}, grid=major, grid style={line width=.1pt}]",
        rf"\addplot+[mark=*] coordinates {{{coords((r['n'], r['r0_states']) for r in rows if r['r0_states'])}}};",
        r"\addlegendentry{states searched, R0}",
        rf"\addplot+[mark=square*] coordinates {{{coords((r['n'], r['r2_states']) for r in rows)}}};",
        r"\addlegendentry{states searched, R2}",
        rf"\addplot+[mark=triangle*] coordinates {{{coords((r['n'], r['closure_checks']) for r in rows)}}};",
        r"\addlegendentry{rule checks, closure (R2)}",
        r"\end{semilogyaxis}",
        r"\end{tikzpicture}",
    ]) + "\n"

    out = Results(__file__)
    out.json("growth", rows)
    out.tex("growth_plot", plot)
    out.tex("growth_table", tabular(
        ["Agents", "R0 states", "R2 states", "R2 transitions", "Closure checks"],
        [[r["n"], r["r0_states"] if r["r0_states"] is not None else "--", r["r2_states"], r["r2_transitions"],
          r["closure_checks"]] for r in rows if r["n"] in (1, 2, 3, 5, 8, 10)],
        "r r r r r"))


if __name__ == "__main__":
    main()
