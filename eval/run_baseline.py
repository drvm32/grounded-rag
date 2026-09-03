"""
Runs the answerable question groups (factual, comparison, operational) against
the current workflow.py and writes a side-by-side comparison file for manual grading.

Usage:
    ./venv/Scripts/python.exe eval/run_baseline.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import query_result
from eval.test_questions import QUESTIONS

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "results_baseline.md")
MAX_RETRIES = 3


def run():
    answerable = [q for q in QUESTIONS if q["group"] in ("factual", "comparison", "operational")]
    results = []

    for i, q in enumerate(answerable, start=1):
        print(f"[{i}/{len(answerable)}] ({q['group']}) {q['question']}")
        answer = None
        total_time = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = query_result(q["question"])
                answer = result["answer"]
                total_time = result["timings"]["total"]
                break
            except Exception as e:
                print(f"  ERROR (attempt {attempt}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(15)
                else:
                    answer = f"[FAILED after {MAX_RETRIES} attempts: {e}]"
        results.append({**q, "system_answer": answer, "total_time": total_time})
        write_results(results)

    print(f"\nDone. Results written to {OUTPUT_PATH}")


def write_results(results):
    lines = ["# Baseline eval results\n"]
    for r in results:
        lines.append(f"## [{r['id']}] ({r['group']}) {r['question']}\n")
        lines.append(f"**Expected:** {r['expected_answer']}\n")
        lines.append(f"**System answer:** {r['system_answer']}\n")
        if r.get("total_time") is not None:
            lines.append(f"**Latency:** {r['total_time']:.2f}s\n")
        lines.append("**Grade (fill in correct/incorrect):** \n")
        lines.append("---\n")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run()
