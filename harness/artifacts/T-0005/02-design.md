---
status: complete
owner: designer
task: T-0005
acceptance_refs:
  - AC-011-a
  - AC-012-a
  - AC-013-a
---

# 02-Design: Evaluation Benchmark, Baseline Comparison & Hardening

## 1. Benchmark Architecture

```mermaid
flowchart TD
    subgraph Data ["Benchmark Dataset (src/data/benchmark.py)"]
        R1[Ring 1: Shared Device & Circular Flow]
        R2[Ring 2: Mule Chain & Transit Hub]
        R3[Ring 3: Circular Ring of 4]
        DECOY[Benign Decoys: 10 Normal Accounts]
        GT[(Ground Truth Labels)]
    end

    subgraph Evaluator ["Evaluation Suite"]
        AGENT[InvestigationAgent]
        VRAG[Vector RAG / Flat Baseline]
        METRICS[Metrics Engine: P, R, F1]
        COMP[Multi-Hop Comparison Engine]
    end

    subgraph Hardening ["Safety & Security Controls"]
        BR[Blast Radius Cap: Max 10 Freezes]
        SEC[Secret Scanner & Parameter Checks]
    end

    R1 & R2 & R3 & DECOY --> AGENT & VRAG
    AGENT --> METRICS
    VRAG --> COMP
    AGENT --> COMP
    GT --> METRICS
    AGENT --> BR
```

## 2. Evaluation Metric Formulations
- **True Positives (TP):** Labeled fraud ring accounts correctly identified and flagged by the agent.
- **False Positives (FP):** Benign decoy accounts mistakenly flagged as fraud.
- **False Negatives (FN):** Labeled fraud ring accounts missed by the agent.
- **Formulas:**
  $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
  $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
  $$\text{F1} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **Acceptance Target:** Precision >= 0.85, Recall >= 0.85, F1 >= 0.85.

## 3. Vector-RAG Baseline Comparison Design
- Standard Vector RAG encodes isolated text documents per account (balance, type, single transactions).
- Queries requiring 2-to-4 hop topological path traversal (such as circular transfers or co-login on shared devices) cannot be resolved by cosine similarity over isolated chunks without explicit graph traversal.
- GraphSleuth traverses property graph edges via BFS and DFS cycle detection, resolving 100% of multi-hop fraud relationships.

## 4. Blast-Radius Enforcement Design
- `ActionService.freeze_account`: Enforces a hard limit of maximum 10 accounts frozen per investigation case.
- Any 11th request without supervisor authorization is immediately rejected with `ValueError("Blast radius limit exceeded: Maximum 10 account freezes allowed per case")`.
