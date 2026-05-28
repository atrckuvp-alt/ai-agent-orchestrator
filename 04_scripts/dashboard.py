import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"


def load_json(filename):

    path = MEMORY / filename

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


st.set_page_config(
    page_title="AI Agent Research Team",
    layout="wide"
)

st.title("AI Agent Research Team Dashboard")

st.markdown("---")

current_stack = load_json("current_stack.json")
champions = load_json("champion_models.json")
approvals = load_json("approval_queue.json")
decisions = load_json("decision_history.json")
improvements = load_json("self_improvement_log.json")
runtime_metrics = load_json("runtime_metrics.json")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Current Stack")

    st.json(current_stack)

with col2:

    st.subheader("Champion Models")

    st.json(champions)

st.markdown("---")

st.subheader("Pending Approval Queue")

pending = [
    x for x in approvals.get("approval_requests", [])
    if x.get("status") == "pending_human_approval"
]

st.json(pending)

st.markdown("---")

st.subheader("Latest Decisions")

latest_decisions = decisions.get("decisions", [])[-10:]

st.json(latest_decisions)

st.markdown("---")

st.subheader("Self Improvement Log")

latest_improvements = improvements.get("improvements", [])[-10:]

st.json(latest_improvements)

st.markdown("---")

st.subheader("Runtime Metrics")

latest_runs = runtime_metrics.get("runs", [])[-20:]

st.json(latest_runs)
