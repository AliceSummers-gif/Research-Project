# Research Project

Project skeleton for a risk-aware refund AI system.

## Structure

- `data/`: images, claims, policies, and orders
- `src/image_quality/`: image quality assessment
- `src/damage_detection/`: damage detection
- `src/evidence/`: retrieval, order evidence, and verification
- `src/decision/`: confidence, risk, and decision logic
- `src/agent/`: workflow agent
- `notebooks/`: research notebooks
- `tests/`: automated tests
- `app/`: application entry points

## Member 3 - Final Retrieval and Evidence Layer

Member 3 retrieves mock orders and policies, verifies evidence completeness
and policy eligibility, and supplies traceable features to the decision agent.
The demo order source contains 120 synthetic records while preserving the
original 12 order IDs used by existing integration tests.
The final Week 9 evaluation compares the frozen lexical baseline with the
intent-aware retriever, validates 120 balanced evidence cases, and retains the
12-case legacy regression. See
`docs/member3_week9_final_report.md` and reproduce the saved results with:

```bash
python3 -B scripts/member3_week9_final_evaluation.py
```

The evaluation uses controlled synthetic data and must not be interpreted as
real-world refund accuracy.
