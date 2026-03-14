def score_confidence(state):
    anomalies = state.get("anomalies", [])
    retrieved_docs = state.get("retrieved_docs", [])
    causal_analysis = state.get("causal_analysis", {})

    score = 0.0

    if len(anomalies) >= 2:
        score += 0.35

    if len(retrieved_docs) >= 1:
        score += 0.25

    llm_conf = str(causal_analysis.get("confidence", "low")).lower()
    if llm_conf == "high":
        score += 0.40
    elif llm_conf == "medium":
        score += 0.25
    else:
        score += 0.10

    score = min(score, 1.0)

    return {
        **state,
        "confidence_score": round(score, 2)
    }