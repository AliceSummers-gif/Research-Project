"""Deterministic policy retrieval for the Member 3 prototype."""

import json
import re
from pathlib import Path

from src.evidence.models import RetrievedPolicy


DEFAULT_POLICY_KB = Path("data/policies/refund_policies.json")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

INTENT_PATTERNS = {
    "POL-FINAL-SALE": (
        "final sale",
        "final-sale",
        "clearance",
        "non-refundable",
        "non refundable",
        "no-refund",
        "no refund",
        "excluded",
        "cannot be returned",
        "refund exclusion",
    ),
    "POL-NO-DAMAGE": (
        "no visible damage",
        "no visible",
        "no damage",
        "not damaged",
        "undamaged",
        "no defect",
        "no hole",
        "no stain",
        "without a tear",
        "looks normal",
        "appears intact",
        "looks intact",
        "nothing in the image",
        "cannot identify",
        "does not support",
    ),
    "POL-WRONG-ITEM-14": (
        "wrong item",
        "wrong product",
        "incorrect item",
        "incorrect product",
        "different order",
        "another customer's",
        "not the item",
        "does not match my order",
        "do not match my order",
        "product mismatch",
        "not mine",
        "but received",
    ),
    "POL-DAMAGE-30": (
        "tear",
        "torn",
        "ripped",
        "hole",
        "stain",
        "spot",
        "broken zip",
        "broken zipper",
        "damaged",
        "damage",
    ),
}


def _tokens(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(text.lower()))


def classify_policy_intent(query: str) -> str | None:
    """Identify a high-precision policy intent before lexical ranking.

    Priority matters: exclusion and negated-damage language must be handled
    before generic words such as ``damage``, ``hole`` or ``product``.
    """

    normalized = " ".join(query.lower().split())
    for policy_id in (
        "POL-FINAL-SALE",
        "POL-NO-DAMAGE",
        "POL-WRONG-ITEM-14",
        "POL-DAMAGE-30",
    ):
        if any(pattern in normalized for pattern in INTENT_PATTERNS[policy_id]):
            return policy_id
    return None


def retrieve_policies(
    query: str,
    filename: str | Path = DEFAULT_POLICY_KB,
    top_k: int = 3,
    strategy: str = "intent_aware",
) -> list[RetrievedPolicy]:
    """Rank policies using lexical overlap with optional intent routing."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    if strategy not in {"lexical", "intent_aware"}:
        raise ValueError("strategy must be 'lexical' or 'intent_aware'")

    with Path(filename).open(encoding="utf-8") as policy_file:
        policies = json.load(policy_file)

    query_tokens = _tokens(query)
    routed_policy_id = classify_policy_intent(query) if strategy == "intent_aware" else None
    ranked = []
    for policy in policies:
        policy_tokens = _tokens(
            " ".join(
                [
                    policy["title"],
                    policy["policy_text"],
                    *policy["keywords"],
                    *policy["eligible_damage_types"],
                ]
            )
        )
        overlap = len(query_tokens & policy_tokens)
        lexical_score = overlap / max(len(query_tokens), 1)
        ranking_score = lexical_score
        if policy["policy_id"] == routed_policy_id:
            ranking_score += 1.0
        output_score = 1.0 if policy["policy_id"] == routed_policy_id else lexical_score
        ranked.append((ranking_score, output_score, policy))

    ranked.sort(key=lambda item: (-item[0], item[2]["policy_id"]))
    results = []
    for _, output_score, policy in ranked[:top_k]:
        results.append(
            RetrievedPolicy(
                policy_id=policy["policy_id"],
                title=policy["title"],
                policy_text=policy["policy_text"],
                policy_source=policy["policy_source"],
                policy_match=round(output_score, 2),
                refund_window_days=policy["refund_window_days"],
                requires_image=policy["requires_image"],
                eligible_damage_types=tuple(policy["eligible_damage_types"]),
            )
        )
    return results


def retrieve_best_policy(
    query: str,
    filename: str | Path = DEFAULT_POLICY_KB,
    strategy: str = "intent_aware",
) -> RetrievedPolicy:
    """Return the highest-ranked policy for a query."""

    return retrieve_policies(query, filename, top_k=1, strategy=strategy)[0]
