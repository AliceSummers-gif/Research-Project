"""Show recorded Week 5 Member 2 examples without rerunning or fabricating inference."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_RESULTS = Path("data/member2/week5/week5_results.csv")
DEFAULT_METRICS = Path("data/member2/week5/week5_metrics.json")


def first_matching(rows: list[dict[str, str]], **expected: str) -> dict[str, str]:
    for row in rows:
        if all(row[key] == value for key, value in expected.items()):
            return row
    raise ValueError(f"Recorded results do not contain an example matching {expected}")


def demo_payload(results_path: Path, metrics_path: Path) -> dict[str, object]:
    with results_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    executed = [row for row in rows if row["execution_status"] == "executed"]
    fields = (
        "case_id", "source_image_id", "image_path", "expected_damage",
        "predicted_damage", "expected_consistency", "predicted_consistency",
        "damage_confidence", "needs_human_review", "reason_code",
    )
    examples = {
        "supported_claim": first_matching(executed, expected_consistency="positive", predicted_consistency="positive"),
        "contradicted_claim": first_matching(executed, expected_consistency="negative", predicted_consistency="negative"),
        "human_review": first_matching(executed, predicted_consistency="ambiguous"),
    }
    return {
        "source": "recorded Week 5 CLIP baseline; this demo performs no model inference",
        "executed_cases": len(executed),
        "unmaterialized_variants": sum(row["execution_status"] == "not_materialized_variant" for row in rows),
        "damage_metrics": metrics["damage_detection"],
        "claim_image_metrics": metrics["claim_image_verification"],
        "examples": {
            label: {field: row[field] for field in fields} for label, row in examples.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    arguments = parser.parse_args()
    print(json.dumps(demo_payload(arguments.results, arguments.metrics), indent=2))


if __name__ == "__main__":
    main()
