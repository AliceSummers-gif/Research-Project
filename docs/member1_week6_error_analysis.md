# Member 1 — Week 6 Final Error Analysis

## 1. Purpose

The purpose of this final error analysis is to consolidate the main failure cases, limitations, stabilisation findings, and downstream effects identified during the development and evaluation of the Member 1 Visual Evidence Quality Module.

Member 1 is responsible for:

- customer claim parsing
- image-quality assessment
- image usability assessment
- providing structured visual-evidence quality signals to downstream modules

The final analysis combines findings from:

- Week 3 module stabilisation and evaluation
- Week 5 controlled image-degradation experiments


## 2. Final Member 1 Scope

The final Member 1 module contains two main components:

### Claim Processing

Implemented in:

`src/image_quality/claim_parser.py`

The claim parser extracts:

- product
- claimed defect
- claimed location

### Visual Evidence Quality Assessment

Implemented in:

`src/image_quality/quality.py`

The module assesses:

- blur
- lighting
- relevant-region visibility
- overall image usability

The main unified function is:

`assess_image_quality()`


## 3. Early Failure Case — Low Lighting Interfering with Blur Assessment

During the initial Week 3 evaluation, a dark hoodie image was manually labelled as clear but was predicted as slightly blurred.

Initial observations:

- Normal hoodie blur score: approximately 366.14
- Dark hoodie blur score: approximately 53.80

The image was not intentionally blurred.

The failure occurred because low lighting reduced visible contrast and edge information. The original blur assessment used Laplacian variance directly on the grayscale image.

Therefore, lighting conditions incorrectly influenced the blur score.

### Refinement

Histogram equalisation was added before Laplacian variance:

Image

→ Grayscale

→ Histogram Equalisation

→ Laplacian Variance

→ Blur Classification

This reduced the sensitivity of blur estimation to low-light conditions in the controlled dataset.


## 4. Early Failure Case — Occlusion Interfering with Blur Assessment

A partially occluded jacket produced another initial blur-classification mismatch.

Manual label:

`clear`

Initial prediction:

`slightly_blurred`

Observed scores:

- Normal jacket: approximately 200.40
- Occluded jacket: approximately 181.21

The image remained visually sharp, but the occlusion reduced the amount and distribution of high-frequency edge information.

Because the score was close to the original clear threshold, the image was incorrectly classified as slightly blurred.

### Refinement

Histogram equalisation and threshold recalibration improved separation between clear and blurred images in the controlled dataset.


## 5. Final Blur Thresholds

The final prototype blur thresholds are:

- `blur_score < 30` → `severely_blurred`
- `30 <= blur_score < 150` → `slightly_blurred`
- `blur_score >= 150` → `clear`

These thresholds are heuristic and were calibrated using the current controlled dataset.

They must not be interpreted as universal image-quality thresholds.


## 6. Week 3 Final Controlled Evaluation

After stabilisation, the controlled 10-image dataset produced:

- Blur accuracy: 10/10
- Lighting accuracy: 10/10
- Usability accuracy: 10/10

This represents 100% agreement with the manual labels on the current controlled dataset.

However, this should not be interpreted as 100% real-world accuracy because:

- the dataset contains only 10 images
- the same dataset was used to identify failures
- the same dataset influenced threshold refinement

Therefore, the result demonstrates prototype stability on the controlled evaluation set rather than generalisation.


## 7. Week 5 Downstream Degradation Analysis

Week 5 evaluated how image-quality degradation propagates through the full refund-decision pipeline.

Seven controlled conditions were tested using the same source stain image:

- clear
- slight blur
- severe blur
- dark
- overexposed
- cropped
- occluded


## 8. Mild Degradation Behaviour

The clear baseline produced:

- Member 1 image quality: 1.0
- Image usable: True
- Damage type: `stain_or_spot`
- Damage confidence: approximately 0.920
- Evidence confidence: 0.53
- Confidence label: `MEDIUM`

The slightly blurred image produced:

- Member 1 image quality: 1.0
- Image usable: True
- Damage type: `stain_or_spot`
- Damage confidence: approximately 0.943
- Evidence confidence: 0.53
- Confidence label: `MEDIUM`

Therefore, mild blur did not reduce downstream damage confidence in this single controlled example.

The small increase in damage confidence must not be interpreted as evidence that blur improves model performance.

It only indicates that mild degradation did not negatively affect this particular image.


## 9. Severe Degradation Behaviour

The following conditions were classified as unusable:

- severe blur
- dark
- overexposed
- cropped
- occluded

For these conditions:

- Member 1 image quality decreased to 0.0
- Member 1 image usability became False
- Member 2 evidence quality became `unusable`
- Member 2 damage type became `uncertain`
- Member 2 damage confidence decreased to 0.0
- Evidence confidence decreased to 0.17
- Confidence label changed to `LOW`
- Final decision became `REQUEST_MORE_EVIDENCE`

This demonstrates a clear safety-gating effect.

