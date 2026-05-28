{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Orchestrator Agent - coordinates all other agents with memory awareness\
"""\
\
from google.adk.agents import LlmAgent\
from google.adk.tools import FunctionTool\
from agents.memory_retriever import memory_retriever\
\
def get_memory_context(hour: int, day: str) -> str:\
    """Tool: Retrieves historical patterns from memory bank"""\
    patterns = memory_retriever.retrieve_surge_patterns(hour, day)\
    \
    if not patterns:\
        return "No historical data available for this time."\
    \
    context = f"Historical patterns for \{day\} at \{hour\}:00:\\n"\
    for i, p in enumerate(patterns, 1):\
        context += f"\{i\}. Surge probability: \{p['surge_probability']*100:.0f\}% | "\
        context += f"Accurate: \{p['was_accurate'] if p['was_accurate'] is not None else 'pending'\}\\n"\
    \
    adjustment = memory_retriever.get_historical_adjustment_factor(hour, day)\
    context += f"\\nHistorical adjustment factor: \{adjustment\}x"\
    \
    return context\
\
def get_current_bed_status() -> dict:\
    """Tool: Returns current ER bed status"""\
    return \{\
        "total_beds": 24,\
        "available_beds": 6,\
        "occupied_beds": 18,\
        "cleaning_in_progress": 2\
    \}\
\
def get_patient_queue() -> list:\
    """Tool: Returns current triage queue"""\
    return [\
        \{"patient_id": "P001", "esi_level": 2, "chief_complaint": "Chest pain", "wait_minutes": 12\},\
        \{"patient_id": "P002", "esi_level": 3, "chief_complaint": "Shortness of breath", "wait_minutes": 8\},\
        \{"patient_id": "P003", "esi_level": 4, "chief_complaint": "Broken ankle", "wait_minutes": 25\},\
        \{"patient_id": "P004", "esi_level": 1, "chief_complaint": "Unresponsive", "wait_minutes": 0\},\
    ]\
\
orchestrator_agent = LlmAgent(\
    name="ER_Orchestrator",\
    model="gemini-2.5-flash",\
    instruction="""\
    You are the orchestrator for an Emergency Room surge management system with MEMORY.\
    \
    ALWAYS call get_memory_context FIRST before making any prediction.\
    Use historical patterns to adjust your confidence.\
    \
    Available tools:\
    1. get_memory_context - ALWAYS call first\
    2. get_current_bed_status - Current ER capacity\
    3. get_patient_queue - Current patient wait times\
    \
    Output format:\
    \{\
        "surge_probability": float (0-1),\
        "adjustment_applied": "increased" or "decreased",\
        "recommendation": "clear action for charge nurse",\
        "reasoning": "step-by-step explanation"\
    \}\
    """,\
    tools=[\
        FunctionTool(get_memory_context),\
        FunctionTool(get_current_bed_status),\
        FunctionTool(get_patient_queue)\
    ]\
)}