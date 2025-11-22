# Tourism AI System

A multi-agent tourism system that helps users plan trips by providing weather information and tourist attraction suggestions for any place they want to visit.

## Features

- **Multi-Agent Architecture**: Parent agent orchestrates specialized child agents
- **Weather Information**: Get current temperature and precipitation probability using Open-Meteo API
- **Tourist Attractions**: Get up to 5 tourist attraction suggestions using Overpass API
- **Error Handling**: Gracefully handles non-existent places with appropriate error messages
- **Natural Language Processing**: Understands user intent from natural language queries

## System Architecture

1. **Parent Agent**: `TourismAIAgent` - Orchestrates the entire system, parses user intent, and coordinates child agents
2. **Child Agent 1**: `Weather Agent` - Uses Open-Meteo API to fetch current weather information
3. **Child Agent 2**: `Places Agent` - Uses Overpass API and Nominatim API to find tourist attractions
4. **Geocoding Utility**: Uses Nominatim API to convert place names to coordinates

## APIs Used

- **Nominatim API** (OpenStreetMap): Geocoding - converts place names to coordinates
  - Base URL: https://nominatim.openstreetmap.org/search
  
- **Open-Meteo API**: Weather data - provides current temperature and precipitation probability
  - Endpoint: https://api.open-meteo.com/v1/forecast
  
- **Overpass API**: Tourist attractions - finds points of interest from OpenStreetMap data
  - Base URL: https://overpass-api.de/api/interpreter

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

Run the Streamlit web application:

```bash
streamlit run app.py
```

The web interface will open in your browser automatically at `http://localhost:8501`

### Command Line Interface

Alternatively, run the CLI version:

```bash
python main.py
```

### Example Queries

**Example 1 - Places Only:**
```
Input: I'm going to go to Bangalore, let's plan my trip.
Output: In Bangalore these are the places you can go,
- Lalbagh
- Sri Chamarajendra Park
- Bangalore palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

**Example 2 - Weather Only:**
```
Input: I'm going to go to Bangalore, what is the temperature there
Output: In Bangalore it's currently 24°C with a chance of 35% to rain.
```

**Example 3 - Weather and Places:**
```
Input: I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?
Output: In Bangalore it's currently 24°C with a chance of 35% to rain. And these are the places you can go:
- Lalbagh
- Sri Chamarajendra Park
- Bangalore palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

## Project Structure

