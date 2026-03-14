def synthesize_response(state):
    if state.get("intent") != "root_cause_analysis" or state.get("component") == "unknown":
        report = {
            "status": "unsupported_or_unknown_query",
            "title": "Unsupported or unclear query",
            "summary": "The system could not confidently identify a supported RCA query or a known equipment component.",
            "detected_intent": state.get("intent", "unknown"),
            "detected_component": state.get("component", "unknown")
        }
        return {
            **state,
            "report": report
        }

    causal = state.get("causal_analysis", {})

    report = {
        "status": "success",
        "title": f"RCA Report for {state.get('component')}",
        "component": state.get("component"),
        "equipment_type": state.get("equipment_type"),
        "intent": state.get("intent"),
        "severity": state.get("severity"),
        "problem": causal.get("problem", "Not available"),
        "root_cause": causal.get("root_cause", "Not available"),
        "evidence": causal.get("evidence", []),
        "steps": causal.get("steps", []),
        "llm_confidence": causal.get("confidence", "low"),
        "confidence_score": state.get("confidence_score", 0.0),
        "anomalies": state.get("anomalies", []),
        "maintenance_history": state.get("maintenance_history", []),
        "retrieved_docs_count": len(state.get("retrieved_docs", [])),
        "recommendation": (
            "Inspect the suspected subsystem, validate alarms and sensors, "
            "and review recent maintenance before restarting equipment."
        )
    }

    return {
        **state,
        "report": report
    }