def route_query(state):
    if state.get("intent") == "root_cause_analysis" and state.get("component") != "unknown":
        next_step = "RetrieveLogs"
    else:
        next_step = "Synthesize"

    return {
        **state,
        "next_step": next_step
    }