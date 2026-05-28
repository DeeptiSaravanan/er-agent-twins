{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Memory configuration for ER Agentic Twin\
Uses InMemoryMemoryService for hackathon demo (no GCP setup required)\
"""\
\
from google.adk.memory import InMemoryMemoryService\
from google.adk.sessions import InMemorySessionService\
from typing import Optional\
\
# Create memory and session services (both in-memory for hackathon)\
_memory_service = InMemoryMemoryService()\
_session_service = InMemorySessionService()\
\
# Session configuration\
APP_NAME = "er_agentic_twin"\
USER_ID = "charge_nurse_1"\
\
# Memory retrieval settings\
MAX_MEMORIES_TO_RETRIEVE = 5\
MEMORY_RELEVANCE_THRESHOLD = 0.7\
\
def get_memory_service():\
    """Returns memory service for dependency injection"""\
    return _memory_service\
\
def get_session_service():\
    """Returns session service for dependency injection"""\
    return _session_service\
\
def get_or_create_session(session_id: Optional[str] = None):\
    """Get existing session or create a new one"""\
    if session_id:\
        try:\
            return _session_service.get_session(\
                app_name=APP_NAME,\
                user_id=USER_ID,\
                session_id=session_id\
            )\
        except:\
            pass\
    \
    # Create new session\
    return _session_service.create_session(\
        app_name=APP_NAME,\
        user_id=USER_ID,\
        state=\{\}\
    )\
\
def store_memory(session, memory_data: dict):\
    """Store a memory in the memory bank"""\
    _memory_service.add_memory(\
        session=session,\
        memory=memory_data\
    )\
\
def retrieve_memories(session, query: str, limit: int = MAX_MEMORIES_TO_RETRIEVE):\
    """Retrieve memories by semantic search"""\
    return _memory_service.retrieve_memories(\
        session=session,\
        query=query,\
        limit=limit\
    )}