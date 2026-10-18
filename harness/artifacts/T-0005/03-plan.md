---
status: complete
owner: tech-lead
task: T-0005
acceptance_refs:
  - AC-011-a
  - AC-012-a
  - AC-013-a
---

# 03-Plan: Evaluation Benchmark & Hardening Plan

## 1. Lane Breakdown

### Lane 1: Benchmark Core (`src/data/benchmark.py`)
- **Owner:** Builder (Benchmark Lane)
- **Files:** `src/data/benchmark.py`
- **Deliverables:**
  - `generate_benchmark_dataset(seed=42)`: Seeds 3 distinct fraud ring topologies (shared devices, cycles, transit hubs) and 10 decoy accounts with verified ground-truth labels.
  - `evaluate_detection_performance(agent, benchmark_data)`: Runs investigations, tallies TP, FP, FN, and computes Precision, Recall, and F1.
  - `run_vector_rag_comparison(benchmark_data)`: Flat vector similarity baseline comparing multi-hop circular flow and shared device detection.

### Lane 2: Security Hardening (`src/actions/service.py`)
- **Owner:** Builder (Hardening Lane)
- **Files:** `src/actions/service.py`
- **Deliverables:**
  - Blast-radius limit: Maximum 10 account freezes per case.
  - Rejection with `ValueError` when limit is exceeded.

### Lane 3: Automated Verification
- **Owner:** Test Author
- **Files:** `tests/unit/test_evaluation_and_benchmark.py`, `tests/integration/test_end_to_end_investigation.py`
- **Deliverables:**
  - Red tests asserting Precision >= 0.85, Recall >= 0.85, F1 >= 0.85.
  - Red tests asserting Graph multi-hop accuracy > Vector RAG accuracy.
  - Red tests asserting blast radius rejection at > 10 freezes.
  - End-to-end integration test verifying full pipeline execution.

## 2. Gate Criteria & Constraints
- Execution time: Full benchmark test suite executes in < 3.0 seconds.
- Diff limit: < 400 lines per module.
- 100% parameter safety maintained.
