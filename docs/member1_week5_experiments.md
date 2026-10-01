# Member 1 Week 5 Image Quality Experiments

## 1. Objective

The objective of Week 5 is to measure how controlled image-quality degradation affects damage detection, evidence confidence, and the final refund decision.

The same source damage image is used for all experimental conditions so that image quality is the main controlled variable.

## 2. Experiment Setup

- Total conditions: 7
- Order ID: ORD003
- Request date: 2026-08-15
- Claim: The t-shirt has a stain on the front.

Controlled image conditions:

- clear
- slight_blur
- severe_blur
- dark
- overexposed
- cropped
- occluded

## 3. Experimental Results

| Case ID | Condition | Image Quality | Image Usable | Blur | Lighting | Damage Type | Damage Confidence | Evidence Confidence | Confidence Label | Final Decision |
| --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| W5_IMG_001 | clear | 1.0 | True | clear | normal | stain_or_spot | 0.919710620070234 | 0.53 | MEDIUM | HUMAN_REVIEW |
| W5_IMG_002 | slight_blur | 1.0 | True | clear | normal | stain_or_spot | 0.942512544064662 | 0.53 | MEDIUM | HUMAN_REVIEW |
| W5_IMG_003 | severe_blur | 0.0 | False | severely_blurred | normal | uncertain | 0.0 | 0.17 | LOW | REQUEST_MORE_EVIDENCE |
| W5_IMG_004 | dark | 0.0 | False | clear | dark | uncertain | 0.0 | 0.17 | LOW | REQUEST_MORE_EVIDENCE |
| W5_IMG_005 | overexposed | 0.0 | False | clear | overexposed | uncertain | 0.0 | 0.17 | LOW | REQUEST_MORE_EVIDENCE |
| W5_IMG_006 | cropped | 0.0 | False | clear | normal | uncertain | 0.0 | 0.17 | LOW | REQUEST_MORE_EVIDENCE |
| W5_IMG_007 | occluded | 0.0 | False | clear | normal | uncertain | 0.0 | 0.17 | LOW | REQUEST_MORE_EVIDENCE |

## 4. Decision Counts

- HUMAN_REVIEW: 2
- REQUEST_MORE_EVIDENCE: 5

## 5. Confidence Labels

- MEDIUM: 2
- LOW: 5

## 6. Damage Detection Results

- stain_or_spot: 2
- uncertain: 5

## 7. Interpretation

The controlled experiment shows a clear difference between mild and severe image degradation.

The clear baseline remained usable and produced a correct `stain_or_spot` prediction with a damage confidence of approximately 0.920. The slightly blurred version also remained usable and produced a correct `stain_or_spot` prediction with a damage confidence of approximately 0.943.

Therefore, in this single controlled case, mild blur did not reduce damage-detection confidence. The small increase from approximately 0.920 to 0.943 should not be interpreted as evidence that blur improves model performance. It only shows that mild degradation did not negatively affect this particular image.

For severe degradation conditions, including severe blur, darkness, overexposure, cropping, and occlusion, Member 1 classified the image as unusable. This triggered the Member 2 evidence-quality safety gate.

As a result:

- Member 1 image quality decreased from 1.0 to 0.0.
- Member 2 damage confidence decreased from approximately 0.92–0.94 to 0.0.
- Evidence confidence decreased from 0.53 (`MEDIUM`) to 0.17 (`LOW`).
- The final decision changed to `REQUEST_MORE_EVIDENCE`.

The clear and slightly blurred cases produced `HUMAN_REVIEW`, but this was not caused by image quality. Their decision reason was:

`Refund-policy eligibility is not confirmed.`

Therefore, the Week 5 experiment demonstrates that severe image-quality degradation can propagate through the multimodal refund pipeline by reducing image usability, suppressing downstream damage confidence, lowering overall evidence confidence, and causing the system to request additional evidence.

The experiment also shows that final decisions can still be affected by non-image factors such as refund-policy eligibility. This is important because image quality should not be treated as the only determinant of the final refund outcome.

## 8. Limitations

- The experiment uses one primary damage image.
- Image degradations are synthetically generated.
- The CLIP damage detector is a zero-shot prototype.
- Member 1 image-quality thresholds remain heuristic.
- Relevant-region visibility for cropped and occluded conditions is provided explicitly.
- The experiment does not demonstrate real-world model generalisation.

## 9. Output Files

- Detailed CSV: `data/member1/week5/results/week5_experiment_results.csv`
- Summary JSON: `data/member1/week5/results/week5_experiment_summary.json`
- Degradation manifest: `data/member1/week5/degradation_manifest.csv`

