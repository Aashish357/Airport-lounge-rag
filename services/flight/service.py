from .models import FLIGHTS_DB
from typing import Dict, Any

def get_flight_info(flight_number: str) -> Dict[str, Any]:
    """Retrieve flight information from database"""
    flight_number = flight_number.upper().strip()
    
    if flight_number not in FLIGHTS_DB:
        return None
    
    return FLIGHTS_DB[flight_number]