"""Run the Week 7 pipeline with a real image and local order data."""

import json

from src.agent.pipeline import run_pipeline
from src.common.schemas import CaseInput


def main():
    case = CaseInput(
        case_id="WEEK7_END_TO_END_001",
        order_id="ORD001",
        claim_text=(
            "The jacket arrived with a tear on the left sleeve."
        ),
        image_paths=[
            "data/member1/images/member1_jacket_001.jpg"
        ],
    )

    print(
        "Running Members 1-3 and the Student 4 decision Agent...",
        flush=True,
    )

    result = run_pipeline(
        case,
        # Historical demo date, not today's date.
        request_date="2026-08-15",
        # Explicit demo input, not automatic visibility detection.
        relevant_region_visible=True,
        confidence_method="ml",
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        ),
        flush=True,
    )

    print("\nEnd-to-end pipeline finished.", flush=True)


if __name__ == "__main__":
    main()