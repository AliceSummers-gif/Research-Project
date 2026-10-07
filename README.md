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

## Member 2 — Damage Detection V1

Hangyi Zhang's Week 2 image-only damage detector is in `src/damage_detection/`.
It uses the shared `Member2Output` schema, preserves the Week 1 damage labels,
and routes poor evidence or low-confidence predictions to human review. See
`docs/member2_week2.md`. GitHub Actions runs its tests and the free CLIP
full-image-plus-YOLO-crop evaluation on `student2-week5`.
The recorded baseline result is in `data/member2/week2/results/`; it documents
good stain detection but inadequate hole recall and the planned detector
upgrade without introducing Week 3 claim verification.
The optional `Week 2 YOLO training` workflow is manual so model training does
not consume GitHub Actions time on every code push.

## Member 3 - Final Retrieval and Evidence Layer

Member 3 retrieves mock orders and policies, verifies evidence completeness
and policy eligibility, and supplies traceable features to the decision agent.
The final Week 9 evaluation compares the frozen lexical baseline with the
intent-aware retriever, validates 120 balanced evidence cases, and retains the
12-case legacy regression. See
`docs/member3_week9_final_report.md` and reproduce the saved results with:

```bash
python3 -B scripts/member3_week9_final_evaluation.py
```

The evaluation uses controlled synthetic data and must not be interpreted as
real-world refund accuracy.
