{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Triage Agent - Assesses patient severity using ESI-like scoring\
"""\
\
from google.adk.agents import LlmAgent\
from google.adk.tools import FunctionTool\
\
def assess_patient(vitals: dict, chief_complaint: str) -> dict:\
    """Tool: Assess patient and return ESI level"""\
    # Simple rule-based triage for demo\
    hr = vitals.get('heart_rate', 80)\
    spo2 = vitals.get('spo2', 98)\
    \
    if 'chest pain' in chief_complaint.lower() or hr > 120 or spo2 < 90:\
        esi_level = 2\
        risk = "High"\
    elif 'broken' in chief_complaint.lower() or hr > 100:\
        esi_level = 3\
        risk = "Medium"\
    else:\
        esi_level = 4\
        risk = "Low"\
    \
    return \{\
        "esi_level": esi_level,\
        "risk_level": risk,\
        "recommended_action": "Immediate ECG" if esi_level <= 2 else "Standard workup"\
    \}\
\
triage_agent = LlmAgent(\
    name="Triage_Agent",\
    model="gemini-2.5-flash",\
    instruction="""\
    You are a triage nurse AI. Given patient vitals and chief complaint,\
    return an ESI level (1-5) where 1 is most urgent.\
    \
    ESI-1: Unresponsive, not breathing \uc0\u8594  immediate life threat\
    ESI-2: High risk (chest pain, severe respiratory distress)\
    ESI-3: Stable but needs resources\
    ESI-4: Stable, few resources needed\
    ESI-5: Minor complaint\
    \
    Use the assess_patient tool for consistent scoring.\
    """,\
    tools=[FunctionTool(assess_patient)]\
)}