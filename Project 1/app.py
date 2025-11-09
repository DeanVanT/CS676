"""
URL Credibility Checker Chatbot - Enhanced Conversational Edition
Built with Streamlit for Deliverable 3

This chatbot analyzes URLs for credibility using multiple evaluation criteria:
- Reference credibility (ML-based fake news detection)
- Fact-checking (domain reputation analysis)
- Citation analysis (reference counting and quality)

NEW: Now with conversational AI, multi-URL comparison, and educational responses!
"""

import streamlit as st
import re
from typing import Optional, List, Dict
from deliverable1_3 import analyze_url_credibility
from conversational_ai import ConversationalAI, Intent
from search_engine import SearchEngine
from urllib.parse import urlparse

# Configure Streamlit page
st.set_page_config(
    page_title="URL Credibility Checker AI",
    page_icon="🔍",
    layout="centered"
)

# Initialize conversational AI
if "ai" not in st.session_state:
    st.session_state.ai = ConversationalAI()

# Initialize search engine
if "search" not in st.session_state:
    st.session_state.search = SearchEngine()

# Initialize enhanced session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "analyzed_urls" not in st.session_state:
    st.session_state.analyzed_urls = []  # History of all analyzed URLs

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "session_stats" not in st.session_state:
    st.session_state.session_stats = {
        'total_analyzed': 0,
        'highly_credible': 0,
        'topics': []
    }

def extract_all_urls(text: str) -> List[str]:
    """
    Extract ALL URLs from user message.
    Supports multiple URLs in one message.
    """
    url_pattern = r'(?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    matches = re.findall(url_pattern, text)
    
    # Normalize URLs
    normalized = []
    for url in matches:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        normalized.append(url)
    
    return normalized

def format_credibility_response(result: dict, include_suggestions: bool = False) -> str:
    """
    Format the credibility analysis results into a readable chat message.
    """
    if not result.get("success"):
        error_msg = f"❌ **Error**: {result.get('error', 'Unknown error occurred')}"
        
        # Offer helpful suggestions on error
        if "validation failed" in result.get('error', '').lower():
            error_msg += "\n\n💡 **Tip:** Make sure the URL is correctly formatted (e.g., https://example.com)"
        
        return error_msg
    
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
    
    # Add suggestions for low-scoring URLs
    if include_suggestions and final_score < 0.6:
        domain = urlparse(result['url']).netloc
        response += f"\n\n⚠️ **This source scored relatively low.** Consider checking more authoritative sources."
        response += f"\n\n💡 Want me to suggest more credible alternatives? Just ask!"
    
    return response

def format_search_results_response(search_results: List[Dict], analyzed_results: List[dict]) -> str:
    """
    Format search results with credibility analysis and rankings
    """
    if not search_results:
        return "❌ No search results found. Try a different query."
    
    if not analyzed_results:
        return "❌ Could not analyze search results."
    
    # Sort by credibility score
    sorted_results = sorted(analyzed_results, key=lambda x: x.get('final_score', 0) if x.get('success') else -1, reverse=True)
    
    response = f"🔎 **Found {len(search_results)} sources. Here they are ranked by credibility:**\n\n"
    
    for i, result in enumerate(sorted_results, 1):
        if not result.get('success'):
            continue
        
        # Find original search result for title/snippet
        search_result = next((sr for sr in search_results if sr['url'] == result['url']), None)
        
        emoji_map = {
            "Poor": "🔴",
            "Fair": "🟠",
            "Good": "🟡",
            "Very Good": "🟢",
            "Excellent": "🟢"
        }
        emoji = emoji_map.get(result['tranche'], "⚪")
        
        response += f"""
**{i}. {emoji} {result['tranche']}** (Score: {result['final_score']:.2f})
   📰 **{search_result['title'] if search_result else 'Source'}**
   🔗 `{result['url']}`
   
   • Credibility: {result['individual_scores']['credibility']:.2f}
   • Fact-Check: {result['individual_scores']['fact_check']:.2f}
   • Citations: {result['individual_scores']['citations']:.2f}

"""
    
    # Add recommendations
    high_quality = [r for r in sorted_results if r.get('success') and r['final_score'] >= 0.7]
    if high_quality:
        response += f"\n✅ **Recommended:** I'd suggest reading the top {min(3, len(high_quality))} sources (highest credibility)"
    else:
        response += f"\n⚠️ **Note:** None of these sources scored highly. Consider searching for more authoritative sources."
    
    return response

