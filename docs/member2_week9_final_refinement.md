# Member 2 — Week 9 final refinement

Owner: Hangyi Zhang (Student 2 / Member 2)

## Final module scope

Member 2 supplies two bounded functions for the refund workflow:

1. `DamageDetector` classifies visible garment evidence as `hole_or_tear`,
   `stain_or_spot`, `no_damage`, or `uncertain`.
2. `verify_claim` compares a parsed defect claim (and a location when both sides
   provide one) with that visual output. It returns `positive`, `negative`, or
   `ambiguous`, plus an auditable reason code and a claim-image score.

This is not product-to-order verification; that remains Member 3's scope. A
score of `1.0` or `0.0` is a categorical evidence result, not a calibrated
probability. Ambiguous evidence keeps the score as `null` and requires human
review.

## What was refined

- Restored the Claim–Image Verification implementation required by the existing
  Week 5 evaluator, so the evaluator is importable and reproducible again.
- Added focused regression tests for supported evidence, concrete contradiction,
  low-confidence abstention, and a location-specific claim with missing location
  evidence.
- Added `scripts/member2_week9_demo.py`, which displays examples and metrics
  from the committed Week 5 results only. It does **not** run a model or produce
  new measurements.

Run the checks from the repository root:

```text
python -m pytest tests/test_member2_damage.py tests/test_member2_week5_evaluate.py tests/test_member2_week9_refinement.py -q
python -m scripts.member2_week9_demo
python -m scripts.member2_week5_evaluate --backend none --output-dir <new-output-directory>
```

The last command is an honest preflight inventory. Re-running measured CLIP or
YOLO evaluation requires the actual model/cache or the actual YOLO weights; it
must not overwrite the recorded Week 5 baseline unless a new run is intended.

## Evidence used for final analysis

All metrics below are copied from the committed, executed Week 5 CLIP baseline
in `data/member2/week5/`; no metric was re-estimated in Week 9.

| Evaluation | Executed | Accuracy | Macro F1 | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Damage detection | 70 | 34.29% | 26.15% | Not reliable as an automated classifier. |
| Claim–image verification | 70 | 22.86% | 31.56% | Must remain review-assisted. |

The manifest contains 100 cases across 70 source-image groups. Only 70 source
images were materialized and executed. The other 30 are recipe-only ambiguous
variants and were excluded from predictions, metrics, and confusion matrices.
This is deliberate: variants of a source image cannot be treated as independent
observations, and a non-existent image cannot be evaluated.

## Failure-case synthesis from the recorded output

The Week 5 failure queue contains 58 executed cases that had a damage error, a
claim-verification error, or a human-review flag. Its rows are observed output,
not hand-authored model labels.

### Damage patterns

| Ground-truth visual class | Recorded predictions | Finding |
| --- | --- | --- |
| hole/tear (25) | 15 stain, 5 no-damage, 5 uncertain | Hole/tear recall was 0%; this is the principal detector weakness. |
| stain/spot (25) | 20 stain, 1 hole/tear, 2 no-damage, 2 uncertain | Stain recall was 80%, but false negatives and abstentions remain. |
| provisional no-damage (20) | 4 no-damage, 16 stain | Clean-control recall was 20%; these controls are provisional and should not support a production no-damage claim. |

### Verification patterns

Of the 70 executed cases, the reason codes were 40 `visual_review_required`,
16 `damage_type_mismatch`, and 14 `damage_type_matches`. Against the recorded
claim labels, the 40 positive cases became 10 positive, 10 negative, and 20
ambiguous; the 30 negative cases became 4 positive, 6 negative, and 20
ambiguous. The dominant limitation is therefore upstream visual uncertainty or
misclassification, not a reason to silently turn uncertain evidence into a
negative decision.

## Demonstrable safety behavior

- An unusable image, a hidden relevant region, `uncertain` damage, or confidence
  below 0.70 becomes `ambiguous` and `needs_human_review=True`.
- A concrete high-confidence damage-type mismatch is a structured `negative`,
  preserving the detector result and reason code.
- A location-specific claim cannot be automatically supported when the detector
  does not provide a sufficiently specific location.
- The demo selects one recorded supported claim, one recorded contradiction, and
  one recorded human-review case so reviewers can inspect real output without
  claiming a fresh inference run.

## Remaining evidence needed before a stronger model claim

1. Materialize the 30 blur/crop/occlusion/contrast variants and evaluate them
   as grouped derivatives of their source images.
2. Add independently sourced clean garments before asserting `no_damage`
   performance.
3. Train and evaluate the YOLO candidate with source-image-group separation;
   report its actual held-out metrics next to, rather than combined with, the
   recorded CLIP baseline.
4. Obtain visual location annotations if location-specific automatic decisions
   are required. Until then the module correctly abstains.

The current module is therefore appropriate for evidence triage and transparent
human review, not autonomous refund approval.
