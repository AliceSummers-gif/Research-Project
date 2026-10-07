# Student 4 Week 9: Final error analysis and refinement

## Scope and provenance

This release integrates the current group main (d220e36, Member 2 Week 9), the previous Student 4 Week 8/Streamlit work, and the Week 9 conservative decision profile. Week 8 files and run_agent baseline behavior remain unchanged. The final end-to-end pipeline calls run_final_agent; the public Streamlit workflow continues to use rule confidence, while the local pipeline supports ML with the new safeguard.

Evaluation reuses 10 validation and 6 test scenarios from Week 8. Their labels follow the original rule rubric. These are synthetic structured evidence, not image-level ground truth. Test cases were already inspected in Week 8 and cannot be presented as a fresh independent benchmark. No new LLM collection or model training was performed.

## Error analysis

- Incorrect automatic refunds: baseline ML produced AUTO_REFUND for validation V07 (ML 0.83, weighted evidence 0.70) and V08 (ML 0.97, weighted evidence 0.79). Original labels request further evidence. The saved Week 8 threshold experiment reduced this to one error at ML threshold 0.90; V08 persisted. A high ML score is insufficient corroboration of evidence strength.
- Unnecessary human reviews: none relative to the fixed labels in these scenarios. This does not quantify real-world unnecessary review rates. Real image cases may legitimately need review because product identity/location are missing, policy eligibility is unconfirmed, or visual verification abstains.
- Unnecessary evidence requests: none relative to the fixed labels in the final profile. Conservative safeguards could increase this rate on unseen cases; that tradeoff requires independent labelled evaluation.
- Visual classification: user-observed jacket examples were classified as stain_or_spot despite a reported tear or no visible damage. They are qualitative observations, not a measured image accuracy experiment. Verification compares the prediction with the parsed claim; it does not correct the detector.
- Integration: the old cloud test treated claim_image_consistency as always missing. Member 2 Week 9 now assigns a negative result for a confident damage-type mismatch. The updated test checks consistency=0 while product identity and damage location remain missing.

## Refinement

Keep all existing quality, visibility, order, policy, and review overrides. An ML candidate AUTO_REFUND now also requires ML confidence >=0.90 and weighted rule confidence >=0.80. Otherwise it becomes REQUEST_MORE_EVIDENCE. This guard never upgrades a review or evidence request into an automatic refund. Rule-mode behavior is unchanged. The guard is motivated by validation V08, not selected using new test cases.

The corroborating rule score intentionally makes this a conservative hybrid, not an independent ML method. Agreement with rule-derived labels is partly expected by design. Scores remain model/evidence scores, not calibrated probabilities of refund eligibility.

## Re-run results

| Split | Profile | Rule matches | ML matches | ML incorrect automatic refunds |
|---|---|---:|---:|---:|
| Validation (10) | Original baseline (0.80) | 10/10 | 8/10 | 2 |
| Validation (10) | Final conservative | 10/10 | 10/10 | 0 |
| Reused test (6) | Original baseline | 6/6 | 6/6 | 0 |
| Reused test (6) | Final conservative | 6/6 | 6/6 | 0 |

All four evaluations per split have zero unnecessary reviews; final evaluations have zero unnecessary evidence requests relative to these labels. Raw cases, reasons, error counts, input/model/source hashes, and Python version are in data/results/student4_week9/final_comparison.json. Reproduce from the project root: python -m scripts.student4_week9_evaluate. Week 8 results are not overwritten. Historical manual LLM results remain in the Week 8 report with their provenance limitations; no final LLM reliability claim is made.

## Website refinements

The result page separates model damage prediction, location, verification verdict/reason, usable-photo status, order/policy checks, and missing evidence. A negative verdict is distinct from an ambiguous or missing result. Review choices and history actions use readable English. English date selectors are retained. Review approvals remain demonstration actions and preserve original assessments and unresolved evidence. No payments, reviewer authentication, cross-browser record sharing, or permanent cloud storage are added.

## Validation and remaining acceptance

Before this update, the user ran the integrated suite: 130 passed, 40 dependency deprecation warnings. Added regression checks cover the ML threshold boundaries, policy/image/review overrides, and presentation of negative versus unknown verification. Workspace validation excludes the HTTP socket test because the sandbox prevents local socket binding; it must be included in the user's final local run. Controlled backend tests do not measure CLIP accuracy. Initial and controlled-result Streamlit pages are checked with AppTest; a new real-image cloud deployment is not claimed.

Before publication: run the complete suite in the Desktop checkout, preview the updated Streamlit page, commit/push this update, merge the group PR after review, and update the personal fork deployment branch. Preserve existing deployment configuration until these steps complete. Record the final deployed commit and actual cloud acceptance separately.

## Suggested demonstration

Use clearly marked structured fixtures to illustrate all three automated branches. Use an unannotated real photo to show model prediction and unresolved evidence; do not promise an automatic refund. Demonstrate role-play review, simulated confirmation, and record download. Keep the original assessment visible. Records belong to one browser session and may disappear on refresh/restart.
