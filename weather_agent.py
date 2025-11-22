"""
Weather Agent - Uses Open-Meteo API to get current weather and forecast
"""
import requests
from typing import Optional, Dict
from geocoding import get_coordinates


def get_weather(place_name: str) -> Optional[Dict]:
    """
    Get current weather for a place using Open-Meteo API
    
    Args:
        place_name: Name of the place
        
    Returns:
        Dictionary with weather information, or None if place not found
    """
    # First, get coordinates
    coords = get_coordinates(place_name)
    
    if not coords:
        return None
    
    lat, lon = coords
    
    # Open-Meteo API endpoint
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation_probability,weather_code",
        "timezone": "auto"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "current" in data:
            current = data["current"]
            return {
                "temperature": current.get("temperature_2m", "N/A"),
                "precipitation_probability": current.get("precipitation_probability", 0),
                "weather_code": current.get("weather_code", 0)
            }
        
        return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None


def format_weather_response(place_name: str) -> str:
    """
    Format weather information as a natural language response
    
    Args:
        place_name: Name of the place
        
    Returns:
        Formatted weather response string
    """
    weather_data = get_weather(place_name)
    
    if not weather_data:
        return f"I don't know if the place '{place_name}' exists. Could you check the spelling?"
    
    temp = weather_data["temperature"]
    precip_prob = weather_data["precipitation_probability"]
    
    return f"In {place_name} it's currently {temp}°C with a chance of {precip_prob}% to rain."

