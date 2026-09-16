"""Run the real Member 1 module on existing project images."""

import json

from src.agent.member1_adapter import run_member1
from src.common.schemas import CaseInput


def main():
    examples = [
        (
            "CLEAR_IMAGE",
            "The jacket arrived with a tear on the left sleeve.",
            "data/member1/images/member1_jacket_001.jpg",
        ),
        (
            "DARK_IMAGE",
            "The hoodie arrived with a stain on the front.",
            "data/member1/images/member1_hoodie_001_dark.jpg",
        ),
    ]

    for case_id, claim_text, image_path in examples:
        case = CaseInput(
            case_id=case_id,
            order_id="ORD001",
            claim_text=claim_text,
            image_paths=[image_path],
        )

        # Explicit demo input, not an automatic visibility prediction.
        member1, raw_quality = run_member1(
            case,
            relevant_region_visible=True,
        )

        print(f"\nCase: {case_id}")
        print(
            json.dumps(
                {
                    "member1": member1.model_dump(),
                    "raw_quality": raw_quality,
                },
                indent=2,
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()