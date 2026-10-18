---
status: complete
owner: scribe
task: T-0003
acceptance_refs:
  - AC-003-a
  - AC-003-b
  - AC-003-c
  - AC-003-d
  - AC-003-e
---

# 08-Docs: Multi-Hop Reasoning & Action Layer Documentation

## 1. Documentation Updates
- Updated `CHANGELOG.md` with version `[0.3.0] - 2026-10-18`.
- Documented composite risk scoring formula and weights:
  - Shared devices factor: 35%
  - Circular money flow factor: 30%
  - Community clustering density: 20%
  - Transaction velocity: 15%
- Documented simulated core banking action service and risk-tiered approval matrix:
  - `AUTO_EXECUTED`: Low-impact actions (`flag_entity`, `create_case`).
  - `PENDING_APPROVAL`: High-impact actions (`freeze_account`, `block_device`) requiring human analyst signoff.
  - Reversibility: `reverse_action` transitions state to `REVERSED` and restores previous account/device status.
  - Audit Trail: Immutable append-only `ActionLog` capturing timestamps, approvers, and cited evidence IDs.

## 2. Tool Catalog Additions
- **`algo.score_risk`**: Computes composite risk score `[0.0, 1.0]`, risk tier (`LOW`, `MEDIUM`, `HIGH`), and factor breakdown.
- **`action.create_case`**: Creates an investigation case.
- **`action.flag_entity`**: Flags account or device with suspicion level and reason.
- **`action.freeze_account`**: Queues account freeze pending approval.
- **`action.block_device`**: Queues device block pending approval.
- **`action.approve_action`**: Approves and executes a pending action.
- **`action.reverse_action`**: Rolls back an executed action.
- **`action.get_audit_log`**: Retrieves the immutable history of actions.