```
Tourism_ai/
├── app.py                   # Streamlit web application
├── main.py                  # CLI application entry point
├── tourism_ai_agent.py      # Parent orchestrator agent
├── weather_agent.py         # Weather information child agent
├── places_agent.py          # Tourist attractions child agent
├── geocoding.py             # Geocoding utility (Nominatim)
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## How It Works

1. **User Input**: User enters a natural language query about a place they want to visit
2. **Place Extraction**: Parent agent extracts the place name from the user input
3. **Place Validation**: System checks if the place exists using Nominatim geocoding
4. **Intent Parsing**: Parent agent determines if user wants weather, places, or both
5. **Agent Execution**: 
   - If weather requested: Weather Agent fetches data from Open-Meteo API
   - If places requested: Places Agent uses Nominatim to geocode, then Overpass API to find attractions
6. **Response Formatting**: Parent agent formats and combines responses from child agents
7. **Error Handling**: If place doesn't exist, system returns appropriate error message

## Error Handling

The system handles various error scenarios:
- Non-existent places: Returns "I don't know if the place 'X' exists. Could you check the spelling?"
- API failures: Gracefully handles API timeouts and errors
- Invalid inputs: Prompts user for clarification

## Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and set:
   - **Main file path**: `app.py`
   - **Branch**: `main` (or your default branch)
6. Click "Deploy"

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

### Deploy to Other Platforms

#### Heroku
1. Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
2. Deploy using Heroku CLI or GitHub integration

#### PythonAnywhere
1. Upload files via web interface or Git
2. Create a web app pointing to `app.py`
3. Configure WSGI file for Streamlit

## Notes

- All APIs used are free and open-source
- No API keys required for the recommended APIs
- The system respects API rate limits with appropriate User-Agent headers
- Tourist attractions are limited to 5 results by default

## Assignment Summary

### Approach

I built a multi-agent tourism system following a modular architecture pattern. The system consists of a parent orchestrator agent (`TourismAIAgent`) that coordinates two specialized child agents: a Weather Agent and a Places Agent. The architecture allows for clear separation of concerns and easy extensibility.

**Key Technical Decisions:**
1. **Intent Parsing**: Implemented regex-based pattern matching for intent recognition instead of requiring external LLM APIs, making the system lightweight and API-key-free
2. **Modular Design**: Each agent is a separate module with focused responsibilities, following the single responsibility principle
3. **Error Handling**: Implemented comprehensive error handling at multiple levels (geocoding, API calls, response formatting)
4. **Response Formatting**: Created dedicated formatting functions to match exact output format specified in assignment examples

### Key Decisions

1. **No LLM Dependency**: Chose regex-based intent parsing over OpenAI/other LLM APIs to avoid API key requirements and reduce complexity
   - Uses keyword matching and pattern recognition for intent detection
   - Handles natural language variations through multiple regex patterns

2. **Open Source APIs Only**: Selected free, open-source APIs as recommended:
   - **Nominatim API** (OpenStreetMap) for geocoding
   - **Open-Meteo API** for weather data
   - **Overpass API** for tourist attractions
   - No authentication required, making deployment easier

3. **Web Interface**: Added Streamlit web application for better user experience
   - Modern, interactive UI
   - Easy deployment to Streamlit Cloud
   - Better accessibility than CLI-only version

4. **Place Name Extraction**: Implemented sophisticated regex-based extraction with:
   - Case-insensitive matching
   - Stop keyword detection to prevent over-extraction
   - Multiple fallback patterns for various input formats

5. **Overpass API Query Strategy**: Used multi-tiered query approach:
   - Primary search within 10km radius
   - Fallback to broader 20km search if insufficient results
   - Filters for tourism and leisure tags only

### Challenges & Solutions

1. **Challenge: Place Name Extraction from Natural Language**
   - **Problem**: Initial regex patterns couldn't handle variations like "i am visiting delhi what is weather conditions" - extracted "delhi what is weather conditions" instead of just "delhi"
   - **Solution**: 
     - Implemented stop keyword detection (what, where, when, temperature, etc.)
     - Used non-greedy regex patterns with explicit stop conditions
     - Added fallback logic for edge cases

2. **Challenge: Overpass API Query Complexity**
   - **Problem**: Overpass QL syntax is complex, and querying for tourist attractions requires understanding OSM data structure
   - **Solution**:
     - Studied Overpass QL documentation
     - Implemented queries targeting `tourism` and `leisure` tags
     - Added fallback queries with broader radius if initial query returns insufficient results
     - Filtered for named attractions only

3. **Challenge: Response Formatting to Match Examples**
   - **Problem**: Assignment examples required specific formatting (comma vs colon, exact phrasing)
   - **Solution**:
     - Created dedicated formatting functions for weather and places
     - Implemented conditional formatting for combined responses
     - Handled edge cases for single vs multiple agent responses

4. **Challenge: API Rate Limiting**
   - **Problem**: Free APIs have rate limits that could cause failures
   - **Solution**:
     - Added proper User-Agent headers as required by Nominatim
     - Implemented timeout handling for all API calls
     - Added error handling that provides helpful user feedback

5. **Challenge: Handling Non-Existent Places**
   - **Problem**: Need to distinguish between "place doesn't exist" vs "API error"
   - **Solution**:
     - Validate place existence using Nominatim before making other API calls
     - Return specific error messages that guide users
     - Handle API failures gracefully with informative messages

6. **Challenge: Web Application Deployment**
   - **Problem**: Need to make application publicly accessible for assignment submission
   - **Solution**:
     - Created Streamlit web wrapper for better user experience
     - Streamlit Cloud provides free hosting with easy GitHub integration
     - Added comprehensive deployment instructions in README

### Testing

The system was tested with various inputs including:
- Exact examples from assignment requirements
- Variations in phrasing and capitalization
- Non-existent places (error handling)
- Combined queries (weather + places)
- Different city names (Bangalore, Delhi, Paris, etc.)

All three example scenarios from the assignment work correctly:
1. Places-only queries
2. Weather-only queries
3. Combined weather and places queries

## License

This project is created as part of an assignment for Inkle.

