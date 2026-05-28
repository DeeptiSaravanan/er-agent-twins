"""
Resource Agent - Tracks bed, doctor, and equipment availability
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def get_resource_status() -> dict:
    """Tool: Returns current ER resource status"""
    return {
        "total_beds": 24,
        "available_beds": 6,
        "occupied_beds": 18,
        "cleaning_beds": 2,
        "doctors_on_duty": 4,
        "doctors_available": 2,
        "nurses_on_duty": 8,
        "nurses_available": 3,
        "ct_scanners": 2,
        "ct_available": 1
    }

def predict_bed_availability(minutes_ahead: int = 30) -> dict:
    """Tool: Predicts how many beds will be available"""
    # Simple prediction for demo
    return {
        "minutes_ahead": minutes_ahead,
        "beds_free_in_30min": 4,
        "beds_free_in_60min": 7,
        "confidence": "medium"
    }

resource_agent = LlmAgent(
    name="Resource_Agent",
    model="gemini-2.5-flash",
    instruction="""
    You track ER resource status and predict future availability.
    
    Tools:
    - get_resource_status: Current bed/doctor/nurse/CT availability
    - predict_bed_availability: Forecast for next 30-60 minutes
    
    When asked about capacity, always provide both current AND predicted status.
    """,
    tools=[
        FunctionTool(get_resource_status),
        FunctionTool(predict_bed_availability)
    ]
)
