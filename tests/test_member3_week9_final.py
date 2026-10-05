import json

from scripts.member3_week8_generate_dataset import build_cases
from scripts.member3_week8_evaluate_rag import evaluate
from scripts.member3_week9_final_evaluation import build_final_results
from src.evidence.rag import classify_policy_intent, retrieve_best_policy


def test_intent_router_handles_the_four_policy_families():
    examples = {
        "The jacket arrived with a tear.": "POL-DAMAGE-30",
        "I received the wrong item.": "POL-WRONG-ITEM-14",
        "The photo shows no visible damage.": "POL-NO-DAMAGE",
        "This clearance item was final sale.": "POL-FINAL-SALE",
    }

    for query, expected in examples.items():
        assert classify_policy_intent(query) == expected
        assert retrieve_best_policy(query).policy_id == expected


def test_refined_retrieval_improves_the_frozen_week8_baseline():
    cases = build_cases()
    baseline = evaluate(cases, strategy="lexical")
    refined = evaluate(cases, strategy="intent_aware")

    assert baseline["top_1_accuracy"] == 37 / 60
    assert refined["top_1_accuracy"] >= 0.95
    assert refined["top_1_accuracy"] > baseline["top_1_accuracy"]
    assert len(refined["top_1_failures"]) < len(baseline["top_1_failures"])


def test_final_evidence_regression_matches_all_expected_labels():
    results = build_final_results()
    regression = results["evidence_regression"]

    assert regression["total_cases"] == 12
    assert regression["passed_cases"] == 12
    assert regression["pass_rate"] == 1.0
    assert regression["failures"] == []


def test_saved_week9_results_match_reproducible_evaluation():
    with open("data/results/member3_week9_final_results.json", encoding="utf-8") as file:
        saved = json.load(file)

    assert saved == build_final_results()
