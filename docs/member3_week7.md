# Member 3 - Week 7 Agent and UI Integration

## Objective

Expose the Member 3 retrieval and verification layer through one runnable app
interface and connect its structured output to the downstream decision Agent.

## Deliverables

- Added a local interactive refund UI and Python HTTP backend.
- Connected order retrieval, policy retrieval, evidence verification, evidence
  confidence, refund risk, and final decision generation.
- Added traceable text/order, image-evidence, and automatic-decision rules.
- Added an interactive command-line evidence interface and a repeatable demo.
- Added integration tests for a complete valid case and a missing-image case.

## Current boundary

The app executes the retrieval, verification, and decision modules. Raw-image
damage inference still uses controlled upstream values because trained Member 2
YOLO weights are not present in the repository. The UI labels this stage as a
prototype and does not process real refunds.
