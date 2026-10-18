---
status: complete
owner: test-author
task: T-0005
acceptance_refs:
  - AC-011-a
  - AC-012-a
  - AC-013-a
---

# 04-Tests: Evaluation Benchmark & Hardening Test Suite

## 1. Test Suite Structure
- Unit tests: `tests/unit/test_evaluation_and_benchmark.py`
- Integration tests: `tests/integration/test_end_to_end_investigation.py`

## 2. Red Phase Verification
- **Command:** `python -m pytest tests/unit/test_evaluation_and_benchmark.py`
- **Result:** FAILED (`ModuleNotFoundError: No module named 'src.data.benchmark'`)
- **Status:** Red tests established cleanly before implementation.

## 3. Test Cases Implemented

| Test Function | Acceptance ID | Target Behavior Verified |
|---|---|---|
| `test_benchmark_dataset_structure` | `AC-011-a` | Validates benchmark generator produces multiple fraud rings, decoy accounts, and ground-truth labels. |
| `test_evaluation_metrics_precision_recall_f1` | `AC-011-a` | Evaluates autonomous agent detection performance: verifies Precision >= 0.85, Recall >= 0.85, and F1 >= 0.85. |
| `test_vector_rag_baseline_comparison` | `AC-012-a` | Compares multi-hop topology detection against flat vector/text retrieval: verifies graph accuracy >= 0.90 while flat RAG accuracy <= 0.40. |
| `test_blast_radius_cap_enforcement` | `AC-013-a` | Rejects freezing > 10 accounts in a single case with `ValueError("Blast radius limit exceeded")`. |
| `test_full_pipeline_alert_to_investigation_and_approval` | `AC-010-a` / `AC-011-a` | End-to-end integration test from alert ingestion to reasoning, Cytoscape element extraction, citation check, and action approval. |

## 4. Gate G1 Readiness
All test specifications authored and awaiting Builder implementation.
