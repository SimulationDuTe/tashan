"""Aggregate the cheap pilot (evals/pilot/iteration-1).

Reads two blind-judge JSON files plus the A/B arm map, maps scores back to
arms, and writes results.json. Run from anywhere:

    python evals/analyze_pilot.py

No third-party dependencies.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PILOT = ROOT / "pilot" / "iteration-1"
JUDGES = PILOT / "judgment" / "round-1"
STRATUM = {
    "h1-latency": "hard",
    "h2-team-throughput": "hard",
    "h3-qa-bot": "hard",
    "h4-db-cost": "hard",
    "t1-support-ai": "trap",
    "t2-content-kpi": "trap",
    "s1-dict-complexity": "simple",
    "s2-sentence-trim": "simple",
}
DIMS = ("d1", "d2", "d3", "d4", "d5")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def total(entry: dict) -> int:
    return sum(int(entry[d]) for d in DIMS)


def map_winner(raw: str, a_is_with: bool) -> str:
    if raw == "tie":
        return "tie"
    winner_is_a = raw == "A"
    return "with" if winner_is_a == a_is_with else "base"


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(center - half, 4), round(center + half, 4)]


def chars(path: Path) -> int:
    return len(path.read_text(encoding="utf-8"))


def main() -> None:
    mapping = load_json(PILOT / "judgment" / "map.json")
    judges = [load_json(JUDGES / "judge-1.json"), load_json(JUDGES / "judge-2.json")]

    rows = []
    for task, stratum in STRATUM.items():
        a_is_with = mapping[task]["A"] == "with_skill"
        entries = [next(e for e in j["tasks"] if e["id"] == task) for j in judges]
        with_scores, base_scores, winners = [], [], []
        for entry in entries:
            ta, tb = total(entry["A"]), total(entry["B"])
            with_scores.append(ta if a_is_with else tb)
            base_scores.append(tb if a_is_with else ta)
            winners.append(map_winner(entry["winner"], a_is_with))

        rows.append(
            {
                "id": task,
                "stratum": stratum,
                "with": round(sum(with_scores) / len(with_scores), 2),
                "base": round(sum(base_scores) / len(base_scores), 2),
                "delta": round(
                    sum(with_scores) / len(with_scores)
                    - sum(base_scores) / len(base_scores),
                    2,
                ),
                "judges": winners,
                "with_chars": chars(PILOT / task / "with_skill" / "answer.md"),
                "base_chars": chars(PILOT / task / "without_skill" / "answer.md"),
            }
        )

    votes = {"with": 0, "base": 0, "tie": 0}
    for row in rows:
        for winner in row["judges"]:
            votes[winner] += 1
    decisive = votes["with"] + votes["base"]

    strata = []
    for name in ("hard", "trap", "simple"):
        subset = [r for r in rows if r["stratum"] == name]
        s_votes = {"with": 0, "base": 0, "tie": 0}
        for row in subset:
            for winner in row["judges"]:
                s_votes[winner] += 1
        with_mean = round(sum(r["with"] for r in subset) / len(subset), 3)
        base_mean = round(sum(r["base"] for r in subset) / len(subset), 3)
        strata.append(
            {
                "stratum": name,
                "with": with_mean,
                "base": base_mean,
                "delta": round(with_mean - base_mean, 3),
                "votes": s_votes,
            }
        )

    with_chars = sum(r["with_chars"] for r in rows)
    base_chars = sum(r["base_chars"] for r in rows)

    result = {
        "pilot": "iteration-1",
        "date": "2026-11-21",
        "design": "8 tasks x 2 arms x 1 generation, 2 blind judges with swapped read order",
        "tasks": rows,
        "summary": {
            "with_mean": round(sum(r["with"] for r in rows) / len(rows), 3),
            "base_mean": round(sum(r["base"] for r in rows) / len(rows), 3),
            "delta": round(
                sum(r["with"] for r in rows) / len(rows)
                - sum(r["base"] for r in rows) / len(rows),
                3,
            ),
            "votes": votes,
            "decisive_votes": decisive,
            "win_rate": round(votes["with"] / decisive, 3),
            "win_rate_wilson95": wilson(votes["with"], decisive),
            "judge_agreement_tasks": sum(1 for r in rows if r["judges"][0] == r["judges"][1]),
            "with_chars": with_chars,
            "base_chars": base_chars,
            "char_ratio": round(with_chars / base_chars, 3),
            "strata": strata,
        },
    }

    out = PILOT / "results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'task':<20}{'stratum':<8}{'with':>6}{'base':>6}{'delta':>7}  judges")
    for row in rows:
        print(
            f"{row['id']:<20}{row['stratum']:<8}{row['with']:>6}{row['base']:>6}"
            f"{row['delta']:>7}  {'/'.join(row['judges'])}"
        )
    s = result["summary"]
    print(f"\nwith={s['with_mean']} base={s['base_mean']} delta={s['delta']}")
    print(f"votes={s['votes']} win_rate={s['win_rate']} CI95={s['win_rate_wilson95']}")
    print(f"judge agreement {s['judge_agreement_tasks']}/8, chars ratio {s['char_ratio']}")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
