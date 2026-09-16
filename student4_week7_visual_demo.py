"""Run real image-quality assessment and damage detection."""

import json

from src.agent.member1_adapter import run_member1
from src.agent.member2_adapter import run_member2
from src.common.schemas import CaseInput


def main():
    case = CaseInput(
        case_id="WEEK7_VISUAL_001",
        order_id="ORD001",
        claim_text=(
            "The jacket arrived with a tear on the left sleeve."
        ),
        image_paths=[
            "data/member1/images/member1_jacket_001.jpg"
        ],
    )

    print("Step 1: Running Member 1...", flush=True)

    member1, raw_quality = run_member1(
        case,
        relevant_region_visible=True,
    )

    print(
        json.dumps(
            {
                "member1": member1.model_dump(),
                "raw_quality": raw_quality,
            },
            indent=2,
            ensure_ascii=False,
        ),
        flush=True,
    )

    print(
        "\nStep 2: Running Member 2. "
        "The first run may download the CLIP model...",
        flush=True,
    )

    member2 = run_member2(case, member1)

    print(
        json.dumps(
            {"member2": member2.model_dump()},
            indent=2,
            ensure_ascii=False,
        ),
        flush=True,
    )

    print("\nVisual pipeline finished.", flush=True)


if __name__ == "__main__":
    main()