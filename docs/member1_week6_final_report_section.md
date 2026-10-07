# Member 1 — Final Report Section

## Visual Evidence Quality Assessment for Refund Decision-Making

### 1. Module Objective

The Member 1 component was designed to determine whether customer-provided visual evidence is sufficiently reliable for downstream refund assessment.

The module does not directly decide whether a refund should be approved. Instead, it performs an evidence-quality gating function before visual damage analysis and final refund decision-making.

The main responsibilities of Member 1 are:

- parsing structured information from the customer claim,
- assessing image blur,
- assessing lighting quality,
- incorporating relevant-region visibility,
- determining overall image usability, and
- providing structured visual-quality signals to downstream modules.

The final output is consumed by the shared multimodal refund pipeline, including damage detection, evidence confidence estimation, and the final risk-aware decision layer.


### 2. Claim Processing

Customer claim processing is implemented in:

`src/image_quality/claim_parser.py`

The parser extracts three structured fields:

- product,
- claimed defect,
- claimed location.

For example, the claim:

`The black jacket arrived with a tear on the left sleeve.`

is converted into:

```json
{
  "product": "jacket",
  "claimed_defect": "tear_hole",
  "claimed_location": "left_sleeve"
}
```

The current implementation is keyword-based and is intended as a lightweight prototype rather than a general natural-language understanding model.


### 3. Image Quality Assessment

The visual-evidence quality module is implemented in:

`src/image_quality/quality.py`

The final module evaluates three main factors:

1. blur,
2. lighting,
3. relevant-region visibility.

These signals are combined into an overall image-usability decision.


### 4. Blur Assessment

Blur is assessed using the variance of the Laplacian.

The initial implementation calculated Laplacian variance directly on the grayscale image.

During controlled evaluation, this approach produced two important failure cases:

- a dark but visually sharp hoodie was incorrectly classified as slightly blurred,
- a partially occluded but visually sharp jacket was also incorrectly classified as slightly blurred.

The analysis showed that lighting and occlusion could reduce high-frequency edge information and artificially lower the Laplacian score.

To improve stability, histogram equalisation was added before Laplacian variance calculation.

The final processing sequence is:

```text
Image
→ Grayscale
→ Histogram Equalisation
→ Laplacian Variance
→ Blur Classification
```

The final prototype thresholds are:

- `blur_score < 30` → `severely_blurred`
- `30 <= blur_score < 150` → `slightly_blurred`
- `blur_score >= 150` → `clear`

These thresholds are heuristic and were calibrated on the current controlled dataset.


### 5. Lighting Assessment

Lighting quality is assessed using:

- average grayscale brightness, and
- highlight ratio.

The lighting rules are:

- `brightness_score < 50` → `dark`
- `highlight_ratio > 0.05` → `overexposed`
- otherwise → `normal`

Using both brightness and highlight ratio avoids treating every naturally bright image as overexposed.

The current lighting thresholds are prototype heuristics and are not intended as universal thresholds.


### 6. Relevant-Region Visibility

The current prototype uses:

`relevant_region_visible`

as an explicit input signal.

If the relevant product or evidence region is not visible, the image is treated as unusable.

The current implementation does not automatically detect relevant-region visibility using a vision model.

This design keeps the Member 1 scope focused on evidence-quality assessment while allowing the downstream system to respond conservatively when important evidence is missing.


### 7. Image Usability Decision

The final image is considered unusable when one or more critical conditions occur.

Examples include:

- severe blur,
- insufficient lighting,
- overexposure,
- relevant evidence region not visible.

The unified function:

`assess_image_quality()`

returns structured signals including:

- `blur_score`
- `blur_label`
- `brightness_score`
- `highlight_ratio`
- `lighting_label`
- `relevant_region_visible`
- `image_usable`
- `usability_reason`

These outputs are passed to the Agent integration layer.


### 8. Agent Integration

The real Member 1 module is integrated through:

`src/agent/member1_adapter.py`

The main callable interface is:

`run_member1()`

The adapter:

- parses the customer claim,
- runs the real image-quality module,
- converts quality results into the shared `Member1Output`,
- preserves raw image-quality signals for downstream analysis.

The shared Agent pipeline calls the real Member 1 adapter before damage detection.

The resulting flow is:

```text
CaseInput
→ Member 1
→ Member 2 Damage Detection
→ Evidence Chain
→ Evidence Confidence
→ Refund Risk
→ Final Decision
```


### 9. Controlled Evaluation

The stabilised image-quality module was evaluated on a controlled 10-image dataset.

Before stabilisation:

- Blur accuracy: 80.0%
- Lighting accuracy: 100.0%
- Usability accuracy: 100.0%

After histogram equalisation and threshold refinement:

- Blur accuracy: 100.0%
- Lighting accuracy: 100.0%
- Usability accuracy: 100.0%

The final result represents agreement with the manual labels on the current controlled dataset.

