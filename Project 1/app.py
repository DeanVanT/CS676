"""
URL Credibility Checker Chatbot
Built with Streamlit for Deliverable 3

This chatbot analyzes URLs for credibility using multiple evaluation criteria:
- Reference credibility (ML-based fake news detection)
- Fact-checking (domain reputation analysis)
- Citation analysis (reference counting and quality)
"""

import streamlit as st
import re
from typing import Optional
from deliverable1_3 import analyze_url_credibility

# Configure Streamlit page
st.set_page_config(
    page_title="URL Credibility Checker",
    page_icon="🔍",
    layout="centered"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_url(text: str) -> Optional[str]:
    """
    Extract URL from user message using regex.
    Supports URLs with or without http/https scheme.
    """
    # Pattern matches common URL formats
    url_pattern = r'(?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

def format_credibility_response(result: dict) -> str:
    """
    Format the credibility analysis results into a readable chat message.
    """
    if not result.get("success"):
        return f"❌ **Error**: {result.get('error', 'Unknown error occurred')}"
    
    # Build response with emojis and formatting
    tranche = result['tranche']
    final_score = result['final_score']
    
    # Choose emoji based on tranche
    emoji_map = {
        "Poor": "🔴",
        "Fair": "🟠",
        "Good": "🟡",
        "Very Good": "🟢",
        "Excellent": "🟢"
    }
    emoji = emoji_map.get(tranche, "⚪")
    
    response = f"""
{emoji} **Overall Credibility: {tranche}** (Score: {final_score:.2f}/1.00)

**📊 Detailed Breakdown:**

**1. Reference Credibility** ({result['individual_scores']['credibility']:.2f})
└─ {result['explanations']['credibility']}

**2. Fact-Check Score** ({result['individual_scores']['fact_check']:.2f})
└─ {result['explanations']['fact_check']}

**3. Citation Analysis** ({result['individual_scores']['citations']:.2f})
└─ {result['explanations']['citations']}

---
🔗 Analyzed URL: `{result['url']}`
"""
    return response

# App Title and Description
st.title("🔍 URL Credibility Checker")
st.markdown("""
Welcome! I can analyze the credibility of any URL you provide. Just send me a message containing a URL, 
and I'll evaluate it based on multiple criteria including content credibility, domain reputation, and citation quality.

**Example:** Send me "Check this URL: https://example.com"
""")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Send me a URL to check its credibility..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process the message
    with st.chat_message("assistant"):
        # Check if message contains a URL
        url = extract_url(prompt)
        
        if url:
            with st.spinner(f"Analyzing {url}... This may take a moment for the first analysis."):
                # Analyze the URL
                result = analyze_url_credibility(url)
                response = format_credibility_response(result)
        else:
            response = """
👋 Hi! I'm the URL Credibility Checker. 

I didn't detect a URL in your message. Please send me a message containing a URL to analyze.

**Examples:**
- `Check https://www.nature.com/articles/example`
- `How credible is example.com?`
- `Analyze this: github.com/username/repo`
"""
        
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with additional info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot evaluates URL credibility using three key metrics:
    
    **🤖 Reference Credibility (35%)**
    - Uses ML model to detect fake news patterns
    - Analyzes page content quality
    
    **✅ Fact-Check Score (35%)**
    - Evaluates domain reputation
    - Checks against authoritative sources
    
    **📚 Citation Analysis (30%)**
    - Counts references and citations
    - Validates DOI presence
    
    **Score Ranges:**
    - 🟢 0.80-1.00: Excellent/Very Good
    - 🟡 0.60-0.79: Good
    - 🟠 0.40-0.59: Fair
    - 🔴 0.00-0.39: Poor
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
