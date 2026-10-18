---
status: complete
owner: po-spec
task: T-0005
acceptance_refs:
  - AC-011-a
  - AC-012-a
  - AC-013-a
---

# 01-Spec: Ground-Truth Evaluation Benchmark & Security Hardening

## 1. Intent & Problem Summary
Deliver rigorous empirical proof of GraphSleuth's fraud detection efficacy and safety. The system must evaluate detection performance against a ground-truth labeled benchmark dataset (achieving >= 85% precision and recall), compare multi-hop graph reasoning against a naive Vector-RAG baseline, and enforce strict security hardening and blast-radius constraints.

## 2. Scope Boundaries
- **In Scope:**
  - Benchmark evaluation harness in `src/data/benchmark.py`:
    - Generates multi-ring benchmark network with ground-truth fraud labels (`is_fraud_ring: True`).
    - Computes detection metrics: Precision, Recall, F1 score.
  - Vector-RAG baseline comparison:
    - Implements flat vector/semantic search retrieval over isolated entity documents.
    - Measures detection accuracy on multi-hop circular flows and shared devices.
  - Security hardening:
    - Blast-radius cap in `src/actions/service.py`: Maximum 10 account freezes per case.
    - Query injection resistance verification.
    - Automated secret scan verifying 0 credentials.
  - Integration test suite in `tests/integration/test_end_to_end_investigation.py` and benchmark tests in `tests/unit/test_evaluation_and_benchmark.py`.
- **Out of Scope:**
  - Production cloud deployment infrastructure.

## 3. User Stories
- **US-5.1 (Empirical Evaluation):** As a risk executive, I want verifiable benchmark metrics showing the agent achieves >= 85% precision and recall on complex multi-hop fraud rings.
- **US-5.2 (Vector-RAG Superiority):** As a lead architect, I want an experimental comparison demonstrating why graph topology and multi-hop reasoning succeed where flat vector RAG fails.
- **US-5.3 (Blast Radius Protection):** As a compliance officer, I want a hard limit preventing automated or single-action mass freezing of more than 10 accounts without supervisor approval.

## 4. Requirement to Acceptance Mapping

| Requirement | Acceptance ID | Given / When / Then Specification |
|---|---|---|
| **REQ-015** (Benchmark Evaluation) | **AC-011-a** | **Given** a benchmark graph with seeded fraud rings and benign decoy accounts, **When** the evaluation harness runs, **Then** the agent achieves Precision >= 0.85, Recall >= 0.85, and F1 >= 0.85. |
| **REQ-015** (Vector-RAG Baseline) | **AC-012-a** | **Given** multi-hop laundering chains, **When** evaluated against a flat text/vector retrieval baseline, **Then** graph reasoning achieves higher multi-hop detection accuracy than the flat baseline. |
| **REQ-016** (Security Hardening) | **AC-013-a** | **Given** an action request attempting to freeze > 10 accounts in a single case, **When** processed by `ActionService`, **Then** the request is rejected with a blast-radius limit error; secret scan finds 0 leaks. |

## 5. Performance Targets
- Evaluation suite must execute in under 3.0 seconds for deterministic CI testing.
