"""Adapt the real Member 1 module to the shared Agent schema."""

from pathlib import Path

from src.common.schemas import CaseInput, Member1Output
from src.image_quality.claim_parser import parse_claim
from src.image_quality.quality import assess_image_quality


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Provisional integration scores, not calibrated probabilities.
BLUR_LABEL_SCORES = {
    "clear": 1.0,
    "slightly_blurred": 0.5,
    "severely_blurred": 0.0,
}

LIGHTING_LABEL_SCORES = {
    "normal": 1.0,
    "dark": 0.0,
    "overexposed": 0.0,
}


def run_member1(
    case: CaseInput,
    *,
    relevant_region_visible: bool,
) -> tuple[Member1Output, dict]:
    """Parse the claim and assess one real image.

    Region visibility must be supplied explicitly.
    The current Member 1 module does not detect it automatically.
    """

    if len(case.image_paths) != 1:
        raise ValueError(
            "Member 1 adapter V1 requires exactly one image."
        )

    image_path = Path(case.image_paths[0]).expanduser()

    if not image_path.is_absolute():
        image_path = PROJECT_ROOT / image_path

    claim = parse_claim(case.claim_text)

    quality = assess_image_quality(
        str(image_path),
        relevant_region_visible=relevant_region_visible,
    )

    sharpness_score = BLUR_LABEL_SCORES[
        quality["blur_label"]
    ]
    lighting_score = LIGHTING_LABEL_SCORES[
        quality["lighting_label"]
    ]

    image_quality = min(
        sharpness_score,
        lighting_score,
    )

    if not quality["image_usable"]:
        image_quality = 0.0

    member1 = Member1Output(
        case_id=case.case_id,
        product=claim["product"],
        claimed_defect=claim["claimed_defect"],
        claimed_location=claim["claimed_location"],
        image_quality=image_quality,
        blur_score=quality["blur_score"],
        lighting_score=lighting_score,
        relevant_region_visible=(
            quality["relevant_region_visible"]
        ),
        image_usable=quality["image_usable"],
    )

    return member1, quality