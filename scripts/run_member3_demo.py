"""Run the Member 3 order, policy, and evidence-verification demo."""

import json
from pathlib import Path
from pprint import pprint
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.schemas import CaseInput, Member1Output, Member2Output
from src.evidence.pipeline import build_evidence_chain


DEMO_CASE = PROJECT_ROOT / "data/test_cases/member3_week6_single_case.json"


def main() -> None:
    with DEMO_CASE.open(encoding="utf-8") as case_file:
        data = json.load(case_file)

    chain = build_evidence_chain(
        CaseInput(**data["case_input"]),
        Member1Output(**data["member1"]),
        Member2Output(**data["member2"]),
        data["request_date"],
    )

    print("\nMEMBER 3 — RETRIEVAL AND EVIDENCE VERIFICATION")
    print("\nInput")
    pprint(data["case_input"])
    print("\nRetrieved order")
    pprint(chain.order_evidence)
    print("\nRetrieved policy")
    pprint(chain.policy_evidence)
    print("\nVerified output")
    pprint(chain.member3_output)
    print("\nFeedback")
    print(chain.verified_evidence.reason)


if __name__ == "__main__":
    main()
