from src.evidence.rules import load_adopted_rules


def test_adopted_rules_cover_three_required_layers():
    rules = load_adopted_rules()

    assert len(rules) == 3
    assert {rule["category"] for rule in rules} == {
        "text_order_verification",
        "image_evidence_verification",
        "automatic_decision_thresholds",
    }


def test_external_rules_are_traceable_and_auto_rule_is_project_defined():
    rules = load_adopted_rules()
    external = [rule for rule in rules if rule["source_type"] == "official_retailer_policy"]
    automatic = next(
        rule for rule in rules if rule["category"] == "automatic_decision_thresholds"
    )

    assert all(rule["source_url"] for rule in external)
    assert automatic["source_type"] == "project_defined_research_baseline"
    assert automatic["requirements"]["high_evidence_confidence_minimum"] == 0.8
