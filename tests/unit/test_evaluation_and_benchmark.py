"""Unit tests for ground-truth benchmark evaluation, Vector-RAG comparison, and security hardening."""
import pytest

from src.actions.service import ActionService
from src.data.benchmark import (
    generate_benchmark_dataset,
    evaluate_detection_performance,
    run_vector_rag_comparison,
)
from src.graph.engine import PropertyGraph
from src.mcp.server import SengraMCPServer
from src.agent.loop import InvestigationAgent


def test_benchmark_dataset_structure():
    """Verify benchmark generator creates multiple fraud rings and ground-truth labels."""
    dataset = generate_benchmark_dataset(seed=42)
    assert "nodes" in dataset and "edges" in dataset
    assert "ground_truth" in dataset

    gt = dataset["ground_truth"]
    assert "fraud_accounts" in gt and "benign_accounts" in gt
    assert len(gt["fraud_accounts"]) >= 6  # At least 2 rings of 3+ accounts
    assert len(gt["benign_accounts"]) >= 5


def test_evaluation_metrics_precision_recall_f1():
    """AC-011-a: Agent achieves precision >= 0.85, recall >= 0.85, and F1 >= 0.85 on benchmark."""
    dataset = generate_benchmark_dataset(seed=42)
    engine = PropertyGraph()
    engine.load_dataset(dataset)
    action_service = ActionService()
    mcp_server = SengraMCPServer(graph=engine, action_service=action_service)
    agent = InvestigationAgent(tool_client=mcp_server)

    metrics = evaluate_detection_performance(agent=agent, benchmark_data=dataset)

    assert metrics["precision"] >= 0.85, f"Precision {metrics['precision']} < 0.85"
    assert metrics["recall"] >= 0.85, f"Recall {metrics['recall']} < 0.85"
    assert metrics["f1"] >= 0.85, f"F1 score {metrics['f1']} < 0.85"
    assert metrics["total_investigations"] >= 5


def test_vector_rag_baseline_comparison():
    """AC-012-a: Proves graph multi-hop reasoning outperforms flat vector RAG on topological fraud."""
    dataset = generate_benchmark_dataset(seed=42)
    comparison = run_vector_rag_comparison(benchmark_data=dataset)

    assert comparison["graph_accuracy"] > comparison["vector_rag_accuracy"]
    assert comparison["graph_accuracy"] >= 0.90
    assert comparison["vector_rag_accuracy"] <= 0.40  # Flat vector search misses multi-hop loops


def test_blast_radius_cap_enforcement():
    """AC-013-a: Action service blocks freezing > 10 accounts in a single case."""
    service = ActionService()
    case_id = service.create_case("Large Investigation", ["A-1"], "Mass freezing test")

    # Freeze 10 accounts successfully
    for i in range(1, 11):
        service.freeze_account(
            case_id=case_id,
            account_id=f"A-{i}",
            reason=f"Suspect {i}",
            evidence_ids=[f"A-{i}"]
        )

    # 11th freeze attempt must raise blast radius error
    with pytest.raises(ValueError, match="Blast radius limit"):
        service.freeze_account(
            case_id=case_id,
            account_id="A-11",
            reason="Suspect 11",
            evidence_ids=["A-11"]
        )
