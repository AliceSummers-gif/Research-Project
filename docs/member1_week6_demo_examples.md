# Member 1 — Week 6 Demo Examples

## 1. Purpose

This document provides representative demonstration examples for the final Member 1 Visual Evidence Quality Module.

The examples illustrate how image-quality conditions affect:

- claim processing
- image usability
- downstream damage detection
- evidence confidence
- final decision behaviour

The examples are based on the controlled evaluation and experiment results produced during Weeks 3 and 5.


## 2. Demo Example A — Clear Usable Image

### Scenario

Customer claim:

`The t-shirt has a stain on the front.`

Image condition:

`clear`

Expected Member 1 behaviour:

- Image is clear
- Lighting is normal
- Relevant region is visible
- Image is usable

### Member 1 Output

Representative result:

```json
{
  "image_quality": 1.0,
  "blur_label": "clear",
  "lighting_label": "normal",
  "relevant_region_visible": true,
  "image_usable": true
}
```

### Downstream Result

Week 5 controlled experiment:

- Damage type: `stain_or_spot`
- Damage confidence: approximately `0.920`
- Evidence confidence: `0.53`
- Confidence label: `MEDIUM`
- Final decision: `HUMAN_REVIEW`

### Interpretation

The image quality is sufficient for downstream analysis.

The final `HUMAN_REVIEW` result is not caused by image quality.

The recorded downstream reason is:

`Refund-policy eligibility is not confirmed.`

This demonstrates that Member 1 acts as an evidence-quality gate rather than the sole refund decision-maker.


## 3. Demo Example B — Slightly Blurred but Still Usable

### Scenario

The same source image is mildly blurred.

Image condition:

`slight_blur`

### Member 1 Behaviour

Representative result:

```json
{
  "image_quality": 1.0,
  "image_usable": true
}
```

The image remains usable because the blur does not exceed the severe-blur threshold.

### Downstream Result

- Damage type: `stain_or_spot`
- Damage confidence: approximately `0.943`
- Evidence confidence: `0.53`
- Confidence label: `MEDIUM`
- Final decision: `HUMAN_REVIEW`

### Interpretation

In this single controlled example, mild blur did not reduce damage-detection confidence.

The slight increase from approximately `0.920` to `0.943` should not be interpreted as evidence that blur improves model performance.

The correct conclusion is only that mild blur did not negatively affect this image.


## 4. Demo Example C — Severe Blur

### Scenario

The source image is strongly blurred.

Image condition:

`severe_blur`

### Member 1 Behaviour

Representative output:

```json
{
  "blur_label": "severely_blurred",
  "image_quality": 0.0,
  "image_usable": false,
  "usability_reason": "severely_blurred"
}
```

### Downstream Result

- Member 2 evidence quality: `unusable`
- Damage type: `uncertain`
- Damage confidence: `0.0`
- Evidence confidence: `0.17`
- Confidence label: `LOW`
- Final decision: `REQUEST_MORE_EVIDENCE`

### Interpretation

Severe blur causes the visual evidence to fail the Member 1 usability gate.

The system does not continue treating the visual evidence as reliable.

Instead, downstream visual confidence is suppressed and the customer is asked to provide better evidence.


## 5. Demo Example D — Dark Image

### Scenario

The source image is significantly underexposed.

Image condition:

`dark`

### Member 1 Behaviour

Representative output:

```json
{
  "lighting_label": "dark",
  "image_quality": 0.0,
  "image_usable": false,
  "usability_reason": "insufficient_lighting"
}
```

### Downstream Result

- Damage type: `uncertain`
- Damage confidence: `0.0`
- Evidence confidence: `0.17`
- Confidence label: `LOW`
- Final decision: `REQUEST_MORE_EVIDENCE`

### Interpretation

Poor lighting prevents reliable visual evidence assessment.

The architecture responds conservatively rather than attempting an automated refund decision using unreliable evidence.


## 6. Demo Example E — Overexposed Image

### Scenario

The source image contains excessive brightness and highlight clipping.

Image condition:

`overexposed`

### Member 1 Behaviour

Representative output:

