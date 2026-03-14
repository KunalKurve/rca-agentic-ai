def classify_query(state):
    query = state["input"].lower()

    component = "unknown"
    equipment_type = "unknown"
    intent = "unknown"
    severity = "medium"

    if "reactor" in query or "r-204" in query:
        component = "R-204"
        equipment_type = "reactor"
    elif "pump" in query or "p-101" in query:
        component = "P-101"
        equipment_type = "pump"

    if "why" in query or "root cause" in query or "trip" in query or "fail" in query:
        intent = "root_cause_analysis"

    if "urgent" in query or "critical" in query:
        severity = "high"

    return {
        **state,
        "component": component,
        "equipment_type": equipment_type,
        "intent": intent,
        "severity": severity
    }