---
status: complete
owner: po-spec
task: T-0003
acceptance_refs:
  - AC-003-a
  - AC-003-b
  - AC-003-c
  - AC-003-d
  - AC-003-e
---

# 01-Spec: Multi-Hop Reasoning & Action Layer

## 1. Intent & Problem Summary
Deliver an intelligent reasoning and remediation layer for GraphSleuth. The agent formulates fraud hypotheses across multiple hops, gathers evidence using graph tools, computes a composite risk score with factor contributions, and initiates risk-tiered actions (auto-flagging, case creation, and gated freeze/block requests) that require recorded approvals and maintain an immutable audit trail.

## 2. Scope Boundaries
- **In Scope:**
  - `algo.score_risk`: Composite scoring tool synthesizing graph topology into a normalized score [0.0, 1.0] with feature contributions.
  - Multi-hop hypothesis testing in `InvestigationAgent`: evaluates shared-device collusion and circular laundering hypotheses within <= 15 calls.
  - `src/actions/service.py`: Action service managing cases, entity flags, account freezes, device blocks, and analyst notifications.
  - Decision policy mapping case confidence and entity risk to action tiers (`AUTO`, `PENDING_ONE_CLICK`, `PENDING_EXPLICIT_REVIEW`).
  - Idempotency, reversibility (unfreeze, unflag), and `ActionLog` audit history.
  - Integration with `SengraMCPServer` exposing `action.*` and `algo.score_risk`.
- **Out of Scope:**
  - Web UI visualization canvas (Sprint 4).

## 3. User Stories
- **US-3.1 (Multi-Factor Risk Scoring):** As an analyst, I want to see an overall risk score broken down into contributing factors (shared devices: 35%, circular flows: 30%, community density: 25%) so I understand what drove the score.
- **US-3.2 (Hypothesis Reasoning):** As an analyst, I want the agent to systematically evaluate multiple hypotheses (mule network vs. shared family device) before rendering a conclusion.
- **US-3.3 (Gated Remediation):** As a risk officer, I want high-impact actions like account freezes and device blocks placed in an approval queue with cited evidence before execution.
- **US-3.4 (Action Reversibility & Audit):** As an auditor, I want every action recorded in an immutable log and reversible if a customer false positive is identified.

## 4. Requirement to Acceptance Mapping

| Requirement | Acceptance ID | Given / When / Then Specification |
|---|---|---|
| **REQ-007** (Risk Scoring) | **AC-003-a** | **Given** account `A-1042`, **When** `score_risk` is executed, **Then** it returns score >= 0.75, tier `HIGH`, and factor contributions for shared devices, circular flows, and community membership. |
| **REQ-008 & REQ-009** (Hypothesis Loop) | **AC-003-b** | **Given** an alert on `A-1042`, **When** the agent runs multi-hop investigation, **Then** it tests collusion and circular flow hypotheses across 3 hops and finishes in <= 15 tool calls. |
| **REQ-010 & REQ-011** (Gated Actions) | **AC-003-c** | **Given** an investigation finding fraud ring accounts (`A-1042`, `A-1050`), **When** actions are requested, **Then** account flags execute automatically, while account freeze and device block enter `PENDING_APPROVAL`. |
| **REQ-012** (Execution & Reversibility) | **AC-003-d** | **Given** a queued action, **When** approved by an authorized user, **Then** state transitions to `COMPLETED`; **When** reversal is triggered (`unfreeze`), **Then** account status returns to active. |
| **REQ-012** (Audit Trail) | **AC-003-e** | **Given** any executed or queued action, **When** inspecting `ActionLog`, **Then** record contains immutable action ID, target entity, status, approver, evidence references, and timestamp. |

## 5. Edge Cases & Constraints
- Duplicate requests: Passing the same idempotency key returns the existing action result without creating duplicates.
- Missing evidence: Write tools reject calls lacking a case ID or evidence IDs.
- Blast-radius limit: Maximum 10 account freeze requests per investigation.
