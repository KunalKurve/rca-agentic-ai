from graphviz import Digraph

dot = Digraph(comment="Advanced Agentic RCA Workflow")

dot.node("A", "Query Classifier")
dot.node("B", "Router")
dot.node("C", "Log Retriever")
dot.node("D", "Maintenance Retriever")
dot.node("E", "Anomaly Detector")
dot.node("F", "RAG Retriever")
dot.node("G", "Causal Reasoning LLM")
dot.node("H", "Confidence Scorer")
dot.node("I", "Final Synthesizer")

dot.edge("A", "B")
dot.edge("B", "C")
dot.edge("C", "D")
dot.edge("D", "E")
dot.edge("E", "F")
dot.edge("F", "G")
dot.edge("G", "H")
dot.edge("H", "I")

dot.render("rca_agentic_graph", format="png", cleanup=True)
print("Graph saved as rca_agentic_graph.png")