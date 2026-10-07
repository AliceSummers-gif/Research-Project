"""Generate the balanced Week 9 Member 3 evidence evaluation set."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "data/test_cases/member3_week9_evidence_evaluation.json"

CLAIMS = {
    "valid_hole": [
        "The black jacket arrived with a hole on the sleeve.",
        "A tear is visible in the delivered jacket.",
        "The jacket fabric was ripped when it arrived.",
    ],
    "valid_stain": [
        "The grey hoodie arrived with a stain.",
        "A dark spot is visible on the hoodie.",
        "The delivered hoodie has a fabric blemish.",
    ],
    "missing_image": [
        "The jacket arrived damaged but I have not attached a photo.",
        "There is a tear in the jacket without image evidence.",
        "My delivered jacket is damaged.",
    ],
    "unusable_image": [
        "The jacket is torn but the submitted image is unclear.",
        "The photo is unusable and does not clearly show the jacket tear.",
        "I submitted a poor image of the damaged jacket.",
    ],
    "no_damage": [
        "No visible damage was detected in the jacket image.",
        "The jacket looks intact in the submitted evidence.",
        "The image does not show a tear or hole.",
    ],
    "low_consistency": [
        "The claim says the jacket is torn but the image is inconsistent.",
        "The submitted evidence does not support the jacket damage claim.",
        "The claim and image describe different damage.",
    ],
    "product_mismatch": [
        "The claim concerns the brown jacket but the image shows a hoodie.",
        "The photographed product does not match the ordered jacket.",
        "A different garment appears in the evidence.",
    ],
    "expired_window": [
        "The blue jacket has a tear but the request is late.",
        "I am requesting a refund after the policy window.",
        "The damaged jacket was purchased more than 30 days ago.",
    ],
    "final_sale": [
        "The final-sale green hoodie has a stain.",
        "I want a refund for a damaged final-sale hoodie.",
        "The sale item arrived with a visible spot.",
    ],
    "unknown_order": [
        "The jacket is torn but the order number cannot be found.",
        "I submitted damage evidence for an unknown order.",
        "The supplied order ID is not in the order database.",
    ],
}

SCENARIOS = {
    "valid_hole": {
        "order_id": "ORD001",
        "detected_product": "Black Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.92,
        "request_date": "2026-08-15",
        "expected_eligible": True,
        "expected_reason": "Order, image, and policy evidence are consistent.",
    },
    "valid_stain": {
        "order_id": "ORD002",
        "detected_product": "Grey Hoodie",
        "damage_detected": True,
        "damage_type": "stain_or_spot",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.88,
        "request_date": "2026-08-16",
        "expected_eligible": True,
        "expected_reason": "Order, image, and policy evidence are consistent.",
    },
    "missing_image": {
        "order_id": "ORD001",
        "detected_product": "Black Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": False,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Required image evidence is missing.",
    },
    "unusable_image": {
        "order_id": "ORD001",
        "detected_product": "Black Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": False,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Submitted image evidence is not usable.",
    },
    "no_damage": {
        "order_id": "ORD001",
        "detected_product": "Black Jacket",
        "damage_detected": False,
        "damage_type": "no_damage",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "No visible damage was detected.",
    },
    "low_consistency": {
        "order_id": "ORD001",
        "detected_product": "Black Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.30,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Image evidence does not sufficiently support the claim.",
    },
    "product_mismatch": {
        "order_id": "ORD009",
        "detected_product": "Grey Hoodie",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "The detected product does not match the order.",
    },
    "expired_window": {
        "order_id": "ORD004",
        "detected_product": "Blue Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Refund request is outside the policy window.",
    },
    "final_sale": {
        "order_id": "ORD005",
        "detected_product": "Green Hoodie",
        "damage_detected": True,
        "damage_type": "stain_or_spot",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Final-sale products are not eligible for refund.",
    },
    "unknown_order": {
        "order_id": "ORD999",
        "detected_product": "Black Jacket",
        "damage_detected": True,
        "damage_type": "hole_or_tear",
        "image_present": True,
        "image_usable": True,
        "claim_image_consistency": 0.90,
        "request_date": "2026-08-15",
        "expected_eligible": False,
        "expected_reason": "Order ID was not found.",
    },
}


def build_cases() -> list[dict]:
    cases = []
    index = 1
    for scenario, template in SCENARIOS.items():
        claims = CLAIMS[scenario]
        for variation in range(12):
            case = {
                "case_id": f"M3_W9_E{index:03d}",
                "scenario": scenario,
                "claim_text": claims[variation % len(claims)],
                "dataset_type": "synthetic_balanced_evidence_evaluation",
                **template,
            }
            cases.append(case)
            index += 1
    return cases


def main() -> None:
    cases = build_cases()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(cases)} cases to {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
