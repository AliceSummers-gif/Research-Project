"""Student 4 Agent with rule-based and ML confidence modes."""

from typing import Literal

from src.common.schemas import (
    Member1Output,
    Member2Output,
    Member3Output,
    Member4Output,
)
from src.decision.confidence import (
    calculate_evidence_confidence,
    get_confidence_label,
)
from src.decision.decision import make_decision
from src.decision.risk import calculate_refund_risk


def run_agent(
    member1: Member1Output,
    member2: Member2Output,
    member3: Member3Output,
    *,
    confidence_method: Literal["rule", "ml"] = "rule",
    model=None,
) -> Member4Output:
    """Combine member outputs using rule-based or ML confidence."""

    case_ids = {
        member1.case_id,
        member2.case_id,
        member3.case_id,
    }

    if len(case_ids) != 1:
        raise ValueError(
            "Member outputs have different case_id values."
        )

    if confidence_method not in {"rule", "ml"}:
        raise ValueError(
            "confidence_method must be 'rule' or 'ml'."
        )

    if confidence_method == "rule":
        evidence_confidence = calculate_evidence_confidence(
            member1,
            member2,
            member3,
        )
    else:
        from src.decision.ml_confidence import (
            predict_evidence_confidence,
        )

        evidence_confidence = predict_evidence_confidence(
            member1,
            member2,
            member3,
            model=model,
        )

    confidence_label = get_confidence_label(
        evidence_confidence
    )

    refund_risk = calculate_refund_risk(
        member3.refund_amount
    )

    decision, reason = make_decision(
        confidence_label,
        refund_risk,
        member1,
        member2,
        member3,
    )

    return Member4Output(
        case_id=member1.case_id,
        evidence_confidence=evidence_confidence,
        refund_risk=refund_risk,
        decision=decision,
        reason=reason,
    )