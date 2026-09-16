"""Connect the real Member 2 damage detector to the Agent."""

from pathlib import Path

from src.common.schemas import (
    CaseInput,
    Member1Output,
    Member2Output,
)
from src.damage_detection.damage import (
    ClipBackend,
    DamageDetector,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_member2(
    case: CaseInput,
    member1: Member1Output,
    *,
    detector: DamageDetector | None = None,
) -> Member2Output:
    """Run damage detection using Member 1 image-usability results."""

    if case.case_id != member1.case_id:
        raise ValueError(
            "CaseInput and Member 1 have different case_id values."
        )

    if len(case.image_paths) != 1:
        raise ValueError(
            "Member 2 adapter V1 requires exactly one image."
        )

    image_path = Path(case.image_paths[0]).expanduser()

    if not image_path.is_absolute():
        image_path = PROJECT_ROOT / image_path

    evidence_quality = (
        "good"
        if (
            member1.image_usable
            and member1.relevant_region_visible
        )
        else "unusable"
    )

    if detector is None:
        detector = DamageDetector(
            backend=ClipBackend(),
        )

    return detector.detect(
        case_id=case.case_id,
        image_path=image_path,
        evidence_quality=evidence_quality,
    )