"""Generate the deterministic Member 3 Week 8 RAG evaluation dataset."""

import json
from pathlib import Path


OUTPUT = Path("data/test_cases/member3_week8_rag_evaluation.json")


POLICY_QUERIES = {
    "POL-DAMAGE-30": [
        "The black jacket arrived with a tear on the left sleeve.",
        "There is a visible hole in the hoodie fabric.",
        "My shirt was delivered with a dark stain on the front.",
        "The zipper on the jacket arrived broken.",
        "I found ripped fabric near the coat pocket.",
        "The garment has a spot that was present at delivery.",
        "A seam opened and left a hole in my new jacket.",
        "The delivered clothing has torn material around the sleeve.",
        "My hoodie arrived damaged with a visible rip.",
        "The shirt has a permanent stain straight out of the parcel.",
        "The jacket zip does not work because it is broken.",
        "I received clothing with damaged and torn fabric.",
        "The product photo shows a hole in the ordered jacket.",
        "A visible spot and fabric damage appeared on arrival.",
        "The sleeve tear is clearly visible in the submitted image.",
    ],
    "POL-WRONG-ITEM-14": [
        "I ordered a jacket but received a shirt.",
        "The product in my parcel is not the item I ordered.",
        "An incorrect hoodie was delivered for this order.",
        "The received colour and product do not match my order.",
        "I was sent the wrong item in the package.",
        "The order record says jacket but the parcel contains trousers.",
        "This delivered product belongs to a different order.",
        "I received another customer's item by mistake.",
        "The item shown in my photo does not match the purchased product.",
        "The retailer delivered an incorrect product.",
        "My order was for a hoodie and I received shorts.",
        "Wrong size and wrong product were sent in the parcel.",
        "The label and item are different from my order confirmation.",
        "I need a refund because the delivered item is not mine.",
        "The package contains a product mismatch.",
    ],
    "POL-NO-DAMAGE": [
        "The submitted photo shows no visible damage.",
        "I cannot identify a hole, tear or stain in the image.",
        "The garment appears clean and undamaged.",
        "There is no damage visible on the product.",
        "The clothing looks intact in every submitted photo.",
        "No defect can be seen in the evidence.",
        "The jacket is not damaged according to the image.",
        "The claim says damage but the product looks normal.",
        "The fabric has no visible hole or mark.",
        "The evidence shows an undamaged item.",
        "No stain is present in the supplied photograph.",
        "The shirt appears intact without a tear.",
        "The photo does not support a visible-damage claim.",
        "Nothing in the image indicates product damage.",
        "The item is clean, intact and shows no defect.",
    ],
    "POL-FINAL-SALE": [
        "The item was marked final sale when I purchased it.",
        "I want to return a final-sale product.",
        "The order contains a clearance item excluded from refunds.",
        "This purchase was sold as final sale.",
        "The product is a sale item with a refund exclusion.",
        "I changed my mind about an item marked final sale.",
        "The receipt identifies this product as final sale.",
        "Can I refund a product that was excluded at checkout?",
        "The discounted item was labelled non-refundable.",
        "This clearance purchase has a final-sale condition.",
        "The return request concerns an excluded sale product.",
        "I bought this from the final-sale section.",
        "The order states that the product cannot be returned.",
        "The item was sold with a no-refund final-sale label.",
        "A final sale exclusion applies to this purchase.",
    ],
}


def build_cases() -> list[dict[str, object]]:
    cases = []
    index = 1
    for policy_id, queries in POLICY_QUERIES.items():
        for query in queries:
            cases.append(
                {
                    "case_id": f"M3_W8_{index:03d}",
                    "query": query,
                    "expected_policy_id": policy_id,
                    "dataset_type": "synthetic_labelled_evaluation",
                }
            )
            index += 1
    return cases


def main() -> None:
    cases = build_cases()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(cases)} cases to {OUTPUT}")


if __name__ == "__main__":
    main()
