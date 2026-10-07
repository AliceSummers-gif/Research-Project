# Member 3 - Week 8 RAG Evaluation Baseline

## Objective

Establish a reproducible evaluation baseline for policy retrieval before adding
embedding-based retrieval or real customer data.

## Dataset

- 60 synthetic labelled policy-retrieval cases.
- 15 cases for each of four controlled policy or safety-rule families.
- Includes vocabulary variation for damaged items, wrong items, no visible
  damage, and final-sale exclusions.
- Each record contains a case ID, query, expected policy ID, and an explicit
  synthetic-dataset label.

## Metrics

- Top-1 accuracy.
- Hit Rate@3.
- Mean Reciprocal Rank.
- Per-policy Top-1 accuracy.
- Saved failure cases for inspection.

## Interpretation

The results measure deterministic lexical retrieval on a small controlled mock
policy corpus. They do not represent real-world accuracy. The dataset is an
evaluation set, not customer data and not evidence that the model was trained
on real refund behaviour.

## Baseline result

- Top-1 accuracy: 61.7%.
- Hit Rate@3: 95.0%.
- Mean Reciprocal Rank: 0.764.
- Member 3 automated test result: 18 passed across Weeks 4-8.

The weaker Top-1 results for no-damage and final-sale queries identify the next
retrieval improvement target. Hit Rate@3 shows that the expected policy is
usually present in the short candidate list even when it is not ranked first.

## Next comparison

Use the same frozen test set to compare the lexical baseline with a pretrained
embedding retriever. Do not adjust the test queries after reviewing final
results; use a separate development set for threshold or prompt changes.
