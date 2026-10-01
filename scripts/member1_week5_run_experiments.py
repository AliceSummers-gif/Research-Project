"""Run Member 1 Week 5 image-quality experiments.

This script measures how controlled image degradations affect:
- Member 1 image quality outputs
- Member 2 damage detection outputs
- evidence confidence
- final pipeline decision
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from src.agent.pipeline import run_pipeline
from src.common.schemas import CaseInput
from src.damage_detection.damage import ClipBackend, DamageDetector


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    PROJECT_ROOT
    / "data/member1/week5/degradation_manifest.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data/member1/week5/results"
)

RESULTS_CSV_PATH = (
    OUTPUT_DIR
    / "week5_experiment_results.csv"
)

SUMMARY_JSON_PATH = (
    OUTPUT_DIR
    / "week5_experiment_summary.json"
)

REPORT_MD_PATH = (
    PROJECT_ROOT
    / "docs/member1_week5_experiments.md"
)

ORDER_ID = "ORD003"
REQUEST_DATE = "2026-08-15"
CLAIM_TEXT = "The t-shirt has a stain on the front."


def parse_bool(value: str) -> bool:
    """Convert a CSV boolean string to bool."""
    return str(value).strip().lower() == "true"


def to_relative(path: Path) -> str:
    """Convert an absolute path to project-relative path."""
    return path.relative_to(PROJECT_ROOT).as_posix()


def get_confidence_label(confidence: float) -> str:
    """Convert evidence confidence to HIGH, MEDIUM, or LOW."""
    if confidence >= 0.80:
        return "HIGH"

    if confidence >= 0.50:
        return "MEDIUM"

    return "LOW"


def load_manifest(
    manifest_path: Path,
) -> list[dict[str, str]]:
    """Load the Week 5 degradation manifest."""

    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Manifest not found: {manifest_path}"
        )

    with manifest_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def build_case(
    row: dict[str, str],
) -> CaseInput:
    """Create one CaseInput for an experimental condition."""

    return CaseInput(
        case_id=row["case_id"],
        order_id=ORDER_ID,
        claim_text=CLAIM_TEXT,
        image_paths=[
            row["image_path"]
        ],
    )


def run_one_experiment(
    row: dict[str, str],
    detector: DamageDetector,
) -> dict[str, object]:
    """Run one controlled degradation experiment."""

    case = build_case(row)

    relevant_region_visible = parse_bool(
        row["relevant_region_visible"]
    )

    result = run_pipeline(
        case,
        request_date=REQUEST_DATE,
        relevant_region_visible=relevant_region_visible,
        confidence_method="rule",
        detector=detector,
    )

    member1 = result["member1"]
    raw_quality = result["raw_image_quality"]
    member2 = result["member2"]
    member3 = result["member3"]
    decision = result["decision"]

    evidence_confidence = float(
        decision.get(
            "evidence_confidence",
            0.0,
        )
    )

    confidence_label = get_confidence_label(
        evidence_confidence
    )

    return {
        # Experiment metadata
        "case_id": row["case_id"],
        "condition": row["condition"],
        "image_path": row["image_path"],
        "description": row["description"],
        "relevant_region_visible_input": (
            relevant_region_visible
        ),

        # Member 1
        "member1_image_quality": (
            member1.get("image_quality")
        ),
        "member1_blur_score": (
            member1.get("blur_score")
        ),
        "member1_lighting_score": (
            member1.get("lighting_score")
        ),
        "member1_relevant_region_visible": (
            member1.get(
                "relevant_region_visible"
            )
        ),
        "member1_image_usable": (
            member1.get("image_usable")
        ),

        # Raw image-quality signals
        "raw_blur_label": (
            raw_quality.get("blur_label")
        ),
        "raw_brightness_score": (
            raw_quality.get(
                "brightness_score"
            )
        ),
        "raw_highlight_ratio": (
            raw_quality.get(
                "highlight_ratio"
            )
        ),
        "raw_lighting_label": (
            raw_quality.get(
                "lighting_label"
            )
        ),
        "raw_usability_reason": (
            raw_quality.get(
                "usability_reason"
            )
        ),

        # Member 2
        "member2_detected_product": (
            member2.get(
                "detected_product"
            )
        ),
        "member2_damage_detected": (
            member2.get(
                "damage_detected"
            )
        ),
        "member2_damage_type": (
            member2.get(
                "damage_type"
            )
        ),
        "member2_damage_location": (
            member2.get(
                "damage_location"
            )
        ),
        "member2_damage_confidence": (
            member2.get(
                "damage_confidence"
            )
        ),
        "member2_evidence_quality": (
            member2.get(
                "evidence_quality"
            )
        ),
        "member2_needs_human_review": (
            member2.get(
                "needs_human_review"
            )
        ),
        "member2_claim_image_consistency": (
            member2.get(
                "claim_image_consistency"
            )
        ),
        "member2_rationale": (
            member2.get(
                "rationale"
            )
        ),

        # Member 3
        "member3_order_valid": (
            member3.get(
                "order_valid"
            )
        ),
        "member3_policy_eligible": (
            member3.get(
                "policy_eligible"
            )
        ),
        "member3_image_order_consistency": (
            member3.get(
                "image_order_consistency"
            )
        ),
        "member3_policy_match_score": (
            member3.get(
                "policy_match_score"
            )
        ),
        "member3_evidence_completeness": (
            member3.get(
                "evidence_completeness"
            )
        ),
        "member3_refund_amount": (
            member3.get(
                "refund_amount"
            )
        ),

        # Final decision
        "decision_evidence_confidence": (
            evidence_confidence
        ),
        "decision_confidence_label": (
            confidence_label
        ),
        "decision_refund_risk": (
            decision.get(
                "refund_risk"
            )
        ),
        "decision": (
            decision.get(
                "decision"
            )
        ),
        "decision_reason": (
            decision.get(
                "reason"
            )
        ),
    }


def save_csv(
    rows: list[dict[str, object]],
    output_path: Path,
) -> None:
    """Save detailed experiment results to CSV."""

    if not rows:
        raise ValueError(
            "No experiment rows to save."
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(rows)


def build_summary(
    rows: list[dict[str, object]],
) -> dict[str, object]:
    """Build summary statistics for Week 5."""

    decision_counts = Counter(
        row["decision"]
        for row in rows
    )

    damage_type_counts = Counter(
        row["member2_damage_type"]
        for row in rows
    )

    evidence_quality_counts = Counter(
        row["member2_evidence_quality"]
        for row in rows
    )

    usability_counts = Counter(
        str(
            row["member1_image_usable"]
        )
        for row in rows
    )

    confidence_label_counts = Counter(
        row["decision_confidence_label"]
        for row in rows
    )

    damage_confidence_by_condition = {}

    evidence_confidence_by_condition = {}

    for row in rows:
        condition = str(
            row["condition"]
        )

        damage_confidence_by_condition[
            condition
        ] = float(
            row[
                "member2_damage_confidence"
            ]
            or 0.0
        )

        evidence_confidence_by_condition[
            condition
        ] = float(
            row[
                "decision_evidence_confidence"
            ]
            or 0.0
        )

    condition_results = []

    for row in rows:
        condition_results.append(
            {
                "case_id": (
                    row["case_id"]
                ),
                "condition": (
                    row["condition"]
                ),
                "member1_image_quality": (
                    row[
                        "member1_image_quality"
                    ]
                ),
                "member1_image_usable": (
                    row[
                        "member1_image_usable"
                    ]
                ),
                "raw_blur_label": (
                    row[
                        "raw_blur_label"
                    ]
                ),
                "raw_lighting_label": (
                    row[
                        "raw_lighting_label"
                    ]
                ),
                "member2_damage_type": (
                    row[
                        "member2_damage_type"
                    ]
                ),
                "member2_damage_confidence": (
                    row[
                        "member2_damage_confidence"
                    ]
                ),
                "evidence_confidence": (
                    row[
                        "decision_evidence_confidence"
                    ]
                ),
                "confidence_label": (
                    row[
                        "decision_confidence_label"
                    ]
                ),
                "decision": (
                    row["decision"]
                ),
            }
        )

    return {
        "experiment_name": (
            "Member 1 Week 5 "
            "Image Quality Experiments"
        ),
        "total_conditions": (
            len(rows)
        ),
        "source_manifest": (
            to_relative(
                MANIFEST_PATH
            )
        ),
        "order_id": (
            ORDER_ID
        ),
        "request_date": (
            REQUEST_DATE
        ),
        "claim_text": (
            CLAIM_TEXT
        ),
        "decision_counts": (
            dict(
                decision_counts
            )
        ),
        "damage_type_counts": (
            dict(
                damage_type_counts
            )
        ),
        "evidence_quality_counts": (
            dict(
                evidence_quality_counts
            )
        ),
        "usability_counts": (
            dict(
                usability_counts
            )
        ),
        "confidence_label_counts": (
            dict(
                confidence_label_counts
            )
        ),
        "damage_confidence_by_condition": (
            damage_confidence_by_condition
        ),
        "evidence_confidence_by_condition": (
            evidence_confidence_by_condition
        ),
        "conditions": (
            condition_results
        ),
    }


def save_summary_json(
    summary: dict[str, object],
    output_path: Path,
) -> None:
    """Save Week 5 summary as JSON."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def save_markdown_report(
    rows: list[dict[str, object]],
    summary: dict[str, object],
    output_path: Path,
) -> None:
    """Save Week 5 experimental report."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    lines.append(
        "# Member 1 Week 5 "
        "Image Quality Experiments"
    )

    lines.append("")

    lines.append(
        "## 1. Objective"
    )

    lines.append("")

    lines.append(
        "The objective of Week 5 is to "
        "measure how controlled image-quality "
        "degradation affects damage detection, "
        "evidence confidence, and the final "
        "refund decision."
    )

    lines.append("")

    lines.append(
        "The same source damage image is used "
        "for all experimental conditions so "
        "that image quality is the main "
        "controlled variable."
    )

    lines.append("")

    lines.append(
        "## 2. Experiment Setup"
    )

    lines.append("")

    lines.append(
        f"- Total conditions: "
        f"{summary['total_conditions']}"
    )

    lines.append(
        f"- Order ID: "
        f"{summary['order_id']}"
    )

    lines.append(
        f"- Request date: "
        f"{summary['request_date']}"
    )

    lines.append(
        f"- Claim: "
        f"{summary['claim_text']}"
    )

    lines.append("")

    lines.append(
        "Controlled image conditions:"
    )

    lines.append("")

    for row in rows:
        lines.append(
            f"- {row['condition']}"
        )

    lines.append("")

    lines.append(
        "## 3. Experimental Results"
    )

    lines.append("")

    lines.append(
        "| Case ID | Condition | "
        "Image Quality | Image Usable | "
        "Blur | Lighting | "
        "Damage Type | Damage Confidence | "
        "Evidence Confidence | "
        "Confidence Label | "
        "Final Decision |"
    )

    lines.append(
        "| --- | --- | ---: | --- | "
        "--- | --- | --- | ---: | "
        "---: | --- | --- |"
    )

    for row in rows:
        lines.append(
            f"| {row['case_id']} "
            f"| {row['condition']} "
            f"| {row['member1_image_quality']} "
            f"| {row['member1_image_usable']} "
            f"| {row['raw_blur_label']} "
            f"| {row['raw_lighting_label']} "
            f"| {row['member2_damage_type']} "
            f"| {row['member2_damage_confidence']} "
            f"| {row['decision_evidence_confidence']} "
            f"| {row['decision_confidence_label']} "
            f"| {row['decision']} |"
        )

    lines.append("")

    lines.append(
        "## 4. Decision Counts"
    )

    lines.append("")

    for key, value in (
        summary[
            "decision_counts"
        ].items()
    ):
        lines.append(
            f"- {key}: {value}"
        )

    lines.append("")

    lines.append(
        "## 5. Confidence Labels"
    )

    lines.append("")

    for key, value in (
        summary[
            "confidence_label_counts"
        ].items()
    ):
        lines.append(
            f"- {key}: {value}"
        )

    lines.append("")

    lines.append(
        "## 6. Damage Detection Results"
    )

    lines.append("")

    for key, value in (
        summary[
            "damage_type_counts"
        ].items()
    ):
        lines.append(
            f"- {key}: {value}"
        )

    lines.append("")

    lines.append(
        "## 7. Interpretation"
    )

    lines.append("")

    lines.append(
        "The experiment evaluates whether "
        "image degradation changes Member 1 "
        "image usability, Member 2 damage "
        "confidence, overall evidence confidence, "
        "and the final decision."
    )

    lines.append("")

    lines.append(
        "Severe degradation conditions that "
        "cause Member 1 to mark an image as "
        "unusable are expected to trigger the "
        "Member 2 evidence-quality safety gate. "
        "In these cases, damage confidence may "
        "fall to zero and the final system may "
        "request additional evidence."
    )

    lines.append("")

    lines.append(
        "Mild degradation may remain usable "
        "and allow the damage detector to "
        "continue operating."
    )

    lines.append("")

    lines.append(
        "The results should be interpreted "
        "as a controlled prototype experiment "
        "rather than a measure of real-world "
        "generalisation."
    )

    lines.append("")

    lines.append(
        "## 8. Limitations"
    )

    lines.append("")

    lines.append(
        "- The experiment uses one primary "
        "damage image."
    )

    lines.append(
        "- Image degradations are synthetically "
        "generated."
    )

    lines.append(
        "- The CLIP damage detector is a "
        "zero-shot prototype."
    )

    lines.append(
        "- Member 1 image-quality thresholds "
        "remain heuristic."
    )

    lines.append(
        "- Relevant-region visibility for "
        "cropped and occluded conditions is "
        "provided explicitly."
    )

    lines.append(
        "- The experiment does not demonstrate "
        "real-world model generalisation."
    )

    lines.append("")

    lines.append(
        "## 9. Output Files"
    )

    lines.append("")

    lines.append(
        f"- Detailed CSV: "
        f"`{to_relative(RESULTS_CSV_PATH)}`"
    )

    lines.append(
        f"- Summary JSON: "
        f"`{to_relative(SUMMARY_JSON_PATH)}`"
    )

    lines.append(
        f"- Degradation manifest: "
        f"`{to_relative(MANIFEST_PATH)}`"
    )

    lines.append("")

    output_path.write_text(
        "\n".join(lines)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    """Run all Week 5 degradation experiments."""

    manifest_rows = load_manifest(
        MANIFEST_PATH
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    detector = DamageDetector(
        backend=ClipBackend(),
    )

    experiment_rows = []

    print(
        "=== Member 1 Week 5 Experiments ==="
    )

    print(
        f"Manifest: "
        f"{to_relative(MANIFEST_PATH)}"
    )

    print()

    for index, row in enumerate(
        manifest_rows,
        start=1,
    ):
        result_row = run_one_experiment(
            row,
            detector=detector,
        )

        experiment_rows.append(
            result_row
        )

        print(
            f"[{index}/{len(manifest_rows)}] "
            f"{row['condition']:<13} "
            f"-> damage_type="
            f"{result_row['member2_damage_type']}, "
            f"damage_conf="
            f"{result_row['member2_damage_confidence']}, "
            f"evidence_conf="
            f"{result_row['decision_evidence_confidence']}, "
            f"label="
            f"{result_row['decision_confidence_label']}, "
            f"decision="
            f"{result_row['decision']}"
        )

    save_csv(
        experiment_rows,
        RESULTS_CSV_PATH,
    )

    summary = build_summary(
        experiment_rows
    )

    save_summary_json(
        summary,
        SUMMARY_JSON_PATH,
    )

    save_markdown_report(
        experiment_rows,
        summary,
        REPORT_MD_PATH,
    )

    print()

    print(
        "Experiment completed."
    )

    print(
        f"CSV saved to: "
        f"{to_relative(RESULTS_CSV_PATH)}"
    )

    print(
        f"JSON saved to: "
        f"{to_relative(SUMMARY_JSON_PATH)}"
    )

    print(
        f"Report saved to: "
        f"{to_relative(REPORT_MD_PATH)}"
    )


if __name__ == "__main__":
    main()