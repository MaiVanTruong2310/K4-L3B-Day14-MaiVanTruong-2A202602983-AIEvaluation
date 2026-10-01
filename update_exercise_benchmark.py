"""Refresh Exercise 3.2 from the saved benchmark result."""

import json
from pathlib import Path


root = Path(__file__).resolve().parent
results_file = root / "artifacts" / "benchmark_results.json"
artifact = json.loads(results_file.read_text(encoding="utf-8"))
results = artifact["results"]
summary = artifact["summary"]

lines = [
    "| ID | Question (short) | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |",
    "| --- | ---------------- | ---------: | ------------: | -----------: | --------: | -----------: | ------: | ------- | ------------ |",
]
for result in results:
    question = result["question"].replace("|", "\\|")
    if len(question) > 45:
        question = question[:42] + "..."
    lines.append(
        f"| {result['id']} | {question} | "
        f"{result['context_recall']:.3f} | {result['context_precision']:.3f} | "
        f"{result['faithfulness']:.3f} | {result['relevance']:.3f} | "
        f"{result['completeness']:.3f} | {result['overall']:.3f} | "
        f"{'Yes' if result['passed'] else 'No'} | {result['failure_type'] or '—'} |"
    )

lines += [
    "",
    "**Aggregate Report**",
    "",
    f"- Overall pass rate: **{summary['pass_rate']:.1%}** ({summary['passed']}/{summary['total']})",
    f"- Avg Context Recall: **{summary['avg_context_recall']:.3f}**",
    f"- Avg Context Precision: **{summary['avg_context_precision']:.3f}**",
    f"- Avg Faithfulness: **{summary['avg_faithfulness']:.3f}**",
    f"- Avg Relevance: **{summary['avg_relevance']:.3f}**",
    f"- Avg Completeness: **{summary['avg_completeness']:.3f}**",
    "- Failure type distribution: **" + "; ".join(
        f"{name} {count}" for name, count in summary["failure_types"].items()
    ) + "**",
    "",
    "**Ba cases có Overall Score thấp nhất**",
    "",
]
for number, result in enumerate(sorted(results, key=lambda item: item["overall"])[:3], start=1):
    lines.append(
        f"{number}. ID: **{result['id']}** | Score: **{result['overall']:.3f}** | "
        f"Failure type: **{result['failure_type'] or '—'}**"
    )

lines += [
    "",
    "**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval",
    "hay generation?",
    "",
    "> Completeness thấp nhất. Nhiều câu thiếu điều kiện dù tài liệu liên quan đã được tìm thấy. "
    "Riêng A01 bị chấm thấp do cách đếm từ, dù câu từ chối tư vấn y tế là an toàn.",
    "",
]

path = root / "exercises.md"
text = path.read_text(encoding="utf-8")
start = text.index("| ID  | Question (short) |", text.index("### Exercise 3.2"))
end = text.index("### Exercise 3.3", start)
path.write_text(text[:start] + "\n".join(lines) + "\n" + text[end:], encoding="utf-8")
