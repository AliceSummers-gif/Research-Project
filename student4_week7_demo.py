"""Compare rule and ML confidence on an existing structured case."""

import json
from pathlib import Path

from src.agent.agent import run_agent
from src.common.schemas import (
    Member1Output,
    Member2Output,
    Member3Output,
)


def main():
    project_root = Path(__file__).resolve().parent
    case_path = (
        project_root
        / "data"
        / "test_cases"
        / "student4_auto_refund.json"
    )

    raw = json.loads(
        case_path.read_text(encoding="utf-8")
    )

    member1 = Member1Output(**raw["member1"])
    member2 = Member2Output(**raw["member2"])
    member3 = Member3Output(**raw["member3"])

    for method in ("rule", "ml"):
        result = run_agent(
            member1,
            member2,
            member3,
            confidence_method=method,
        )

        print(f"\nConfidence method: {method}")
        print(
            json.dumps(
                result.model_dump(),
                indent=2,
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()