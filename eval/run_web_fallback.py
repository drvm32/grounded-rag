"""
Runs the "not in local corpus, but real and web-searchable" question group
against the current workflow.py to check that it correctly falls back to
Tavily web search with citations instead of refusing or hallucinating from
local context alone.

Usage:
    ./venv/Scripts/python.exe eval/run_web_fallback.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import query_result
from eval.test_questions import QUESTIONS

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "results_web_fallback.md")
MAX_RETRIES = 3


def run():
    web_fallback = [q for q in QUESTIONS if q["group"] == "web_fallback"]
    results = []

    for i, q in enumerate(web_fallback, start=1):
        print(f"[{i}/{len(web_fallback)}] {q['question']}")
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
    lines = ["# Web fallback eval results\n"]
    for r in results:
        lines.append(f"## [{r['id']}] {r['question']}\n")
        lines.append(f"**Expected:** {r['expected_answer']}\n")
        lines.append(f"**System answer:** {r['system_answer']}\n")
        if r.get("total_time") is not None:
            lines.append(f"**Latency:** {r['total_time']:.2f}s\n")
        lines.append("**Grade (fill in correct-web-cited/incorrect):** \n")
        lines.append("---\n")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run()