def format_comparison_response(results: List[dict]) -> str:
    """
    Format multiple URL analyses for side-by-side comparison
    """
    if not results:
        return "❌ No results to compare."
    
    response = f"📊 **Comparing {len(results)} URLs:**\n\n"
    
    # Sort by score (highest first)
    sorted_results = sorted(results, key=lambda x: x.get('final_score', 0) if x.get('success') else -1, reverse=True)
    
    for i, result in enumerate(sorted_results, 1):
        if not result.get('success'):
            response += f"**{i}.** ❌ Error analyzing URL\n"
            continue
        
        emoji_map = {
            "Poor": "🔴",
            "Fair": "🟠", 
            "Good": "🟡",
            "Very Good": "🟢",
            "Excellent": "🟢"
        }
        emoji = emoji_map.get(result['tranche'], "⚪")
        
        response += f"""
**{i}. {emoji} {result['tranche']}** (Score: {result['final_score']:.2f})
   📍 `{result['url']}`
   • Credibility: {result['individual_scores']['credibility']:.2f}
   • Fact-Check: {result['individual_scores']['fact_check']:.2f}
   • Citations: {result['individual_scores']['citations']:.2f}

"""
    
    # Add recommendation
    if sorted_results[0].get('success'):
        response += f"\n✅ **Most Credible:** URL #{1} with a score of {sorted_results[0]['final_score']:.2f}"
    
    return response