It must not be interpreted as 100% real-world accuracy because the dataset is small and was also used during failure analysis and threshold refinement.


### 10. Image-Degradation Experiment

A separate controlled experiment was conducted to study how image degradation affects downstream refund decision-making.

The same stain image was used across seven conditions:

- clear,
- slight blur,
- severe blur,
- dark,
- overexposed,
- cropped,
- occluded.

This design kept the source visual evidence constant while changing image quality.


### 11. Mild Degradation Results

For the clear image:

- Member 1 image quality: `1.0`
- Image usable: `True`
- Damage type: `stain_or_spot`
- Damage confidence: approximately `0.920`
- Evidence confidence: `0.53`
- Confidence label: `MEDIUM`

For the slightly blurred image:

- Member 1 image quality: `1.0`
- Image usable: `True`
- Damage type: `stain_or_spot`
- Damage confidence: approximately `0.943`
- Evidence confidence: `0.53`
- Confidence label: `MEDIUM`

In this single controlled example, mild blur did not reduce downstream damage confidence.

The small increase in confidence should not be interpreted as evidence that blur improves model performance.


### 12. Severe Degradation Results

The following conditions were classified as unusable:

- severe blur,
- dark,
- overexposed,
- cropped,
- occluded.

Across these conditions:

- Member 1 image quality decreased to `0.0`,
- image usability became `False`,
- Member 2 evidence quality became `unusable`,
- damage type became `uncertain`,
- damage confidence decreased to `0.0`,
- evidence confidence decreased from `0.53` to `0.17`,
- confidence label changed from `MEDIUM` to `LOW`,
- final decision became `REQUEST_MORE_EVIDENCE`.

This demonstrates that severe image degradation propagates through the multimodal evidence pipeline and leads to more conservative system behaviour.


### 13. Final Decision Interpretation

The clear and slightly blurred conditions resulted in:

`HUMAN_REVIEW`

However, this decision was not caused by image quality.

The recorded reason was:

`Refund-policy eligibility is not confirmed.`

This result demonstrates an important property of the proposed architecture:

good visual evidence does not automatically lead to a refund.

The final decision also depends on:

- order validity,
- policy eligibility,
- evidence consistency,
- evidence confidence,
- refund risk.

Therefore, Member 1 functions as one part of a wider evidence chain rather than as an independent refund decision-maker.


### 14. Error Analysis

The development process identified several important error categories.

#### 14.1 Image Quality Measurement Error

Low lighting and occlusion initially affected Laplacian-based blur scores.

Mitigation:

Histogram equalisation and threshold refinement.


#### 14.2 Evidence Visibility Failure

Cropped or occluded images may be technically sharp while still failing to show the required evidence.

Mitigation:

Use relevant-region visibility as part of the usability gate.


#### 14.3 Severe Lighting Failure

Dark and overexposed images are rejected when visual details cannot be assessed reliably.

Mitigation:

Mark evidence as unusable and request better evidence.


#### 14.4 Downstream Damage-Model Error

A visually usable image may still be incorrectly classified by the zero-shot damage detector.

This error is separate from Member 1 image-quality failure.


#### 14.5 Non-Visual Decision Constraints

Good image evidence may still lead to human review because of policy, order, consistency, or risk constraints.


### 15. Limitations

The final Member 1 prototype has several limitations.

First, the controlled evaluation dataset is small and does not represent the full diversity of real customer-uploaded images.

Second, blur and lighting thresholds are heuristic and may require recalibration on larger datasets.

Third, relevant-region visibility is supplied explicitly rather than detected automatically.

Fourth, dedicated automatic cropping and occlusion classifiers are not implemented.

Fifth, the claim parser uses keyword matching and has limited semantic-language capability.

Sixth, the image-degradation experiment uses one primary damage image and synthetically generated degradations.

Finally, the downstream zero-shot CLIP damage detector has its own class-specific limitations, meaning that not every visual-classification failure should be attributed to Member 1.


### 16. Contribution to Risk-Aware Selective Automation

The main contribution of the Member 1 module is not damage recognition itself.

Its role is to determine whether visual evidence is sufficiently trustworthy to continue through the automated decision pipeline.

The resulting behaviour is:

```text
Reliable Visual Evidence
→ Continue Automated Analysis

Unreliable Visual Evidence
→ Reduce Evidence Confidence
→ Prevent Unsafe Automation
→ Request More Evidence
```

This design supports the broader project objective of risk-aware selective automation.


### 17. Final Outcome

The final Member 1 Visual Evidence Quality Module provides:

- structured customer-claim information,
- stabilised blur assessment,
- lighting assessment,
- evidence-region visibility handling,
- image-usability decisions,
- Agent-compatible structured outputs,
- controlled evaluation results,
- downstream image-degradation analysis,
- documented failure cases and limitations.

The final module is suitable for the current research prototype and demonstrates conservative behaviour when customer-provided visual evidence becomes unreliable.

It should be described as a controlled research prototype rather than a production-ready image-quality system.