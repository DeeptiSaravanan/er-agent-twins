{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Memory update logic - stores simulation outcomes and feedback\
"""\
\
from agents.memory_config import get_or_create_session, store_memory\
from datetime import datetime\
from typing import Dict, Optional\
\
class MemoryUpdater:\
    """\
    Responsible for storing outcomes and ingesting feedback\
    """\
    \
    def __init__(self):\
        self.session = get_or_create_session()\
    \
    def store_prediction_outcome(self, prediction: Dict, actual_outcome: Optional[Dict] = None):\
        """Store what actually happened after a prediction"""\
        store_memory(self.session, \{\
            'type': 'prediction_outcome',\
            'prediction': prediction,\
            'actual': actual_outcome,\
            'was_accurate': None if actual_outcome is None else self._evaluate_accuracy(prediction, actual_outcome),\
            'timestamp': datetime.now().isoformat()\
        \})\
    \
    def ingest_feedback(self, feedback: Dict):\
        """Receive human feedback and update memory weights"""\
        store_memory(self.session, \{\
            'type': 'human_feedback',\
            'feedback': feedback.get('rating'),\
            'notes': feedback.get('notes'),\
            'prediction_id': feedback.get('prediction_id'),\
            'timestamp': datetime.now().isoformat()\
        \})\
        \
        return \{"status": "stored", "will_improve_future": True\}\
    \
    def update_accuracy(self, prediction_id: str, was_accurate: bool):\
        """Update a stored prediction with accuracy feedback"""\
        # In production, this would update the specific memory\
        # For hackathon, we store a new linked memory\
        store_memory(self.session, \{\
            'type': 'accuracy_feedback',\
            'prediction_id': prediction_id,\
            'was_accurate': was_accurate,\
            'timestamp': datetime.now().isoformat()\
        \})\
    \
    def _evaluate_accuracy(self, prediction: Dict, actual: Dict) -> bool:\
        """Simple accuracy evaluation logic"""\
        predicted_prob = prediction.get('surge_probability', 0)\
        actual_surge_occurred = actual.get('surge_occurred', False)\
        \
        predicted_surge = predicted_prob > 0.7\
        return predicted_surge == actual_surge_occurred\
\
memory_updater = MemoryUpdater()}