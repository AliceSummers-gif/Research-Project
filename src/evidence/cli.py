"""Interactive command-line interface for the evidence-verification module."""

from pprint import pprint

from src.common.schemas import CaseInput, Member1Output, Member2Output
from src.evidence.pipeline import build_evidence_chain


def _ask_bool(prompt: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{prompt} [{suffix}]: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def _ask_score(prompt: str, default: float) -> float:
    while True:
        answer = input(f"{prompt} [{default}]: ").strip()
        if not answer:
            return default
        try:
            score = float(answer)
        except ValueError:
            print("Please enter a number from 0 to 1.")
            continue
        if 0.0 <= score <= 1.0:
            return score
        print("Please enter a number from 0 to 1.")


def main() -> None:
    print("\nRISK-AWARE REFUND — EVIDENCE VERIFICATION")
    print("Enter a refund case. Press Enter to accept a value in brackets.\n")

    case_id = input("Case ID [DEMO-001]: ").strip() or "DEMO-001"
    order_id = input("Order ID [ORD001]: ").strip() or "ORD001"
    claim = input(
        "Customer claim [The black jacket arrived with a tear on the left sleeve.]: "
    ).strip() or "The black jacket arrived with a tear on the left sleeve."
    detected_product = input("Detected product [Black Jacket]: ").strip() or "Black Jacket"
    damage_type = input(
        "Damage type (hole_or_tear/stain_or_spot/no_damage/uncertain) "
        "[hole_or_tear]: "
    ).strip() or "hole_or_tear"
    damage_detected = damage_type not in {"no_damage", "uncertain"}
    image_usable = _ask_bool("Is the image usable?", True)
    damage_confidence = _ask_score("Damage confidence", 0.88)
    claim_consistency = _ask_score("Claim-image consistency", 0.92)
    request_date = input("Request date [2026-08-15]: ").strip() or "2026-08-15"

    case_input = CaseInput(
        case_id=case_id,
        order_id=order_id,
        claim_text=claim,
        image_paths=["interactive-upload.jpg"] if image_usable else [],
    )
    member1 = Member1Output(
        case_id=case_id,
        product=detected_product,
        claimed_defect=damage_type,
        claimed_location=None,
        image_quality=0.9 if image_usable else 0.2,
        blur_score=0.1 if image_usable else 0.8,
        lighting_score=0.9 if image_usable else 0.3,
        relevant_region_visible=image_usable,
        image_usable=image_usable,
    )
    member2 = Member2Output(
        case_id=case_id,
        detected_product=detected_product,
        damage_detected=damage_detected,
        damage_type=damage_type,
        damage_location=None,
        damage_confidence=damage_confidence,
        needs_human_review=damage_type == "uncertain",
        claim_image_consistency=claim_consistency,
    )

    chain = build_evidence_chain(case_input, member1, member2, request_date)

    print("\nRETRIEVED ORDER")
    pprint(chain.order_evidence)
    print("\nRETRIEVED POLICY")
    pprint(chain.policy_evidence)
    print("\nVERIFIED EVIDENCE")
    pprint(chain.member3_output)
    print("\nFEEDBACK")
    print(chain.verified_evidence.reason)


if __name__ == "__main__":
    main()
