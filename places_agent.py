"""
Places Agent - Uses Overpass API to get tourist attractions
"""
import requests
from typing import Optional, List
from geocoding import get_coordinates


def get_tourist_attractions(place_name: str, limit: int = 5) -> Optional[List[str]]:
    """
    Get tourist attractions for a place using Overpass API
    
    Args:
        place_name: Name of the place
        limit: Maximum number of attractions to return (default: 5)
        
    Returns:
        List of tourist attraction names, or None if place not found
    """
    # First, get coordinates
    coords = get_coordinates(place_name)
    
    if not coords:
        return None
    
    lat, lon = coords
    
    # Overpass API query to find tourist attractions
    # We'll search for tourist attractions, parks, museums, monuments within ~10km
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Overpass QL query to find tourist attractions
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"](around:10000,{lat},{lon});
      node["leisure"](around:10000,{lat},{lon});
      way["tourism"](around:10000,{lat},{lon});
      way["leisure"](around:10000,{lat},{lon});
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={"data": query}, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        attractions = []
        seen_names = set()
        
        if "elements" in data:
            for element in data["elements"]:
                if "tags" in element:
                    tags = element["tags"]
                    
                    # Try different tag combinations for names
                    name = (
                        tags.get("name") or
                        tags.get("name:en") or
                        tags.get("tourism") or
                        tags.get("leisure")
                    )
                    
                    if name and name not in seen_names:
                        attractions.append(name)
                        seen_names.add(name)
                        
                        if len(attractions) >= limit:
                            break
        
        # If we didn't get enough results, try a broader search
        if len(attractions) < limit:
            broader_query = f"""
            [out:json][timeout:25];
            (
              node["tourism"]["name"](around:20000,{lat},{lon});
              way["tourism"]["name"](around:20000,{lat},{lon});
              relation["tourism"]["name"](around:20000,{lat},{lon});
            );
            out center;
            """
            
            response = requests.post(overpass_url, data={"data": broader_query}, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "elements" in data:
                for element in data["elements"]:
                    if "tags" in element and len(attractions) < limit:
                        tags = element["tags"]
                        name = tags.get("name") or tags.get("name:en")
                        
                        if name and name not in seen_names:
                            attractions.append(name)
                            seen_names.add(name)
                            
                            if len(attractions) >= limit:
                                break
        
        return attractions if attractions else None
        
    except Exception as e:
        print(f"Error fetching tourist attractions: {e}")
        return None


def format_places_response(place_name: str) -> str:
    """
    Format tourist attractions as a natural language response
    
    Args:
        place_name: Name of the place
        
    Returns:
        Formatted places response string
    """
    attractions = get_tourist_attractions(place_name)
    
    if not attractions:
        return f"I don't know if the place '{place_name}' exists. Could you check the spelling?"
    
    if len(attractions) == 0:
        return f"I couldn't find any tourist attractions for {place_name}."
    
    response = f"In {place_name} these are the places you can go,\n"
    
    for attraction in attractions:
        response += f"- {attraction}\n"
    
    return response.strip()

