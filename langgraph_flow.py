from langgraph.graph import StateGraph
from typing import TypedDict

class RCAState(TypedDict, total=False):
    input: str
    intent: str
    component: str
    equipment_type: str
    severity: str
    next_step: str
    logs: list
    maintenance_history: list
    anomalies: list
    retrieved_docs: list
    causal_analysis: dict
    confidence_score: float
    report: dict
    error: str

from agents.query_classifier import classify_query
from agents.router import route_query
from agents.data_retriever import retrieve_logs
from agents.maintenance_retriever import retrieve_maintenance
from agents.anomaly_detector import detect_anomalies
from agents.rag_retriever import search_sops
from agents.causal_reasoning import generate_causal_path
from agents.confidence_scorer import score_confidence
from agents.final_synthesizer import synthesize_response

# Classify → Route → RetrieveLogs → RetrieveMaintenance → DetectAnomalies → RAGSearch → CausalReason → ConfidenceScore → Synthesize

graph = StateGraph(state_schema=RCAState)

graph.add_node("Classify", classify_query)
graph.add_node("Route", route_query)
graph.add_node("RetrieveLogs", retrieve_logs)
graph.add_node("RetrieveMaintenance", retrieve_maintenance)
graph.add_node("DetectAnomalies", detect_anomalies)
graph.add_node("RAGSearch", search_sops)
graph.add_node("CausalReason", generate_causal_path)
graph.add_node("ConfidenceScore", score_confidence)
graph.add_node("Synthesize", synthesize_response)

graph.set_entry_point("Classify")
graph.add_edge("Classify", "Route")

graph.add_conditional_edges(
    "Route",
    lambda state: state["next_step"],
    {
        "RetrieveLogs": "RetrieveLogs",
        "Synthesize": "Synthesize"
    }
)

graph.add_edge("RetrieveLogs", "RetrieveMaintenance")
graph.add_edge("RetrieveMaintenance", "DetectAnomalies")
graph.add_edge("DetectAnomalies", "RAGSearch")
graph.add_edge("RAGSearch", "CausalReason")
graph.add_edge("CausalReason", "ConfidenceScore")
graph.add_edge("ConfidenceScore", "Synthesize")

flow = graph.compile()