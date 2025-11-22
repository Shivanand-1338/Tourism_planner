"""
Streamlit Web Application for Tourism AI System
"""
import streamlit as st
from tourism_ai_agent import TourismAIAgent

# Page configuration
st.set_page_config(
    page_title="Tourism AI System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .response-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: rgb(12, 12, 143);
        border-left: 5px solid #1f77b4;
        margin-top: 1rem;
    }
    .example-box {
        padding: 0.8rem;
        background-color: red;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = TourismAIAgent()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<h1 class="main-header">🌍 Tourism AI System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent travel planning assistant</p>', unsafe_allow_html=True)

# Sidebar with examples and info
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    Enter a place you want to visit and ask about:
    - **Weather conditions**
    - **Tourist attractions**
    - **Both weather and places**
    """)
    
    st.header("💡 Example Queries")
    
    example_queries = [
        "I'm going to go to Bangalore, let's plan my trip.",
        "I'm visiting Delhi, what is the weather conditions",
        "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
        "I'm traveling to Paris, show me places to visit",
        "I'm heading to Mumbai, what's the weather like?"
    ]
    
    for example in example_queries:
        with st.container():
            st.markdown(f'<div class="example-box">{example}</div>', unsafe_allow_html=True)
    
    st.header("ℹ️ About")
    st.markdown("""
    This system uses:
    - **Open-Meteo API** for weather data
    - **Overpass API** for tourist attractions
    - **Nominatim API** for geocoding
    
    All APIs are free and open-source!
    """)

# Main content area
st.markdown("---")

# Input section
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Enter your query:",
        placeholder="e.g., I'm going to go to Bangalore, let's plan my trip.",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("🚀 Submit", type="primary", use_container_width=True)

# Process query
if submit_button and user_input:
    with st.spinner("Processing your request..."):
        response = st.session_state.agent.process_request(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "query": user_input,
            "response": response
        })

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation History")
    
    for idx, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
        with st.expander(f"Query: {chat['query'][:50]}..." if len(chat['query']) > 50 else f"Query: {chat['query']}", expanded=(idx == 0)):
            st.markdown(f"**Your Query:**")
            st.info(chat['query'])
            
            st.markdown(f"**Tourism AI Response:**")
            # Format response with better styling
            response_lines = chat['response'].split('\n')
            formatted_response = ""
            for line in response_lines:
                if line.strip().startswith('-'):
                    formatted_response += f"  {line}\n"
                else:
                    formatted_response += f"{line}\n"
            
            st.markdown(f'<div class="response-box">{formatted_response.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

# Clear history button
if st.session_state.chat_history:
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Built with ❤️ using Streamlit | Tourism AI Multi-Agent System
    </div>
    """,
    unsafe_allow_html=True
)

