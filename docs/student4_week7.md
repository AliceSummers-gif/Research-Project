# Student 4 Week 7: End-to-End Agent V1

## Objective

Connect the real Member 1 image-quality module, Member 2 damage
detector, Member 3 evidence chain and Student 4 decision Agent.

The Agent returns one of:
- AUTO_REFUND
- REQUEST_MORE_EVIDENCE
- HUMAN_REVIEW

These are prototype decisions. The system does not transfer money.

## Pipeline

Entry point: `src/agent/pipeline.py::run_pipeline`

1. Parse the claim and assess a real image.
2. Run damage detection using the image-usability result.
3. Retrieve the order and refund policy.
4. Verify the evidence chain.
5. Calculate rule-based or ML evidence confidence.
6. Calculate refund risk and apply decision rules.
7. Return intermediate evidence and the final decision.

V1 accepts exactly one image. Region visibility must be supplied
explicitly; it is not automatically detected.

Run commands from the project root.

## Confidence Modes

The existing `run_agent` function defaults to rule-based confidence
for compatibility. The new `run_pipeline` function defaults to ML.

The ML mode reuses the Week 6 saved model. No retraining was performed
for this integration.

The Week 6 model was trained on synthetic prototype data. Its output
must not be described as a calibrated real-world reliability guarantee.

The Member 1 adapter introduces provisional label-to-score mappings:
- Clear: 1.0; slightly blurred: 0.5; severely blurred: 0.0.
- Normal lighting: 1.0; dark or overexposed: 0.0.
- Image quality uses the lower score and is zero for unusable images.

These mappings require evaluation with representative real evidence.

## Missing Evidence and Review Rules

Missing claim-image consistency remains missing in the original
Member 2 output. Rule-based scoring gives that feature zero credit.

Poor or unusable visual evidence and Member 2 review flags are handled
before the final confidence-risk matrix, subject to earlier image,
order and policy checks.

Policy eligibility not being confirmed currently triggers HUMAN_REVIEW
before the later missing-consistency rule. Consequently, the integrated
missing-consistency case may return HUMAN_REVIEW.

## Member 3 Integration Fixes

- Do not use the product parsed from the customer's claim as a substitute
  for a visually detected product.
- Empty detected-product values receive an image-order match score of zero.
- Absent or null claim-image consistency does not confirm eligibility.
- Missing consistency does not count as complete evidence.

The 12 legacy Member 3 mock cases now explicitly include a synthetic
consistency input of 1.0, which makes their previous implicit assumption
visible. These are controlled test inputs, not model measurements.

## Validation

Run all tests:

```bash
python -m pytest -q
```

Run the real end-to-end demonstration:

```bash
python student4_week7_end_to_end_demo.py
```

The demonstration uses a historical request date of 2026-08-15.
Actual applications must supply their real request date.

Pipeline routing tests use controlled synthetic damage outputs and
real project image-quality, retrieval, verification and decision code.
They cover all three decision branches, missing consistency and the
single-image restriction. They do not measure visual model accuracy.

The real CLIP demonstration has also been run separately.

## Current Limitations

- The current CLIP detector does not supply detected product, damage
  location or claim-image consistency in the demonstrated case.
- This integration preserves those gaps; it does not invent evidence.
- Missing evidence prevents confirmation of automatic-refund eligibility.
- Orders and policies are local prototype datasets.
- Missing or unreadable image files raise errors.
- Multiple images are rejected by V1.
- Some model-loading tests emit dependency deprecation warnings.
- Controlled branch tests do not establish real-world refund accuracy.

## Next Steps

Coordinate with Member 2 on product identification and claim-image
verification. Evaluate the confidence mappings and decision thresholds
during the Week 8 experiments.