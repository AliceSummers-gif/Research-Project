"""Week 7 decision safeguards for rule and ML confidence."""

import json
from pathlib import Path

import pytest

from src.agent.agent import run_agent
from src.common.schemas import (
    Member1Output,
    Member2Output,
    Member3Output,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_case():
    case_path = (
        PROJECT_ROOT
        / "data"
        / "test_cases"
        / "student4_auto_refund.json"
    )
    raw = json.loads(
        case_path.read_text(encoding="utf-8")
    )

    return (
        Member1Output(**raw["member1"]),
        Member2Output(**raw["member2"]),
        Member3Output(**raw["member3"]),
    )


@pytest.mark.parametrize("method", ["rule", "ml"])
def test_missing_consistency_requests_evidence(method):
    member1, member2, member3 = load_case()
    member2.claim_image_consistency = None

    result = run_agent(
        member1,
        member2,
        member3,
        confidence_method=method,
    )

    assert result.decision == "REQUEST_MORE_EVIDENCE"
    assert "missing" in result.reason.lower()
    assert member2.claim_image_consistency is None


@pytest.mark.parametrize("method", ["rule", "ml"])
def test_damage_review_flag_requires_review(method):
    member1, member2, member3 = load_case()
    member2.needs_human_review = True

    result = run_agent(
        member1,
        member2,
        member3,
        confidence_method=method,
    )

    assert result.decision == "HUMAN_REVIEW"
    assert "damage module" in result.reason.lower()


@pytest.mark.parametrize("method", ["rule", "ml"])
@pytest.mark.parametrize("quality", ["poor", "unusable"])
def test_insufficient_damage_evidence_requests_photo(
    method,
    quality,
):
    member1, member2, member3 = load_case()
    member2.evidence_quality = quality
    member2.needs_human_review = True

    result = run_agent(
        member1,
        member2,
        member3,
        confidence_method=method,
    )

    assert result.decision == "REQUEST_MORE_EVIDENCE"
    assert "insufficient" in result.reason.lower()