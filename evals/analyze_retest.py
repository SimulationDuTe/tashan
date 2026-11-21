"""Aggregate the iteration-2 retest (patched skill vs round-1 baseline)."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent / "pilot" / "iteration-2"
JUDGMENT = BASE / "judgment"
DIMS = ["D1", "D2", "D3", "D4", "D5"]

mapping = json.loads((JUDGMENT / "map.json").read_text(encoding="utf-8"))
judges = [
    json.loads((JUDGMENT / f"judge-{i}.json").read_text(encoding="utf-8-sig"))
    for i in (1, 2)
]

rows = []
votes = {"with_skill": 0, "without_skill": 0, "tie": 0}
totals = {"with_skill": [], "without_skill": []}

tasks = sorted(mapping)
for task in tasks:
    scores = {"with_skill": [], "without_skill": []}
    task_votes = []
    for judge in judges:
        entry = next(t for t in judge["tasks"] if t["task"] == task)
        for label in ("A", "B"):
            arm = mapping[task][label]
            s = sum(entry[label][d] for d in DIMS)
            scores[arm].append(s)
        winner = entry["winner"]
        arm = "tie" if winner == "tie" else mapping[task][winner]
        task_votes.append(arm)
        votes[arm] += 1
    for arm in scores:
        totals[arm].extend(scores[arm])
    rows.append(
        {
            "task": task,
            "with_skill": scores["with_skill"],
            "without_skill": scores["without_skill"],
            "votes": task_votes,
        }
    )

result = {
    "tasks": rows,
    "votes": votes,
    "with_mean": round(sum(totals["with_skill"]) / len(totals["with_skill"]), 3),
    "base_mean": round(sum(totals["without_skill"]) / len(totals["without_skill"]), 3),
    "judge_scores": totals,
}
result["delta"] = round(result["with_mean"] - result["base_mean"], 3)
print(json.dumps(result, ensure_ascii=False, indent=2))
(BASE / "results.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
