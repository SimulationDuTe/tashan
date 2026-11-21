"""Aggregate iteration-6 two-turn blind judgments (5 dims + interrogation).

Usage:
    python evals/analyze_twoturn.py iteration-6
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "pilot"
DIMS = ["D1", "D2", "D3", "D4", "D5"]
ALL_DIMS = DIMS + ["interrogation"]


def main() -> None:
    base = ROOT / sys.argv[1]
    judgment = base / "judgment"
    mapping = json.loads((judgment / "map.json").read_text(encoding="utf-8"))
    judges = [
        json.loads((judgment / f"judge-{i}.json").read_text(encoding="utf-8-sig"))
        for i in (1, 2)
    ]

    rows = []
    votes: dict[str, int] = {}
    totals5: dict[str, list[int]] = {}
    totals6: dict[str, list[int]] = {}
    for task in sorted(mapping):
        per_arm: dict[str, dict[str, list[int]]] = {}
        task_votes = []
        for judge in judges:
            entry = judge["tasks"][task]
            for label in ("A", "B"):
                arm = mapping[task][label]
                scored = entry[label]["scores"]
                per_arm.setdefault(arm, {"five": [], "six": []})
                per_arm[arm]["five"].append(sum(scored[d] for d in DIMS))
                per_arm[arm]["six"].append(sum(scored[d] for d in ALL_DIMS))
                totals5.setdefault(arm, []).append(sum(scored[d] for d in DIMS))
                totals6.setdefault(arm, []).append(sum(scored[d] for d in ALL_DIMS))
            winner = entry["winner"]
            arm = "tie" if winner == "tie" else mapping[task][winner]
            task_votes.append(arm)
            votes[arm] = votes.get(arm, 0) + 1
        rows.append(
            {
                "task": task,
                "votes": task_votes,
                "five": {a: v["five"] for a, v in per_arm.items()},
                "six": {a: v["six"] for a, v in per_arm.items()},
            }
        )

    def mean(vals: list[int]) -> float:
        return round(sum(vals) / len(vals), 3)

    arms = sorted(totals5)
    result = {
        "tasks": rows,
        "votes": votes,
        "means5": {a: mean(totals5[a]) for a in arms},
        "means6": {a: mean(totals6[a]) for a in arms},
        "samples5": {a: len(totals5[a]) for a in arms},
        "delta5": round(mean(totals5[arms[0]]) - mean(totals5[arms[1]]), 3) if len(arms) == 2 else None,
        "delta6": round(mean(totals6[arms[0]]) - mean(totals6[arms[1]]), 3) if len(arms) == 2 else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    (base / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
