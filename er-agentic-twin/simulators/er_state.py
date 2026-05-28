"""
Simulates ER state including beds, queue, and wait times
"""

from typing import List, Dict

class ERStateSimulator:
    """Maintains current ER state for simulation"""
    
    def __init__(self, total_beds: int = 24, doctors: int = 4, nurses: int = 8):
        self.total_beds = total_beds
        self.doctors = doctors
        self.nurses = nurses
        
        self.occupied_beds = random.randint(12, 20)
        self.patient_queue = []
        self.doctors_available = random.randint(1, 3)
        self.nurses_available = random.randint(2, 5)
    
    @property
    def available_beds(self) -> int:
        return self.total_beds - self.occupied_beds
    
    @property
    def load_percentage(self) -> float:
        return (self.occupied_beds / self.total_beds) * 100
    
    def add_patient(self, patient: Dict):
        """Add patient to queue"""
        self.patient_queue.append(patient)
    
    def discharge_patient(self):
        """Simulate patient discharge"""
        if self.occupied_beds > 0:
            self.occupied_beds -= 1
    
    def update_shift(self, hour: int):
        """Update state based on time of day"""
        # Lunch rush (12-2 PM)
        if 12 <= hour <= 14:
            self.occupied_beds = min(self.total_beds, self.occupied_beds + 3)
        # Evening surge (6-9 PM)
        elif 18 <= hour <= 21:
            self.occupied_beds = min(self.total_beds, self.occupied_beds + 4)
        # Night slowdown (1-5 AM)
        elif 1 <= hour <= 5:
            self.occupied_beds = max(8, self.occupied_beds - 2)
    
    def get_state(self) -> dict:
        """Get current ER state"""
        return {
            "total_beds": self.total_beds,
            "available_beds": self.available_beds,
            "occupied_beds": self.occupied_beds,
            "load_percentage": self.load_percentage,
            "queue_length": len(self.patient_queue),
            "doctors_available": self.doctors_available,
            "nurses_available": self.nurses_available
        }

import random  # Add at top of file
