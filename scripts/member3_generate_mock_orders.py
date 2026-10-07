"""Build 70 traceable synthetic orders, one per available public image."""

import json
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDER_FILE = PROJECT_ROOT / "data/orders/orders.json"
IMAGE_ROOT = PROJECT_ROOT / "data/Week4_damage_dataset_v1/images"
TARGET_COUNT = 70

CATALOG = (
    ("Black Jacket", "Jacket", 129.0),
    ("Grey Hoodie", "Hoodie", 79.0),
    ("White T-Shirt", "T-Shirt", 35.0),
    ("Blue Jacket", "Jacket", 220.0),
    ("Green Hoodie", "Hoodie", 95.0),
    ("Red Jacket", "Jacket", 149.0),
    ("Black Hoodie", "Hoodie", 89.0),
    ("Navy T-Shirt", "T-Shirt", 42.0),
    ("Brown Jacket", "Jacket", 189.0),
    ("Cream Hoodie", "Hoodie", 110.0),
    ("Yellow T-Shirt", "T-Shirt", 39.0),
    ("Leather Jacket", "Jacket", 499.0),
)


def build_orders(seed_orders: list[dict]) -> list[dict]:
    """Preserve ORD001-ORD012 and deterministically add ORD013-ORD070."""

    original = seed_orders[:12]
    if len(original) != 12:
        raise ValueError("The generator requires the original 12 seed orders.")

    orders = list(original)
    start = date(2026, 6, 15)
    for number in range(13, TARGET_COUNT + 1):
        product_name, category, base_price = CATALOG[(number - 1) % len(CATALOG)]
        purchase_date = start + timedelta(days=(number * 3) % 75)
        status = "delivered"
        if number % 17 == 0:
            status = "cancelled"
        elif number % 13 == 0:
            status = "processing"

        orders.append(
            {
                "order_id": f"ORD{number:03d}",
                "product_name": product_name,
                "product_category": category,
                "price": round(base_price + (number % 5) * 4.0, 2),
                "purchase_date": purchase_date.isoformat(),
                "status": status,
                "final_sale": number % 11 == 0,
            }
        )
    return orders


def add_provenance(orders: list[dict]) -> list[dict]:
    """Mark transactions synthetic and attach each public image exactly once."""

    image_records = [
        (f"H{number:03d}", f"holes_35/hole_{number:03d}.jpg", "Garment_condition_holes")
        for number in range(1, 36)
    ] + [
        (f"S{number:03d}", f"spots_35/spot_{number:03d}.jpg", "Garment_condition_spots")
        for number in range(1, 36)
    ]
    enriched = []
    for index, order in enumerate(orders):
        record = dict(order)
        record["data_type"] = "synthetic_order"
        record["retailer"] = "H&M Australia"
        purchase = date.fromisoformat(record["purchase_date"])
        record["delivery_date"] = (purchase + timedelta(days=4)).isoformat()
        if index < len(image_records):
            source_id, relative_path, dataset = image_records[index]
            record["image_evidence"] = {
                "source_dataset": dataset,
                "source_image_id": source_id,
                "image_path": f"data/Week4_damage_dataset_v1/images/{relative_path}",
                "license": "CC BY 4.0",
                "attribution": "CISUTAC project - Wargon Innovation",
                "is_model_ground_truth": False,
            }
        else:
            record["image_evidence"] = None
        enriched.append(record)
    return enriched


def main() -> None:
    seed_orders = json.loads(ORDER_FILE.read_text(encoding="utf-8"))
    orders = add_provenance(build_orders(seed_orders))
    ORDER_FILE.write_text(json.dumps(orders, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(orders)} orders to {ORDER_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
