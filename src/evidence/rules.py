"""Load the adopted evidence and automatic-decision rules."""

import json
from pathlib import Path
from typing import Any


DEFAULT_RULES_FILE = Path("data/policies/adopted_evidence_rules.json")


def load_adopted_rules(
    filename: str | Path = DEFAULT_RULES_FILE,
) -> list[dict[str, Any]]:
    """Return the three traceable rule groups used by the prototype."""

    with Path(filename).open(encoding="utf-8") as rules_file:
        rules = json.load(rules_file)

    required_categories = {
        "text_order_verification",
        "image_evidence_verification",
        "automatic_decision_thresholds",
    }
    categories = {rule.get("category") for rule in rules}
    if categories != required_categories:
        raise ValueError("adopted evidence rules must contain all three categories")
    return rules

