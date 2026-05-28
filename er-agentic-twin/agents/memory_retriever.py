"""
Memory retrieval logic - queries past patterns to augment current decisions
"""

from agents.memory_config import get_or_create_session, retrieve_memories
from typing import List, Dict

class MemoryRetriever:
    """
    Responsible for semantic search over historical memories
    """
    
    def __init__(self):
        self.session = get_or_create_session()
    
    def retrieve_surge_patterns(self, hour: int, day: str, is_holiday: bool = False) -> List[Dict]:
        """Retrieve historical surge patterns matching current context"""
        query = f"surge pattern {day} {hour}:00"
        if is_holiday:
            query += " holiday"
        
        memories = retrieve_memories(self.session, query, limit=5)
        
        formatted = []
        for m in memories:
            if m.get('type') == 'simulation_result':
                formatted.append({
                    'surge_probability': m.get('surge_probability'),
                    'was_accurate': m.get('was_accurate'),
                    'recommendation': m.get('recommendation'),
                    'timestamp': m.get('timestamp')
                })
        
        return formatted
    
    def get_historical_adjustment_factor(self, hour: int, day: str) -> float:
        """Calculate how much to adjust predictions based on historical accuracy"""
        patterns = self.retrieve_surge_patterns(hour, day)
        
        if not patterns:
            return 1.0
        
        accurate_count = sum(1 for p in patterns if p.get('was_accurate') is True)
        inaccurate_count = sum(1 for p in patterns if p.get('was_accurate') is False)
        
        if accurate_count + inaccurate_count == 0:
            return 1.0
        
        accuracy_rate = accurate_count / (accurate_count + inaccurate_count)
        
        if accuracy_rate < 0.5:
            return 0.8
        return 1.0

# Singleton instance
memory_retriever = MemoryRetriever()