# App Title and Description
st.title("🔍 URL Credibility Checker AI")
st.markdown("""
Welcome! I'm your **intelligent credibility assistant with search capabilities**. I can:

� **Search & Analyze** - Ask me questions and I'll find and rank credible sources  
�🔍 **Analyze URLs** - Check credibility of any URL you provide  
📊 **Compare Sources** - Rank multiple sources side-by-side  
📚 **Answer Questions** - Learn about credibility and fact-checking  
💬 **Chat Naturally** - Just talk to me like a person  

**Try these:**
- 🆕 **Search:** `Find credible sources about smoking`
- 🆕 **Ask:** `Are cigarettes addictive?` (I'll search and analyze for you!)
- Send URL: `Check https://www.cdc.gov`
- Compare: `Compare example.com vs nature.com`
- Learn: `How do you score URLs?`
""")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything or send me a URL to check..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Build session context for AI
    session_context = {
        'previous_urls': [a['url'] for a in st.session_state.analyzed_urls],
        'last_analysis': st.session_state.last_analysis,
        'stats': st.session_state.session_stats
    }
    
    # Detect intent using conversational AI
    intent = st.session_state.ai.detect_intent(prompt, session_context)
    
    # Process based on intent
    with st.chat_message("assistant"):
        if intent.type == 'search':
            # Search for sources and analyze them
            response_obj = st.session_state.ai.generate_response(intent, session_context)
            if isinstance(response_obj, dict) and response_obj.get('type') == 'search':
                st.markdown(response_obj['message'])
                
                with st.spinner("🔎 Searching and analyzing sources..."):
                    # Search for sources
                    search_results = st.session_state.search.search_and_filter(intent.search_query, max_results=8, min_results=5)
                    
                    if search_results:
                        # Clear previous search results to prevent stale data
                        st.session_state.analyzed_urls = []
                        
                        # Analyze each URL
                        analyzed_results = []
                        for search_result in search_results:
                            url = search_result['url']
                            result = analyze_url_credibility(url)
                            
                            if result.get('success'):
                                analyzed_results.append(result)
                                st.session_state.analyzed_urls.append(result)
                                st.session_state.session_stats['total_analyzed'] += 1
                                
                                if result['final_score'] >= 0.8:
                                    st.session_state.session_stats['highly_credible'] += 1
                        
                        # Format and display results
                        response = format_search_results_response(search_results, analyzed_results)
                        st.session_state.last_analysis = analyzed_results[0] if analyzed_results else None
                    else:
                        response = "❌ No search results found. Try rephrasing your question."
            else:
                response = response_obj
        
        elif intent.type == 'analyze':
            # Analyze single or multiple URLs
            urls = intent.urls
            
            if len(urls) == 1:
                # Single URL analysis
                with st.spinner(f"Analyzing {urls[0]}... This may take a moment for the first analysis."):
                    result = analyze_url_credibility(urls[0])
                    response = format_credibility_response(result, include_suggestions=True)
                    
                    # Update session state
                    if result.get('success'):
                        st.session_state.last_analysis = result
                        st.session_state.analyzed_urls.append(result)
                        st.session_state.session_stats['total_analyzed'] += 1
                        
                        if result['final_score'] >= 0.8:
                            st.session_state.session_stats['highly_credible'] += 1
            
            else:
                # Multiple URL comparison
                with st.spinner(f"Analyzing {len(urls)} URLs for comparison..."):
                    results = []
                    for url in urls:
                        result = analyze_url_credibility(url)
                        results.append(result)
                        
                        if result.get('success'):
                            st.session_state.analyzed_urls.append(result)
                            st.session_state.session_stats['total_analyzed'] += 1
                            
                            if result['final_score'] >= 0.8:
                                st.session_state.session_stats['highly_credible'] += 1
                    
                    response = format_comparison_response(results)
                    st.session_state.last_analysis = results[0] if results else None
        
        elif intent.type == 'compare':
            # Compare with previous URLs
            if len(intent.urls) > 0:
                # New URLs provided
                urls_to_compare = intent.urls
            elif len(st.session_state.analyzed_urls) >= 2:
                # Compare last two
                urls_to_compare = [st.session_state.analyzed_urls[-2]['url'], st.session_state.analyzed_urls[-1]['url']]
            else:
                response = "I need at least 2 URLs to compare. Send me multiple URLs in one message, or analyze another URL first!"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.stop()
            
            with st.spinner("Comparing URLs..."):
                results = []
                for url in urls_to_compare:
                    # Check if already analyzed
                    existing = next((a for a in st.session_state.analyzed_urls if a['url'] == url), None)
                    if existing:
                        results.append(existing)
                    else:
                        result = analyze_url_credibility(url)
                        results.append(result)
                        if result.get('success'):
                            st.session_state.analyzed_urls.append(result)
                
                response = format_comparison_response(results)
        
        elif intent.type in ['greeting', 'thanks', 'educate', 'chat', 'followup']:
            # Use conversational AI for response
            response = st.session_state.ai.generate_response(intent, session_context)
        
        else:
            # Fallback
            response = """
🤔 I'm not sure how to help with that.

**I can:**
• Analyze any URL you send me
• Compare multiple sources
• Explain my methodology
• Answer questions about credibility

Just ask or send me a URL!
            """
        
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with enhanced info and stats
with st.sidebar:
    st.header("Dean Van Tassell Chatbot credibility checker")
    st.markdown("""
    This **AI-powered chatbot** evaluates URL credibility using three key metrics:
    
    **🤖 Reference Credibility (35%)**
    - Uses ML model to detect fake news patterns
    - Analyzes page content quality
    
    **✅ Fact-Check Score (35%)**
    - Evaluates domain reputation
    - Checks against 80+ authoritative sources
    
    **📚 Citation Analysis (30%)**
    - Counts references and citations
    - Validates DOI presence
    
    **Score Ranges:**
    - 🟢 0.80-1.00: Excellent
    - 🟢 0.60-0.79: Very Good
    - 🟡 0.40-0.59: Good
    - 🟠 0.20-0.39: Fair
    - 🔴 0.00-0.19: Poor
    """)
    
    # Session statistics
    st.header("📈 Session Stats")
    stats = st.session_state.session_stats
    st.metric("URLs Analyzed", stats['total_analyzed'])
    st.metric("Highly Credible", stats['highly_credible'])
    
    if stats['total_analyzed'] > 0:
        credibility_rate = (stats['highly_credible'] / stats['total_analyzed']) * 100
        st.metric("Credibility Rate", f"{credibility_rate:.0f}%")
    
    st.divider()
    
    # Recently analyzed URLs
    if st.session_state.analyzed_urls:
        st.header("📚 Recent Analyses")
        for analysis in reversed(st.session_state.analyzed_urls[-3:]):  # Last 3
            domain = urlparse(analysis['url']).netloc
            tranche = analysis.get('tranche', 'Unknown')
            
            emoji_map = {"Poor": "🔴", "Fair": "🟠", "Good": "🟡", "Very Good": "🟢", "Excellent": "🟢"}
            emoji = emoji_map.get(tranche, "⚪")
            
            st.text(f"{emoji} {domain}")
            st.caption(f"{tranche} ({analysis['final_score']:.2f})")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.analyzed_urls = []
        st.session_state.last_analysis = None
        st.session_state.session_stats = {
            'total_analyzed': 0,
            'highly_credible': 0,
            'topics': []
        }
        st.rerun()
