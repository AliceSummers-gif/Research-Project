"""Run the final Member 3 retrieval and evidence regression evaluation."""

import json
from collections import Counter
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.member3_week8_evaluate_rag import evaluate
from src.evidence.verification import verify_case


RETRIEVAL_DATASET = PROJECT_ROOT / "data/test_cases/member3_week8_rag_evaluation.json"
EVIDENCE_DATASET = PROJECT_ROOT / "data/test_cases/member3_cases.json"
OUTPUT = PROJECT_ROOT / "data/results/member3_week9_final_results.json"


def _load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_evidence_regression(cases: list[dict]) -> dict[str, object]:
    failures = []
    reason_counts: Counter[str] = Counter()

    for case in cases:
        result = verify_case(case)
        reason_counts[result.reason] += 1
        if result.policy_eligible != case["expected_eligible"]:
            failures.append(
                {
                    "case_id": case["case_id"],
                    "expected_eligible": case["expected_eligible"],
                    "actual_eligible": result.policy_eligible,
                    "reason": result.reason,
                }
            )

    passed = len(cases) - len(failures)
    return {
        "total_cases": len(cases),
        "passed_cases": passed,
        "pass_rate": passed / len(cases) if cases else 0.0,
        "failures": failures,
        "outcome_reason_counts": dict(sorted(reason_counts.items())),
    }


def build_final_results() -> dict[str, object]:
    retrieval_cases = _load(RETRIEVAL_DATASET)
    evidence_cases = _load(EVIDENCE_DATASET)
    baseline = evaluate(retrieval_cases, strategy="lexical")
    refined = evaluate(retrieval_cases, strategy="intent_aware")

    baseline_failure_ids = {
        failure["case_id"] for failure in baseline["top_1_failures"]
    }
    refined_failure_ids = {
        failure["case_id"] for failure in refined["top_1_failures"]
    }

    return {
        "evaluation_name": "Member 3 Week 9 final retrieval and evidence evaluation",
        "dataset_type": "synthetic_labelled_evaluation",
        "retrieval_comparison": {
            "baseline": baseline,
            "refined": refined,
            "top_1_absolute_improvement": (
                refined["top_1_accuracy"] - baseline["top_1_accuracy"]
            ),
            "resolved_baseline_failure_case_ids": sorted(
                baseline_failure_ids - refined_failure_ids
            ),
            "new_regression_case_ids": sorted(
                refined_failure_ids - baseline_failure_ids
            ),
        },
        "evidence_regression": evaluate_evidence_regression(evidence_cases),
        "limitations": [
            "All evaluation records are synthetic or controlled project data.",
            "The policy corpus contains four mock policy documents.",
            "Intent routing is deterministic and has not been validated on real claims.",
            "Image-model accuracy is outside the Member 3 retrieval evaluation.",
        ],
    }


def main() -> None:
    results = build_final_results()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    comparison = results["retrieval_comparison"]
    evidence = results["evidence_regression"]
    print(f"Baseline Top-1: {comparison['baseline']['top_1_accuracy']:.3f}")
    print(f"Refined Top-1:  {comparison['refined']['top_1_accuracy']:.3f}")
    print(f"Evidence cases: {evidence['passed_cases']}/{evidence['total_cases']} passed")
    print(f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
