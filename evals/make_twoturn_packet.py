"""Compose two-turn blind A/B packet for iteration-6.

Each side becomes one file: user's first request, assistant turn 1,
user's follow-up, assistant turn 2.

Usage:
    python evals/make_twoturn_packet.py iteration-6 q1-decompose,q2-staffing,q3-slo with_skill generic
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "pilot"


def main() -> None:
    iteration, task_list, arm_a, arm_b = sys.argv[1:5]
    base = ROOT / iteration
    tasks = [t.strip() for t in task_list.split(",") if t.strip()]
    out = base / "judgment" / "round-1"
    out.mkdir(parents=True, exist_ok=True)

    mapping = {}
    for task in tasks:
        prompt = (base / task / "prompt.txt").read_text(encoding="utf-8").strip()
        reply = (base / task / "reply.txt").read_text(encoding="utf-8").strip()
        bodies = {}
        for arm in (arm_a, arm_b):
            t1 = (base / task / arm / "turn1.md").read_text(encoding="utf-8-sig").strip()
            t2 = (base / task / arm / "answer.md").read_text(encoding="utf-8-sig").strip()
            bodies[arm] = (
                f"## 用户的第一条请求\n\n{prompt}\n\n"
                f"## 助手的第一轮答复\n\n{t1}\n\n"
                f"## 用户的追问\n\n{reply}\n\n"
                f"## 助手的第二轮答复\n\n{t2}\n"
            )
        labels = ["A", "B"]
        random.shuffle(labels)
        mapping[task] = {labels[0]: arm_a, labels[1]: arm_b}
        for label, arm in mapping[task].items():
            (out / f"{task}-{label}.md").write_text(bodies[arm], encoding="utf-8")

    (base / "judgment" / "map.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(mapping, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
