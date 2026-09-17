# Member 1 — Week 4 Agent Integration

## 1. Objective

The objective of Week 4 is to integrate the real Member 1 module with the shared Agent pipeline.

The Week 4 plan requires:

- Wrapping Member 1 as a callable function/API
- Returning structured JSON-compatible output
- Allowing the Agent pipeline to call the real Member 1 module


## 2. Existing Member 1 Adapter

The repository already contains:

`src/agent/member1_adapter.py`

The main callable function is:

`run_member1()`

Function signature:

```python
run_member1(
    case: CaseInput,
    *,
    relevant_region_visible: bool,
) -> tuple[Member1Output, dict]