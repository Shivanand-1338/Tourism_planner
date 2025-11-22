"""
Parent Tourism AI Agent - Orchestrates the multi-agent system
"""
import re
from typing import Dict, Optional
from geocoding import place_exists
from weather_agent import format_weather_response
from places_agent import format_places_response


class TourismAIAgent:
    """
    Parent agent that orchestrates weather and places agents
    """
    
    def __init__(self):
        self.weather_keywords = [
            "weather", "temperature", "temp", "rain", "rainfall",
            "forecast", "climate", "rainy", "sunny", "cloudy"
        ]
        self.places_keywords = [
            "places", "attractions", "tourist", "visit", "see",
            "sightseeing", "where to go", "things to do", "must see",
            "plan", "planning", "trip"
        ]
    
    def parse_user_intent(self, user_input: str) -> Dict[str, bool]:
        """
        Parse user input to determine what information they need
        
        Args:
            user_input: User's input string
            
        Returns:
            Dictionary with flags for weather and places
        """
        input_lower = user_input.lower()
        
        wants_weather = any(keyword in input_lower for keyword in self.weather_keywords)
        wants_places = any(keyword in input_lower for keyword in self.places_keywords)
        
        # If no specific keywords, default to both
        if not wants_weather and not wants_places:
            wants_places = True
        
        return {
            "weather": wants_weather,
            "places": wants_places
        }
    
    def extract_place_name(self, user_input: str) -> Optional[str]:
        """
        Extract place name from user input
        
        Args:
            user_input: User's input string
            
        Returns:
            Extracted place name or None
        """
        # Keywords that indicate the end of place name
        stop_keywords = [
            "what", "where", "when", "which", "who", "how",
            "let's", "let us", "plan", "planning", "temperature",
            "temp", "weather", "places", "attractions", "visit",
            "can", "should", "will", "is", "are", "and"
        ]
        
        # Common patterns - improved to better extract place names (case-insensitive)
        patterns = [
            # Pattern: "visiting/going to [place]"
            r"(?:going\s+to|visit|visiting|trip\s+to|travel\s+to|heading\s+to|am\s+visiting)\s+([a-zA-Z][a-zA-Z\s]*?)(?:\s+(?:what|where|when|let|plan|conditions)|,|\.|$)",
            # Pattern: "in [place]"
            r"in\s+([a-zA-Z][a-zA-Z\s]*?)(?:\s+(?:what|where|when|it|the|conditions)|,|\.|$)",
            # Pattern: "[Place], let's/what/where"
            r"^([a-zA-Z][a-zA-Z\s]+?),?\s+(?:let's|let\s+us|what|where|temperature|and)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                place_name = match.group(1).strip()
                # Clean up the place name and remove any stop keywords
                place_name = re.sub(r'\s+', ' ', place_name)
                
                # Remove any stop keywords that might have been captured
                words = place_name.split()
                cleaned_words = []
                for word in words:
                    if word.lower() not in stop_keywords:
                        cleaned_words.append(word)
                    else:
                        break
                
                if cleaned_words:
                    # Preserve original capitalization but ensure first letter is capitalized
                    place_name = ' '.join(cleaned_words)
                    # Only title case if all lowercase, otherwise preserve original case
                    if place_name.islower():
                        place_name = place_name.title()
                    elif not place_name[0].isupper():
                        place_name = place_name[0].upper() + place_name[1:]
                    return place_name
        
        # Fallback: try to extract capitalized or all-lowercase city names
        words = user_input.split()
        place_words = []
        
        for i, word in enumerate(words):
            # Check if word looks like it could be part of a place name
            # (capitalized or all lowercase after certain keywords)
            if i > 0 and words[i-1].lower() in ["to", "visit", "visiting", "in", "going"]:
                # Next word(s) after these keywords are likely the place name
                j = i
                while j < len(words):
                    current_word = words[j].lower()
                    # Stop if we hit a question keyword
                    if current_word in stop_keywords:
                        break
                    # Stop if we hit punctuation
                    if words[j] in [",", ".", "?", "!"]:
                        break
                    place_words.append(words[j])
                    j += 1
                break
        
        if place_words:
            place_name = ' '.join(place_words)
            # Remove trailing punctuation
            place_name = re.sub(r'[,.!?]+$', '', place_name)
            place_name = place_name.title()
            return place_name
        
        return None
    
    def process_request(self, user_input: str) -> str:
        """
        Main method to process user request
        
        Args:
            user_input: User's input string
            
        Returns:
            Formatted response string
        """
        # Extract place name
        place_name = self.extract_place_name(user_input)
        
        if not place_name:
            return "I couldn't identify the place you want to visit. Could you please specify the place name?"
        
        # Check if place exists
        if not place_exists(place_name):
            return f"I don't know if the place '{place_name}' exists. Could you check the spelling?"
        
        # Parse intent
        intent = self.parse_user_intent(user_input)
        
        # Collect responses from child agents
        responses = []
        
        if intent["weather"]:
            weather_response = format_weather_response(place_name)
            # Check if weather agent returned an error
            if f"I don't know" in weather_response:
                responses.append(weather_response)
            else:
                responses.append(weather_response)
        
        if intent["places"]:
            places_response = format_places_response(place_name)
            # Check if places agent returned an error
            if f"I don't know" in places_response:
                responses.append(places_response)
            else:
                responses.append(places_response)
        
        # Combine responses
        if len(responses) == 2:
            # Combine weather and places responses
            weather_part = responses[0]
            places_part = responses[1]
            
            # Remove redundant place name from places part if it starts with "In {place_name}"
            if places_part.startswith(f"In {place_name}"):
                # Replace the beginning to match Example 3 format
                places_part = places_part.replace(
                    f"In {place_name} these are the places you can go,", 
                    "And these are the places you can go:"
                )
            
            return f"{weather_part} {places_part}"
        elif len(responses) == 1:
            return responses[0]
        else:
            return f"I couldn't process your request for {place_name}. Please try again."

