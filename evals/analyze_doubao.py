"""Merge the two blind judges of the Doubao run into A/B results.

Usage: python evals/analyze_doubao.py
Writes evals/pilot/iteration-8/results.json and prints a markdown summary.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITER = ROOT / "pilot" / "iteration-8"
TASKS = ["t1", "t2", "t3", "t4"]


def load(name: str, subdir: str = "judgment") -> dict:
    path = ITER / subdir / name if subdir else ITER / name
    return json.loads(path.read_text(encoding="utf-8-sig"))


def unblind(judgment: dict, mapping: dict) -> dict:
    out = {}
    for task in TASKS:
        row = judgment[task]
        arm_of = mapping[task]
        totals = {"A": 0, "B": 0}
        for label in ("jia", "yi"):
            arm = arm_of["甲" if label == "jia" else "乙"]
            totals[arm] = row[label]["total"]
        w = row["winner"]
        winner = "tie" if w == "平" else arm_of[w]
        out[task] = {
            "A": totals["A"],
            "B": totals["B"],
            "winner": winner,
            "reason": row["reason"],
            "Q1": {arm_of["甲" if label == "jia" else "乙"]: row[label]["Q1"] for label in ("jia", "yi")},
            "Q2": {arm_of["甲" if label == "jia" else "乙"]: row[label]["Q2"] for label in ("jia", "yi")},
        }
    return out


def main() -> None:
    j1 = unblind(load("judge-1.json"), load("map-1.json", subdir=""))
    j2 = unblind(load("judge-2.json"), load("map-2.json", subdir=""))

    votes = {"A": 0, "B": 0, "tie": 0}
    scores = {"A": [], "B": []}
    per_task = {}
    for task in TASKS:
        row = {"judge1": j1[task], "judge2": j2[task], "votes": []}
        for judge in (j1, j2):
            votes[judge[task]["winner"]] += 1
            scores["A"].append(judge[task]["A"])
            scores["B"].append(judge[task]["B"])
            row["votes"].append(judge[task]["winner"])
        per_task[task] = row

    n = len(scores["A"])
    result = {
        "n_judgments": n,
        "votes": votes,
        "mean_A": round(sum(scores["A"]) / n, 3),
        "mean_B": round(sum(scores["B"]) / n, 3),
        "diff": round((sum(scores["A"]) - sum(scores["B"])) / n, 3),
        "per_task": per_task,
        "judge_agreement": sum(1 for t in TASKS if j1[t]["winner"] == j2[t]["winner"]),
    }
    (ITER / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"n={n}  votes A={votes['A']} B={votes['B']} tie={votes['tie']}")
    print(f"mean A={result['mean_A']}  B={result['mean_B']}  diff={result['diff']:+.3f}")
    print(f"judge agreement {result['judge_agreement']}/4")
    print()
    print("| 题 | J1 winner | J2 winner | J1 A/B | J2 A/B |")
    print("|---|---|---|---|---|")
    for task in TASKS:
        r = per_task[task]
        print(
            f"| {task.upper()} | {r['votes'][0]} | {r['votes'][1]} | "
            f"{r['judge1']['A']}/{r['judge1']['B']} | {r['judge2']['A']}/{r['judge2']['B']} |"
        )


if __name__ == "__main__":
    main()
