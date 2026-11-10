"""JSON(state.json) 저장 방식이 데이터가 커질 때 얼마나 느려지고 메모리를 쓰는지 측정한다.

usage: python3 -m tools.bench_storage   (프로젝트 루트에서 실행, 실제 state.json 은 건드리지 않음)
"""

import tempfile
import time
import tracemalloc
from pathlib import Path

from quiz import Quiz
from storage import StateStore


def make_quizzes(count):
    return [
        Quiz(f"벤치마크 문제 {i}: 다음 중 올바른 것은?", [f"선택지 {i}-{n}" for n in range(1, 5)], i % 4 + 1, "힌트")
        for i in range(count)
    ]


def measure(count):
    quizzes = make_quizzes(count)
    with tempfile.TemporaryDirectory() as tmp:
        store = StateStore(Path(tmp) / "state.json")

        start = time.perf_counter()
        store.save(quizzes, None, None, [])
        save_sec = time.perf_counter() - start
        size_mb = store.path.stat().st_size / 1024 / 1024

        tracemalloc.start()
        start = time.perf_counter()
        state, _, _ = store.load()
        load_sec = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 퀴즈 1개만 추가해도 파일 전체를 다시 써야 한다
        state["quizzes"].append(Quiz("추가 문제", ["a", "b", "c", "d"], 1))
        start = time.perf_counter()
        store.save(state["quizzes"], None, None, [])
        add_one_sec = time.perf_counter() - start
    return size_mb, save_sec, load_sec, peak / 1024 / 1024, add_one_sec


def main():
    print(f"{'퀴즈 수':>9} | {'파일 크기':>9} | {'전체 저장':>9} | {'불러오기':>9} | {'불러오기 최대 메모리':>14} | {'1개 추가 후 저장':>12}")
    print("-" * 88)
    for count in (100, 10_000, 100_000, 300_000):
        size, save, load, peak, add_one = measure(count)
        print(
            f"{count:>9,} | {size:>7.2f}MB | {save:>8.3f}s | {load:>8.3f}s | {peak:>16.1f}MB | {add_one:>14.3f}s"
        )


if __name__ == "__main__":
    main()
