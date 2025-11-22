"""
Geocoding utility using Nominatim API
"""
import requests
from typing import Optional, Tuple


def get_coordinates(place_name: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude for a place using Nominatim API
    
    Args:
        place_name: Name of the place to geocode
        
    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    
    headers = {
        "User-Agent": "Tourism-AI-Agent/1.0"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])
            return (lat, lon)
        
        return None
    except Exception as e:
        print(f"Error in geocoding: {e}")
        return None


def place_exists(place_name: str) -> bool:
    """
    Check if a place exists by attempting to geocode it
    
    Args:
        place_name: Name of the place to check
        
    Returns:
        True if place exists, False otherwise
    """
    return get_coordinates(place_name) is not None

