"""Generate controlled image degradations for Member 1 Week 5 experiments."""

from __future__ import annotations

import csv
from pathlib import Path

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_IMAGE = (
    PROJECT_ROOT
    / "data/member2/week1/images/spots_35/spot_004.jpg"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data/member1/week5/images"
)

MANIFEST_PATH = (
    PROJECT_ROOT
    / "data/member1/week5/degradation_manifest.csv"
)


def to_relative(path: Path) -> str:
    """Convert an absolute path to a project-relative path."""
    return path.relative_to(PROJECT_ROOT).as_posix()


def load_image(image_path: Path) -> np.ndarray:
    """Load a BGR image with validation."""
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    return image


def save_image(image: np.ndarray, output_path: Path) -> None:
    """Save a BGR image."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise ValueError(f"Failed to save image: {output_path}")


def make_slight_blur(image: np.ndarray) -> np.ndarray:
    """Apply a mild blur."""
    return cv2.GaussianBlur(image, (5, 5), 1.2)


def make_severe_blur(image: np.ndarray) -> np.ndarray:
    """Apply a strong blur."""
    return cv2.GaussianBlur(image, (25, 25), 8.0)


def make_dark(image: np.ndarray) -> np.ndarray:
    """Darken the image."""
    return cv2.convertScaleAbs(image, alpha=0.55, beta=-10)


def make_overexposed(image: np.ndarray) -> np.ndarray:
    """Increase brightness to simulate overexposure."""
    return cv2.convertScaleAbs(image, alpha=1.35, beta=45)


def make_cropped(image: np.ndarray) -> np.ndarray:
    """Crop away a large region, then resize back to original size."""
    height, width = image.shape[:2]

    cropped = image[
        0:int(height * 0.65),
        0:int(width * 0.65),
    ]

    return cv2.resize(
        cropped,
        (width, height),
        interpolation=cv2.INTER_LINEAR,
    )


def make_occluded(image: np.ndarray) -> np.ndarray:
    """Cover the centre region to simulate occlusion."""
    occluded = image.copy()

    height, width = occluded.shape[:2]

    x1 = int(width * 0.30)
    y1 = int(height * 0.30)
    x2 = int(width * 0.75)
    y2 = int(height * 0.75)

    cv2.rectangle(
        occluded,
        (x1, y1),
        (x2, y2),
        color=(0, 0, 0),
        thickness=-1,
    )

    return occluded


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    base_image = load_image(SOURCE_IMAGE)

    conditions = [
        {
            "case_id": "W5_IMG_001",
            "condition": "clear",
            "filename": "spot_004_clear.jpg",
            "relevant_region_visible": True,
            "description": "Original clear baseline image.",
            "generator": lambda image: image.copy(),
        },
        {
            "case_id": "W5_IMG_002",
            "condition": "slight_blur",
            "filename": "spot_004_slight_blur.jpg",
            "relevant_region_visible": True,
            "description": "Mild Gaussian blur.",
            "generator": make_slight_blur,
        },
        {
            "case_id": "W5_IMG_003",
            "condition": "severe_blur",
            "filename": "spot_004_severe_blur.jpg",
            "relevant_region_visible": True,
            "description": "Strong Gaussian blur.",
            "generator": make_severe_blur,
        },
        {
            "case_id": "W5_IMG_004",
            "condition": "dark",
            "filename": "spot_004_dark.jpg",
            "relevant_region_visible": True,
            "description": "Low-light version.",
            "generator": make_dark,
        },
        {
            "case_id": "W5_IMG_005",
            "condition": "overexposed",
            "filename": "spot_004_overexposed.jpg",
            "relevant_region_visible": True,
            "description": "Overexposed bright version.",
            "generator": make_overexposed,
        },
        {
            "case_id": "W5_IMG_006",
            "condition": "cropped",
            "filename": "spot_004_cropped.jpg",
            "relevant_region_visible": False,
            "description": "Cropped version; relevant region treated as not visible.",
            "generator": make_cropped,
        },
        {
            "case_id": "W5_IMG_007",
            "condition": "occluded",
            "filename": "spot_004_occluded.jpg",
            "relevant_region_visible": False,
            "description": "Occluded version; relevant region treated as not visible.",
            "generator": make_occluded,
        },
    ]

    manifest_rows = []

    for item in conditions:
        output_path = OUTPUT_DIR / item["filename"]
        degraded_image = item["generator"](base_image)
        save_image(degraded_image, output_path)

        manifest_rows.append(
            {
                "case_id": item["case_id"],
                "condition": item["condition"],
                "image_path": to_relative(output_path),
                "relevant_region_visible": str(
                    item["relevant_region_visible"]
                ).lower(),
                "description": item["description"],
            }
        )

        print(
            f"[OK] {item['condition']:<13} -> "
            f"{to_relative(output_path)}"
        )

    with MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_id",
                "condition",
                "image_path",
                "relevant_region_visible",
                "description",
            ],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    print()
    print(f"Manifest saved to: {to_relative(MANIFEST_PATH)}")
    print("Week 5 degradation image generation completed.")


if __name__ == "__main__":
    main()