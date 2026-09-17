from src.agent.member1_adapter import run_member1
from src.common.schemas import CaseInput
from src.agent.pipeline import run_pipeline

def test_real_member1_adapter():
    case = CaseInput(
        case_id="WEEK4_MEMBER1_001",
        order_id="ORD_WEEK4_001",
        claim_text="The T-shirt has a tear on the front.",
        image_paths=[
            "data/member1/images/member1_tshirt_001.jpg"
        ],
    )

    member1, raw_quality = run_member1(
        case,
        relevant_region_visible=True,
    )

    assert member1.case_id == "WEEK4_MEMBER1_001"

    assert member1.product == "t-shirt"
    assert member1.claimed_defect == "tear_hole"
    assert member1.claimed_location == "front"

    assert member1.relevant_region_visible is True
    assert member1.image_usable is True

    assert member1.blur_score >= 0
    assert 0.0 <= member1.lighting_score <= 1.0
    assert 0.0 <= member1.image_quality <= 1.0

    assert "blur_score" in raw_quality
    assert "blur_label" in raw_quality
    assert "brightness_score" in raw_quality
    assert "highlight_ratio" in raw_quality
    assert "lighting_label" in raw_quality
    assert "relevant_region_visible" in raw_quality
    assert "image_usable" in raw_quality
    assert "usability_reason" in raw_quality
    from src.agent.pipeline import run_pipeline


class DummyDetector:
    def detect(self, case_id, image_path, evidence_quality):
        from src.common.schemas import Member2Output

        return Member2Output(
            case_id=case_id,
            detected_product="T-Shirt",
            damage_detected=True,
            damage_type="hole_or_tear",
            damage_location="front",
            damage_confidence=0.95,
            evidence_quality=evidence_quality,
            needs_human_review=False,
            claim_image_consistency=1.0,
            model_version="member1-week4-test",
        )


def test_pipeline_uses_real_member1_output():
    case = CaseInput(
        case_id="WEEK4_PIPELINE_001",
        order_id="ORD003",
        claim_text="The T-shirt has a tear on the front.",
        image_paths=[
            "data/member1/images/member1_tshirt_001.jpg"
        ],
    )

    result = run_pipeline(
        case,
        request_date="2026-08-15",
        relevant_region_visible=True,
        confidence_method="rule",
        detector=DummyDetector(),
    )

    member1 = result["member1"]

    assert member1["case_id"] == "WEEK4_PIPELINE_001"
    assert member1["product"] == "t-shirt"
    assert member1["claimed_defect"] == "tear_hole"
    assert member1["claimed_location"] == "front"

    assert member1["relevant_region_visible"] is True
    assert member1["image_usable"] is True

    assert "raw_image_quality" in result
    assert result["raw_image_quality"]["lighting_label"] == "normal"