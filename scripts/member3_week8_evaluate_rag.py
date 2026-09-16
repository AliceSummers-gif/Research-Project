"""Evaluate the deterministic policy retriever on the Week 8 dataset."""

import json
from collections import defaultdict
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evidence.rag import retrieve_policies


DATASET = Path("data/test_cases/member3_week8_rag_evaluation.json")
OUTPUT = Path("data/results/member3_week8_rag_metrics.json")


def evaluate(cases: list[dict[str, str]]) -> dict[str, object]:
    top1_correct = 0
    hit_at_3 = 0
    reciprocal_rank_total = 0.0
    failures = []
    policy_totals: dict[str, int] = defaultdict(int)
    policy_correct: dict[str, int] = defaultdict(int)

    for case in cases:
        expected = case["expected_policy_id"]
        results = retrieve_policies(case["query"], top_k=3)
        ranking = [result.policy_id for result in results]
        policy_totals[expected] += 1

        if ranking and ranking[0] == expected:
            top1_correct += 1
            policy_correct[expected] += 1
        else:
            failures.append(
                {
                    "case_id": case["case_id"],
                    "query": case["query"],
                    "expected_policy_id": expected,
                    "retrieved_policy_ids": ranking,
                }
            )

        if expected in ranking:
            rank = ranking.index(expected) + 1
            hit_at_3 += 1
            reciprocal_rank_total += 1 / rank

    total = len(cases)
    return {
        "evaluation_name": "Member 3 Week 8 lexical RAG baseline",
        "dataset_type": "synthetic_labelled_evaluation",
        "total_cases": total,
        "top_1_accuracy": top1_correct / total if total else 0.0,
        "hit_rate_at_3": hit_at_3 / total if total else 0.0,
        "mean_reciprocal_rank": reciprocal_rank_total / total if total else 0.0,
        "per_policy_top_1_accuracy": {
            policy_id: policy_correct[policy_id] / count
            for policy_id, count in sorted(policy_totals.items())
        },
        "top_1_failures": failures,
        "limitations": [
            "Cases are synthetic and do not establish real-world accuracy.",
            "The policy corpus contains only four mock policies.",
            "Queries were authored for controlled baseline evaluation.",
        ],
    }


def main() -> None:
    cases = json.loads(DATASET.read_text(encoding="utf-8"))
    metrics = evaluate(cases)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
