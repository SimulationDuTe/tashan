"""Build an anonymous A/B packet for iteration-2 (patched skill vs round-1 baseline).

Only the three retested tasks are included. The mapping is random and stored in
judgment/map.json so the judges never see which arm produced which file.
"""

import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "pilot"
ITER1 = ROOT / "iteration-1"
ITER2 = ROOT / "iteration-2"
TASKS = ["h1-latency", "s1-dict-complexity", "s2-sentence-trim"]

out = ITER2 / "judgment" / "round-1"
out.mkdir(parents=True, exist_ok=True)

mapping = {}
for task in TASKS:
    new = ITER2 / task / "with_skill" / "answer.md"
    base = ITER1 / task / "without_skill" / "answer.md"
    if not new.is_file():
        raise SystemExit(f"missing {new}")
    labels = ["A", "B"]
    random.shuffle(labels)
    mapping[task] = {labels[0]: "with_skill", labels[1]: "without_skill"}
    for label, arm in mapping[task].items():
        src = new if arm == "with_skill" else base
        shutil.copyfile(src, out / f"{task}-{label}.md")

(ITER2 / "judgment" / "map.json").write_text(
    json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(mapping, ensure_ascii=False, indent=2))
