{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Simulates patient arrivals with realistic patterns\
"""\
\
import random\
from datetime import datetime\
from typing import List, Dict\
\
class PatientStreamSimulator:\
    """Generates mock patient data with configurable surge patterns"""\
    \
    def __init__(self, base_arrival_rate: float = 8.0):\
        self.base_arrival_rate = base_arrival_rate\
        self.surge_active = False\
        self.surge_multiplier = 1.0\
        \
        self.complaints = [\
            "Chest pain", "Shortness of breath", "Broken ankle",\
            "Headache", "Fever", "Abdominal pain", "Laceration",\
            "Unresponsive", "Seizure", "Allergic reaction"\
        ]\
    \
    def activate_surge(self, multiplier: float = 2.5):\
        """Simulate a surge event"""\
        self.surge_active = True\
        self.surge_multiplier = multiplier\
    \
    def deactivate_surge(self):\
        """End surge simulation"""\
        self.surge_active = False\
        self.surge_multiplier = 1.0\
    \
    def generate_patient(self) -> Dict:\
        """Generate a single mock patient"""\
        complaint = random.choice(self.complaints)\
        \
        # Generate realistic vitals based on complaint\
        if "chest" in complaint.lower():\
            hr = random.randint(100, 130)\
            spo2 = random.randint(92, 97)\
            esi = 2\
        elif "unresponsive" in complaint.lower():\
            hr = random.randint(40, 60)\
            spo2 = random.randint(80, 90)\
            esi = 1\
        elif "breath" in complaint.lower():\
            hr = random.randint(95, 115)\
            spo2 = random.randint(88, 94)\
            esi = 2\
        else:\
            hr = random.randint(70, 100)\
            spo2 = random.randint(95, 99)\
            esi = random.choice([3, 4, 5])\
        \
        return \{\
            "patient_id": f"P\{random.randint(100, 999)\}",\
            "timestamp": datetime.now().isoformat(),\
            "chief_complaint": complaint,\
            "heart_rate": hr,\
            "spo2": spo2,\
            "esi_level": esi\
        \}\
    \
    def get_arrival_rate(self) -> float:\
        """Get current arrival rate (patients per hour)"""\
        rate = self.base_arrival_rate\
        if self.surge_active:\
            rate *= self.surge_multiplier\
        return rate}