The system avoids making an automated refund decision when the visual evidence is not sufficiently usable.


## 10. Final Decision Interpretation

The clear and slightly blurred cases produced:

`HUMAN_REVIEW`

However, this result was not caused by image quality.

The recorded reason was:

`Refund-policy eligibility is not confirmed.`

This demonstrates that image quality is only one component of the complete refund decision.

Other evidence sources, including:

- order validation
- refund-policy eligibility
- evidence consistency
- refund risk

can independently affect the final outcome.

Therefore, Member 1 should be understood as an evidence-quality gate rather than the sole decision-maker.


## 11. Current Claim Parser Limitations

The current claim parser is keyword-based.

Known limitations include:

- limited synonym coverage
- limited support for spelling errors
- limited support for complex natural-language expressions
- only the first matching product is returned
- only the first matching defect is returned
- only the first matching location is returned
- no semantic language model is used
- no claim-parsing confidence score is produced

For the current prototype scope, this behaviour is acceptable because the claim parser is intended to provide simple structured fields to downstream modules.


## 12. Current Image Quality Module Limitations

### 12.1 Small Evaluation Dataset

The controlled image-quality evaluation contains only a small number of images.

The current thresholds have not been validated across:

- different camera devices
- different compression levels
- different backgrounds
- different clothing colours
- different fabrics
- different damage sizes
- different customer-upload environments

### 12.2 Heuristic Thresholds

Blur and lighting thresholds are manually calibrated prototype thresholds.

They may require recalibration when the dataset grows.

### 12.3 Relevant-Region Visibility Is Not Automatically Detected

The current prototype accepts:

`relevant_region_visible`

as an external boolean input.

The module does not automatically determine whether the relevant product or damage region is visible.

### 12.4 Cropping and Occlusion Are Not Separate Automatic Classifiers

Cropping and occlusion affect overall usability through the relevant-region signal.

The current prototype does not contain dedicated learned cropping or occlusion classifiers.

### 12.5 Image Loading Is Repeated

Several quality functions independently load the same image.

This is acceptable for the current prototype but is not computationally optimal.

A production implementation could load the image once and share the processed representation across quality functions.

### 12.6 Preprocessing Is Not Globally Enforced

`preprocess_image()` provides aspect-ratio-preserving resizing, but the complete quality pipeline does not force every assessment function to use the resized image.

This is acceptable for the current controlled prototype but could be standardised in a future version.


## 13. Damage Detection Dependency

Week 5 also revealed that the downstream zero-shot CLIP damage detector has class-specific limitations.

Some hole images were not correctly classified as `hole_or_tear` even under clear image conditions.

Therefore, damage-detection errors must not automatically be attributed to Member 1 image quality.

The final system evaluation should distinguish:

- image-quality failure
- damage-model classification failure
- evidence-integration failure
- policy or order validation failure


## 14. Final Error Categories

The final Member 1 error analysis identifies five broad categories:

### Category 1 — Image Quality Measurement Error

Example:

Low lighting initially reduced Laplacian variance and caused a clear image to appear blurred.

Mitigation:

Histogram equalisation and threshold recalibration.


### Category 2 — Evidence Visibility Failure

Examples:

- cropped image
- heavily occluded image

Effect:

Image becomes unusable and the system requests more evidence.


### Category 3 — Severe Lighting Failure

Examples:

- dark image
- overexposed image

Effect:

Image becomes unusable and downstream damage confidence is suppressed.


### Category 4 — Downstream Vision Model Error

Example:

A visually usable image may still be misclassified by the zero-shot CLIP damage detector.

Effect:

Damage classification or confidence may be incorrect even when Member 1 reports good image quality.


### Category 5 — Non-Visual Decision Constraint

Example:

Valid visual evidence can still result in `HUMAN_REVIEW` because refund-policy eligibility is unresolved.

Effect:

The final decision is not determined by image quality alone.


## 15. Final Safety Behaviour

The final architecture follows a conservative visual-evidence strategy:

Usable Image

→ Allow downstream visual analysis

Unusable Image

→ Suppress unreliable visual confidence

→ Prevent unsafe automation

→ Request additional evidence

This behaviour supports the wider project objective of risk-aware selective automation.


## 16. Final Conclusion

The Member 1 Visual Evidence Quality Module successfully provides a practical visual-evidence gate for the current refund-decision prototype.

The module was stabilised after identifying early blur-classification failures, and controlled experiments demonstrated how severe image degradation propagates into lower damage confidence, lower evidence confidence, and more conservative decisions.

The final prototype should therefore be described as:

- stable on the current controlled dataset
- suitable for integration with the multimodal refund prototype
- conservative when image evidence becomes unreliable
- not yet validated for real-world production deployment

The most important future improvements are:

- larger and more diverse evaluation datasets
- automatic relevant-region visibility detection
- dedicated cropping and occlusion assessment
- stronger semantic claim parsing
- broader validation of image-quality thresholds
- improved downstream damage detection