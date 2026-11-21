"""Build blind judge packets for the Doubao run (iteration-8).

Input : the two Doubao answer files (A arm = skill agent, B arm = bare model)
Output: evals/pilot/iteration-8/{answers,packet-1.md,packet-2.md,map-1.json,map-2.json}

Packet 2 is the mirror of packet 1 (甲/乙 swapped) so the two judges see
different label assignments for the same content.
"""

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITER = ROOT / "pilot" / "iteration-8"
A_FILE = Path(r"C:\Users\xiazi\Doubao\chats\2026-11-21\new-chat\Tashan评测-A臂答复.md")
B_FILE = Path(r"C:\Users\xiazi\Doubao\chats\2026-11-21\new-chat\Tashan评测-B臂答复.md")
TASKS_MD = ROOT / "doubao-kit" / "tasks.md"


def split_answers(path: Path, prefix: str) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    parts = re.split(rf"^## ({prefix}\d)\s*$", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i].lower()] = parts[i + 1].strip()
    return out


def task_prompts() -> dict[str, str]:
    text = TASKS_MD.read_text(encoding="utf-8-sig")
    pairs = re.findall(
        r"^## (T\d)[^\n]*\n\n\*\*题面\*\*\n\n(.+?)\n\n\*\*考点\*\*", text, flags=re.M | re.S
    )
    return {tid.lower(): body.strip() for tid, body in pairs}


def render(task: str, prompt: str, left: tuple[str, str], right: tuple[str, str]) -> str:
    (label_a, body_a), (label_b, body_b) = left, right
    return (
        f"## {task.upper()}\n\n### 题目\n\n{prompt}\n\n"
        f"### 【{label_a}】\n\n{body_a}\n\n### 【{label_b}】\n\n{body_b}\n"
    )


def main() -> None:
    answers = {
        "A": split_answers(A_FILE, "A"),
        "B": split_answers(B_FILE, "B"),
    }
    prompts = task_prompts()
    tasks = ["t1", "t2", "t3", "t4"]
    key = {t: f"a{t[1:]}" for t in tasks}
    key_b = {t: f"b{t[1:]}" for t in tasks}
    for task in tasks:
        assert key[task] in answers["A"], f"missing A{task}"
        assert key_b[task] in answers["B"], f"missing B{task}"
        assert task in prompts, f"missing prompt {task}"

    (ITER / "answers" / "a").mkdir(parents=True, exist_ok=True)
    (ITER / "answers" / "b").mkdir(parents=True, exist_ok=True)
    for task in tasks:
        (ITER / "answers" / "a" / f"{task}.md").write_text(answers["A"][key[task]] + "\n", encoding="utf-8")
        (ITER / "answers" / "b" / f"{task}.md").write_text(answers["B"][key_b[task]] + "\n", encoding="utf-8")

    bodies = {
        "A": {t: answers["A"][key[t]] for t in tasks},
        "B": {t: answers["B"][key_b[t]] for t in tasks},
    }

    rng = random.Random(20261121)
    map1 = {}
    for task in tasks:
        first = rng.choice(["A", "B"])
        map1[task] = {"甲": first, "乙": "B" if first == "A" else "A"}

    packet1, packet2 = ["# 盲评材料（第一包）\n"], ["# 盲评材料（第二包）\n"]
    for task in tasks:
        p = prompts[task]
        m1 = map1[task]
        body1 = bodies[m1["甲"]][task], bodies[m1["乙"]][task]
        packet1.append(render(task, p, ("甲", body1[0]), ("乙", body1[1])))
        body2 = bodies[m1["乙"]][task], bodies[m1["甲"]][task]
        packet2.append(render(task, p, ("甲", body2[0]), ("乙", body2[1])))

    (ITER / "packet-1.md").write_text("\n".join(packet1), encoding="utf-8")
    (ITER / "packet-2.md").write_text("\n".join(packet2), encoding="utf-8")

    map2 = {t: {"甲": map1[t]["乙"], "乙": map1[t]["甲"]} for t in tasks}
    (ITER / "map-1.json").write_text(json.dumps(map1, ensure_ascii=False, indent=2), encoding="utf-8")
    (ITER / "map-2.json").write_text(json.dumps(map2, ensure_ascii=False, indent=2), encoding="utf-8")

    for task in tasks:
        a_len = len(bodies["A"][task])
        b_len = len(bodies["B"][task])
        print(f"{task}: A {a_len} chars / B {b_len} chars")
    print(json.dumps(map1, ensure_ascii=False))


if __name__ == "__main__":
    main()