```json
{
  "lighting_label": "overexposed",
  "image_quality": 0.0,
  "image_usable": false,
  "usability_reason": "overexposed"
}
```

### Downstream Result

- Damage confidence: `0.0`
- Evidence confidence: `0.17`
- Confidence label: `LOW`
- Final decision: `REQUEST_MORE_EVIDENCE`

### Interpretation

The system treats severe overexposure as insufficient visual evidence and requests another image.


## 7. Demo Example F — Cropped Relevant Region

### Scenario

The image is cropped so that the relevant evidence region is not sufficiently visible.

Image condition:

`cropped`

Input:

```text
relevant_region_visible = false
```

### Member 1 Behaviour

Representative output:

```json
{
  "relevant_region_visible": false,
  "image_quality": 0.0,
  "image_usable": false,
  "usability_reason": "relevant_region_not_visible"
}
```

### Downstream Result

- Damage type: `uncertain`
- Damage confidence: `0.0`
- Evidence confidence: `0.17`
- Final decision: `REQUEST_MORE_EVIDENCE`

### Interpretation

Even if the image is technically sharp and normally exposed, it is not useful if the evidence required by the customer claim is not visible.


## 8. Demo Example G — Occluded Relevant Region

### Scenario

The important product region is blocked.

Image condition:

`occluded`

Input:

```text
relevant_region_visible = false
```

### Member 1 Behaviour

Representative output:

```json
{
  "relevant_region_visible": false,
  "image_quality": 0.0,
  "image_usable": false,
  "usability_reason": "relevant_region_not_visible"
}
```

### Downstream Result

- Damage type: `uncertain`
- Damage confidence: `0.0`
- Evidence confidence: `0.17`
- Final decision: `REQUEST_MORE_EVIDENCE`

### Interpretation

Occlusion prevents the system from relying on the visual evidence.

The correct system behaviour is to request additional evidence rather than automate the refund.


## 9. Demo Example H — Historical Blur Failure and Stabilisation

### Initial Problem

During Week 3, a dark hoodie was visually clear but was initially classified as slightly blurred.

Original blur scores:

- Normal hoodie: approximately `366.14`
- Dark hoodie: approximately `53.80`

A partially occluded jacket also produced a borderline blur error:

- Normal jacket: approximately `200.40`
- Occluded jacket: approximately `181.21`

### Refinement

Histogram equalisation was added before Laplacian variance:

```text
Image
→ Grayscale
→ Histogram Equalisation
→ Laplacian Variance
→ Blur Classification
```

### Stabilised Result

After refinement:

- Dark Hoodie blur score: approximately `640.55`
- Occluded Jacket blur score: approximately `964.03`

Both were correctly classified as `clear` on the controlled evaluation dataset.

### Interpretation

This demo shows why error analysis was necessary.

The final blur module is not simply the original Laplacian baseline; it includes a stabilisation step designed to reduce sensitivity to lighting and occlusion.


## 10. Suggested Live Demo Flow

For a live presentation, the recommended demonstration order is:

### Step 1 — Clear Image

Show:

- usable image
- normal damage prediction
- non-zero evidence confidence

Explain:

`The evidence is good enough to continue through the pipeline.`


### Step 2 — Severe Blur

Show:

- `image_usable = false`
- `damage_confidence = 0`
- `evidence_confidence = 0.17`
- `REQUEST_MORE_EVIDENCE`

Explain:

`The system does not automate when the visual evidence is unreliable.`


### Step 3 — Cropped or Occluded Image

Show:

- `relevant_region_visible = false`
- `image_usable = false`
- `REQUEST_MORE_EVIDENCE`

Explain:

`A technically clear image can still be unusable if the relevant evidence is missing.`


### Step 4 — Explain Final Decision Independence

Use the clear-image example.

Explain:

`Good image quality does not guarantee automatic refund. Policy, order validity, consistency, confidence, and refund risk are evaluated separately.`


## 11. Key Demo Message

The main message for the final presentation is:

> Member 1 does not decide whether a customer receives a refund. It determines whether the customer-provided visual evidence is reliable enough for downstream AI decision-making.

The module supports risk-aware selective automation by ensuring that poor-quality visual evidence triggers a conservative response instead of unsafe automated action.