"""Expand the Member 3 seed order database to 120 synthetic records."""

import json
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDER_FILE = PROJECT_ROOT / "data/orders/orders.json"
TARGET_COUNT = 120

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
    """Preserve ORD001-ORD012 and deterministically add ORD013-ORD120."""

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


def main() -> None:
    seed_orders = json.loads(ORDER_FILE.read_text(encoding="utf-8"))
    orders = build_orders(seed_orders)
    ORDER_FILE.write_text(json.dumps(orders, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(orders)} orders to {ORDER_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
