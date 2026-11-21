"""Aggregate one iteration's blind judgments.

Usage:
    python evals/analyze_packet.py iteration-3
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "pilot"
DIMS = ["D1", "D2", "D3", "D4", "D5"]


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
    totals: dict[str, list[int]] = {}
    for task in sorted(mapping):
        scores: dict[str, list[int]] = {}
        task_votes = []
        for judge in judges:
            entry = next(t for t in judge["tasks"] if t["task"] == task)
            for label in ("A", "B"):
                arm = mapping[task][label]
                scores.setdefault(arm, []).append(sum(entry[label][d] for d in DIMS))
            winner = entry["winner"]
            arm = "tie" if winner == "tie" else mapping[task][winner]
            task_votes.append(arm)
            votes[arm] = votes.get(arm, 0) + 1
        for arm, vals in scores.items():
            totals.setdefault(arm, []).extend(vals)
        rows.append({"task": task, "scores": scores, "votes": task_votes})

    result = {
        "tasks": rows,
        "votes": votes,
        "means": {arm: round(sum(v) / len(v), 3) for arm, v in totals.items()},
        "judge_scores": totals,
    }
    arms = sorted(result["means"])
    if len(arms) == 2:
        result["delta"] = round(result["means"][arms[0]] - result["means"][arms[1]], 3)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    (base / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
