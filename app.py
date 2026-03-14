import streamlit as st
from langgraph_flow import flow
from utils.logger import log_run
from datetime import datetime

st.set_page_config(page_title="Agentic RCA System", layout="wide")
st.title("🔍 Agentic AI Root Cause Analysis System")

st.markdown(
    """
This app demonstrates a **stateful agentic workflow** for industrial root cause analysis.

**Workflow:**  
Classify → Route → Retrieve Logs → Retrieve Maintenance → Detect Anomalies → RAG Search → Causal Reasoning → Confidence Score → Synthesize
"""
)

query = st.text_input("Ask your question (e.g., Why did reactor R-204 trip?)")

FULL_PIPELINE_STEPS = [
    "Classify",
    "Route",
    "RetrieveLogs",
    "RetrieveMaintenance",
    "DetectAnomalies",
    "RAGSearch",
    "CausalReason",
    "ConfidenceScore",
    "Synthesize"
]

SHORT_PIPELINE_STEPS = [
    "Classify",
    "Route",
    "Synthesize"
]

def detect_stage_from_state(state: dict) -> str:
    if "report" in state:
        return "Synthesize"
    elif "confidence_score" in state:
        return "ConfidenceScore"
    elif "causal_analysis" in state:
        return "CausalReason"
    elif "retrieved_docs" in state:
        return "RAGSearch"
    elif "anomalies" in state:
        return "DetectAnomalies"
    elif "maintenance_history" in state:
        return "RetrieveMaintenance"
    elif "logs" in state:
        return "RetrieveLogs"
    elif "next_step" in state:
        return "Route"
    elif "intent" in state or "component" in state:
        return "Classify"
    return "Start"

def format_state_for_display(state: dict) -> dict:
    return {
        "input": state.get("input"),
        "intent": state.get("intent"),
        "component": state.get("component"),
        "equipment_type": state.get("equipment_type"),
        "severity": state.get("severity"),
        "next_step": state.get("next_step"),
        "logs_count": len(state.get("logs", [])) if isinstance(state.get("logs"), list) else 0,
        "maintenance_history_count": len(state.get("maintenance_history", [])) if isinstance(state.get("maintenance_history"), list) else 0,
        "anomalies": state.get("anomalies", []),
        "retrieved_docs_count": len(state.get("retrieved_docs", [])) if isinstance(state.get("retrieved_docs"), list) else 0,
        "causal_analysis": state.get("causal_analysis"),
        "confidence_score": state.get("confidence_score"),
        "error": state.get("error"),
        "report_ready": "report" in state
    }

def render_user_friendly_report(report: dict):
    status = report.get("status", "unknown")

    if status != "success":
        st.warning(report.get("title", "Unsupported query"))
        st.write(report.get("summary", "No summary available."))
        st.write(f"**Detected intent:** {report.get('detected_intent', 'unknown')}")
        st.write(f"**Detected component:** {report.get('detected_component', 'unknown')}")
        return

    st.subheader(report.get("title", "RCA Report"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Component", report.get("component", "N/A"))
    with col2:
        st.metric("Equipment Type", report.get("equipment_type", "N/A"))
    with col3:
        st.metric("Confidence Score", report.get("confidence_score", 0.0))

    st.markdown("### Problem")
    st.write(report.get("problem", "Not available"))

    st.markdown("### Most Likely Root Cause")
    st.success(report.get("root_cause", "Not available"))

    st.markdown("### Key Evidence")
    evidence = report.get("evidence", [])
    if evidence:
        for item in evidence:
            st.markdown(f"- {item}")
    else:
        st.write("No evidence available.")

    st.markdown("### Causal Steps / Recommended Investigation Steps")
    steps = report.get("steps", [])
    if steps:
        for idx, step in enumerate(steps, start=1):
            st.markdown(f"{idx}. {step}")
    else:
        st.write("No steps available.")

    st.markdown("### Detected Anomalies")
    anomalies = report.get("anomalies", [])
    if anomalies:
        for item in anomalies:
            st.markdown(f"- {item}")
    else:
        st.write("No anomalies detected.")

    st.markdown("### Maintenance History")
    history = report.get("maintenance_history", [])
    if history:
        for row in history:
            st.markdown(
                f"- **{row.get('date', 'N/A')}** | "
                f"{row.get('maintenance_type', 'N/A')} | "
                f"{row.get('notes', 'N/A')}"
            )
    else:
        st.write("No maintenance history available.")

    st.markdown("### Recommendation")
    st.info(report.get("recommendation", "No recommendation available."))

    st.caption(
        f"LLM confidence: {report.get('llm_confidence', 'low')} | "
        f"Retrieved supporting docs: {report.get('retrieved_docs_count', 0)}"
    )

if query:
    st.divider()
    st.subheader("🧭 Live Agentic Execution")

    status_box = st.empty()
    progress_bar = st.progress(0)
    route_box = st.empty()

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown("### ✅ Execution Timeline")
        timeline_box = st.empty()

    with right_col:
        st.markdown("### 🧠 Full State After Every Step")
        state_box = st.empty()

    final_state = {}
    execution_history = []
    seen_stages = set()

    try:
        for current_state in flow.stream({"input": query}, stream_mode="values"):
            if not isinstance(current_state, dict):
                continue

            final_state = current_state
            stage = detect_stage_from_state(current_state)

            if stage not in seen_stages:
                seen_stages.add(stage)
                execution_history.append(
                    {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "stage": stage
                    }
                )

                if stage == "Route":
                    route_box.info(
                        f"Router decision: **{current_state.get('next_step', 'unknown')}**"
                    )

                chosen_route = current_state.get("next_step")
                if chosen_route == "Synthesize":
                    total_steps = len(SHORT_PIPELINE_STEPS)
                    current_index = SHORT_PIPELINE_STEPS.index(stage) + 1 if stage in SHORT_PIPELINE_STEPS else 1
                else:
                    total_steps = len(FULL_PIPELINE_STEPS)
                    current_index = FULL_PIPELINE_STEPS.index(stage) + 1 if stage in FULL_PIPELINE_STEPS else 1

                progress_bar.progress(min(current_index / total_steps, 1.0))
                status_box.info(f"Running stage: **{stage}**")

                with timeline_box.container():
                    for item in execution_history:
                        st.write(f"{item['time']} — **{item['stage']}**")

                state_box.json(format_state_for_display(current_state))

        progress_bar.progress(1.0)
        status_box.success("Execution completed.")

        st.divider()
        st.subheader("🪜 Final Execution Path")
        executed_path = " → ".join([item["stage"] for item in execution_history])
        st.code(executed_path, language="text")

        st.divider()
        st.subheader("📋 User-Friendly RCA Report")
        if "report" in final_state:
            render_user_friendly_report(final_state["report"])
            log_run(query, final_state["report"])
        else:
            st.warning("No final report was generated.")

        with st.expander("📦 Raw Final Report JSON"):
            if "report" in final_state:
                st.json(final_state["report"])

        with st.expander("📦 Raw Final State"):
            st.json(final_state)

    except Exception as e:
        status_box.error("Execution failed.")
        st.error(str(e))