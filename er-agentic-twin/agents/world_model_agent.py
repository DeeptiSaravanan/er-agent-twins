{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
World Model Agent - Simulates future ER states and learns from outcomes\
"""\
\
from google.adk.agents import LlmAgent\
from google.adk.tools import FunctionTool\
from agents.memory_retriever import memory_retriever\
from agents.memory_updater import memory_updater\
from datetime import datetime\
\
def predict_and_store(arrival_rate: float, beds_available: int, hour: int, day: str) -> dict:\
    """Makes prediction AND stores it in memory for future retrieval"""\
    adjustment = memory_retriever.get_historical_adjustment_factor(hour, day)\
    \
    base_probability = min(0.95, (arrival_rate / 12) * (1 - (beds_available / 24)))\
    adjusted_probability = min(0.95, base_probability * adjustment)\
    \
    prediction = \{\
        "surge_probability": round(adjusted_probability, 2),\
        "arrival_rate": arrival_rate,\
        "beds_available": beds_available,\
        "adjustment_applied": adjustment,\
        "recommendation": "Activate on-call staff" if adjusted_probability > 0.7 else "Monitor",\
        "prediction_id": datetime.now().strftime("%Y%m%d%H%M%S"),\
        "hour": hour,\
        "day": day\
    \}\
    \
    memory_updater.store_prediction_outcome(prediction, actual_outcome=None)\
    \
    return prediction\
\
def submit_feedback(prediction_id: str, was_accurate: bool, notes: str = "") -> dict:\
    """Allows human feedback to improve future predictions"""\
    memory_updater.update_accuracy(prediction_id, was_accurate)\
    \
    return \{\
        "status": "feedback_received",\
        "will_improve_future": True,\
        "message": "Thank you! Your feedback will improve future predictions."\
    \}\
\
world_model_agent = LlmAgent(\
    name="World_Model_Agent",\
    model="gemini-2.5-flash",\
    instruction="""\
    You simulate future ER states AND learn from past performance.\
    \
    ALWAYS use predict_and_store (not just predict). This stores the prediction\
    in memory so future runs can learn from it.\
    \
    Use submit_feedback when users provide accuracy feedback.\
    \
    Your goal: Continuously improve prediction accuracy by learning from outcomes.\
    """,\
    tools=[\
        FunctionTool(predict_and_store),\
        FunctionTool(submit_feedback)\
    ]\
)}