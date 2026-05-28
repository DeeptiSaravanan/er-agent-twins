{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Streamlit dashboard for ER Agentic Twin\
Shows live simulation, memory status, and agent reasoning\
"""\
\
import streamlit as st\
import pandas as pd\
import plotly.express as px\
from datetime import datetime\
from agents.memory_retriever import memory_retriever\
from agents.memory_updater import memory_updater\
from agents.orchestrator_agent import orchestrator_agent\
from agents.world_model_agent import predict_and_store, submit_feedback\
from simulators.patient_stream import PatientStreamSimulator\
from simulators.er_state import ERStateSimulator\
\
st.set_page_config(page_title="ER Agentic Twin", layout="wide")\
\
# Initialize simulators\
if 'patient_sim' not in st.session_state:\
    st.session_state.patient_sim = PatientStreamSimulator()\
    st.session_state.er_state = ERStateSimulator()\
    st.session_state.last_prediction_id = None\
\
st.title("\uc0\u55356 \u57317  ER Agentic Twin")\
st.caption("Memory-Augmented Surge Prediction | Powered by ADK + Gemini 3.5 Flash")\
\
# ============ MEMORY STATUS SIDEBAR ============\
with st.sidebar:\
    st.header("\uc0\u55358 \u56800  Memory Bank")\
    \
    current_hour = datetime.now().hour\
    current_day = datetime.now().strftime("%A")\
    \
    patterns = memory_retriever.retrieve_surge_patterns(current_hour, current_day)\
    \
    st.subheader("Stored Patterns")\
    if patterns:\
        pattern_df = pd.DataFrame([\
            \{\
                "Time": p.get('timestamp', 'Unknown')[:16] if p.get('timestamp') else 'Unknown',\
                "Surge": f"\{p.get('surge_probability', 0)*100:.0f\}%",\
                "Accurate": "\uc0\u9989 " if p.get('was_accurate') is True else "\u9203 " if p.get('was_accurate') is None else "\u10060 "\
            \}\
            for p in patterns\
        ])\
        st.dataframe(pattern_df, use_container_width=True)\
    else:\
        st.info("No memories yet. Run a simulation to build memory.")\
    \
    st.divider()\
    st.caption("Memory Type: InMemoryMemoryService")\
    st.caption("\uc0\u8599 \u65039  Upgrade to Vertex AI Memory Bank in production")\
\
# ============ MAIN DASHBOARD ============\
col1, col2, col3 = st.columns(3)\
\
with col1:\
    load = st.session_state.er_state.load_percentage\
    st.metric("Current ER Load", f"\{load:.0f\}%", delta="+22%", delta_color="inverse")\
\
with col2:\
    beds = st.session_state.er_state.available_beds\
    st.metric("Available Beds", f"\{beds\}/\{st.session_state.er_state.total_beds\}", delta="-4", delta_color="inverse")\
\
with col3:\
    adjustment = memory_retriever.get_historical_adjustment_factor(current_hour, current_day)\
    surge_prob = min(0.95, (st.session_state.patient_sim.get_arrival_rate() / 12) * (1 - (beds / 24)) * adjustment)\
    st.metric("Surge Probability (Memory-Enhanced)", f"\{surge_prob*100:.0f\}%", \
              delta=f"\{'\uc0\u8593 ' if adjustment > 1 else '\u8595 '\} \{abs(adjustment-1)*100:.0f\}% vs baseline")\
\
# ============ TWO-PANEL LAYOUT ============\
left, right = st.columns(2)\
\
with left:\
    st.subheader("\uc0\u55356 \u57317  Patient Queue")\
    \
    # Show current queue\
    queue_data = []\
    for i, p in enumerate(st.session_state.er_state.patient_queue[-5:], 1):\
        queue_data.append(\{\
            "Priority": i,\
            "ESI": p.get('esi_level', 3),\
            "Complaint": p.get('chief_complaint', 'Unknown')[:30],\
            "Wait": f"\{i*3\} min"\
        \})\
    \
    if queue_data:\
        st.dataframe(pd.DataFrame(queue_data), use_container_width=True)\
    else:\
        st.info("Queue empty. Run simulation to add patients.")\
    \
    st.subheader("\uc0\u55358 \u56800  Agent Reasoning")\
    st.info(f"""\
    **Orchestrator Agent (Memory-Aware):**\
    1. Retrieved \{len(patterns)\} historical patterns for \{current_day\} \{current_hour\}:00\
    2. Historical adjustment factor: \{adjustment\}x\
    3. \{f'Increased prediction based on memory' if adjustment > 1 else 'No adjustment from memory'\}\
    """)\
\
with right:\
    st.subheader("\uc0\u55357 \u56520  Surge Prediction")\
    \
    if st.button("\uc0\u55357 \u56580  Run Memory-Enhanced Simulation", use_container_width=True):\
        with st.spinner("Agents analyzing with memory retrieval..."):\
            # Run prediction with memory\
            arrival_rate = st.session_state.patient_sim.get_arrival_rate()\
            beds_avail = st.session_state.er_state.available_beds\
            \
            result = predict_and_store(\
                arrival_rate=arrival_rate,\
                beds_available=beds_avail,\
                hour=current_hour,\
                day=current_day\
            )\
            \
            st.session_state.last_prediction_id = result['prediction_id']\
            \
            st.success(f"""\
            **World Model Agent Prediction:**\
            - Surge probability: **\{result['surge_probability']*100:.0f\}%**\
            - Adjustment factor: **\{result['adjustment_applied']\}x**\
            - Recommendation: **\{result['recommendation']\}**\
            \
            *Prediction stored in memory for future learning.*\
            """)\
    \
    st.subheader("\uc0\u55357 \u56481  Memory-Augmented Recommendations")\
    \
    if surge_prob > 0.7:\
        st.warning("\uc0\u9888 \u65039  **Surge Alert:** Activate on-call staff within 30 minutes")\
    else:\
        st.info("\uc0\u9989  **Normal Operations:** Continue monitoring")\
    \
    st.markdown(f"""\
    - \uc0\u55357 \u56522  **Historical pattern:** \{current_day\}s at \{current_hour\}:00 have \{len(patterns)\} recorded patterns\
    - \uc0\u55358 \u56800  **Memory adjustment:** \{adjustment\}x factor applied\
    - \uc0\u55357 \u56425 \u8205 \u9877 \u65039  **Action:** \{'Call back staff' if surge_prob > 0.7 else 'Regular staffing sufficient'\}\
    """)\
\
# ============ FEEDBACK SECTION ============\
st.divider()\
st.subheader("\uc0\u55357 \u56580  Learning Loop - Provide Feedback")\
\
col_fb1, col_fb2 = st.columns(2)\
\
with col_fb1:\
    st.write("**How memory improves over time:**")\
    st.code("""\
    1. System makes prediction with memory adjustment\
    2. Actual surge outcome occurs (or doesn't)\
    3. Charge nurse provides feedback\
    4. Memory Bank stores the outcome\
    5. Future predictions use this experience\
    """)\
\
with col_fb2:\
    if st.session_state.last_prediction_id:\
        st.write("**Was the last prediction accurate?**")\
        \
        col_yes, col_no = st.columns(2)\
        with col_yes:\
            if st.button("\uc0\u9989  Yes, Accurate", use_container_width=True):\
                result = submit_feedback(st.session_state.last_prediction_id, was_accurate=True)\
                st.success(result['message'])\
        with col_no:\
            if st.button("\uc0\u10060  No, Inaccurate", use_container_width=True):\
                result = submit_feedback(st.session_state.last_prediction_id, was_accurate=False)\
                st.info(result['message'])\
    else:\
        st.info("Run a simulation first, then provide feedback.")\
\
# ============ FOOTER ============\
st.divider()\
st.caption("\uc0\u9888 \u65039  Demo uses InMemoryMemoryService. Production uses Vertex AI Memory Bank with persistent storage.")\
st.caption("Built with Google ADK | Gemini 3.5 Flash | Streamlit")}