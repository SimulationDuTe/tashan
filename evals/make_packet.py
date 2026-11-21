"""Build an anonymous A/B packet for an iteration directory.

Usage:
    python evals/make_packet.py iteration-3 h1-latency,h2-team-throughput,h4-db-cost,s1-dict-complexity with_skill generic
"""

import json
import random
import shutil
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
        files = {arm_a: base / task / arm_a / "answer.md", arm_b: base / task / arm_b / "answer.md"}
        for arm, path in files.items():
            if not path.is_file():
                raise SystemExit(f"missing {path}")
        labels = ["A", "B"]
        random.shuffle(labels)
        mapping[task] = {labels[0]: arm_a, labels[1]: arm_b}
        for label, arm in mapping[task].items():
            shutil.copyfile(files[arm], out / f"{task}-{label}.md")

    (base / "judgment" / "map.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(mapping, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
