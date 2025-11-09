"""
Conversational AI Module for URL Credibility Checker
Handles intent detection, chitchat, and educational responses
100% free, no subscriptions required
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Intent:
    """Represents detected user intent"""
    type: str  # 'analyze', 'compare', 'chat', 'educate', 'greeting', 'thanks', 'search'
    urls: List[str]
    topic: Optional[str] = None
    context: Optional[str] = None
    search_query: Optional[str] = None  # For search intent

class ConversationalAI:
    """
    Free conversational AI using rule-based intent detection and pre-written responses.
    No API keys or subscriptions needed!
    """
    
    def __init__(self):
        # Knowledge base for educational responses
        self.knowledge_base = {
            "methodology": """
🎯 **How I Score URLs:**

I evaluate credibility across **three dimensions**:

**1. Reference Credibility (35% weight)**
• Uses ML model to detect fake news patterns in content
• Analyzes writing quality and information reliability

**2. Fact-Check Score (35% weight)**
• Evaluates domain reputation (.gov, .edu, scientific journals)
• Checks against 80+ authoritative sources

**3. Citation Analysis (30% weight)**
• Counts references and citations
• Validates DOI presence and bibliography quality

The final score (0.0-1.0) is a weighted average of these three components.
            """,
            
            "credibility": """
📚 **What Makes a Source Credible?**

A credible source typically has:

✅ **Authority**: Written by experts or recognized institutions
✅ **Accuracy**: Facts are verifiable and well-cited
✅ **Objectivity**: Presents balanced, unbiased information
✅ **Currency**: Information is up-to-date and timely
✅ **Citations**: References other credible sources

**Red flags** include:
❌ No author or organization listed
❌ No citations or references
❌ Sensational headlines or emotional language
❌ Domain from unverified sources
            """,
            
            "domains": """
🌐 **Domain Types Explained:**

**.gov** - Government websites (highest trust)
└─ Example: cdc.gov, nih.gov

**.edu** - Educational institutions (high trust)
└─ Example: harvard.edu, mit.edu

**.org** - Organizations (varies by organization)
└─ Can be non-profits, research groups, or advocacy

**.com** - Commercial sites (varies widely)
└─ Ranges from news outlets to personal blogs

**Pro tip:** Domain extension alone doesn't guarantee credibility, but .gov and .edu from established institutions are generally more reliable.
            """,
            
            "fake_news": """
🔍 **How to Spot Fake News:**

**Check the source:**
• Is it a known, reputable outlet?
• Does the site have an "About" page?

**Verify the author:**
• Is there an author listed?
• Can you find their credentials?

**Look for citations:**
• Are there links to original sources?
• Can you verify the claims independently?

**Check the date:**
• Is the information current?
• Is it being shared out of context?

**Be skeptical of:**
• ALL CAPS headlines
• Extreme emotional language
• Claims that seem too good/bad to be true
• Single-source stories with no corroboration
            """
        }
        
        # Greeting patterns
        self.greetings = [
            r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b',
        ]
        
        # Thanks patterns
        self.thanks = [
            r'\b(thanks|thank you|thx|appreciate|grateful)\b',
        ]
        
        # Educational keywords
        self.educate_keywords = {
            'methodology': [r'how (do you|does it) (work|score)', r'methodology', r'how (are|do) (you|urls?) (scored|evaluated|rated)'],
            'credibility': [r'what (is|makes) (a )?(credible|reliable|trustworthy) source', r'credibility', r'trust'],
            'domains': [r'(what|difference|explain).*(\.gov|\.edu|\.com|\.org|domain)', r'domain types'],
            'fake_news': [r'(spot|detect|identify|find) (fake|false) news', r'fake news', r'misinformation']
        }
        
        # Search trigger patterns
        self.search_patterns = [
            r'\b(find|search|look up|get|show me|give me).*(sources?|articles?|info|information)\b',
            r'\b(where can i|how can i).*(find|read|learn)\b',
            r'\bfind (credible|reliable|trustworthy) sources?\b'
        ]
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract all URLs from text"""
        url_pattern = r'(?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        matches = re.findall(url_pattern, text)
        
        # Normalize URLs
        normalized = []
        for url in matches:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            normalized.append(url)
        
        return normalized
    
    def detect_intent(self, message: str, session_context: Dict) -> Intent:
        """
        Detect user intent from message using pattern matching
        100% free, no API calls
        """
        message_lower = message.lower()
        urls = self.extract_urls(message)
        
        # Check for greetings
        if any(re.search(pattern, message_lower) for pattern in self.greetings):
            return Intent(type='greeting', urls=urls)
        
        # Check for thanks
        if any(re.search(pattern, message_lower) for pattern in self.thanks):
            return Intent(type='thanks', urls=urls)
        
        # Check for search requests (before educational, as they can overlap)
        if not urls and any(re.search(pattern, message_lower) for pattern in self.search_patterns):
            # Extract topic from message
            topic = message.strip('?').strip()
            # Remove search trigger words to get clean query
            clean_query = re.sub(r'\b(find|search|look up|get|show me|give me|where can i|how can i|credible|reliable|trustworthy|sources?|articles?)\b', '', message_lower, flags=re.IGNORECASE)
            clean_query = clean_query.strip()
            return Intent(type='search', urls=[], search_query=clean_query or message, topic=message)
        
        # Check for educational queries
        for topic, patterns in self.educate_keywords.items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                return Intent(type='educate', urls=urls, topic=topic)
        
        # Check for comparison requests
        if len(urls) > 1 or (re.search(r'\b(compare|vs|versus|which is better|difference between)\b', message_lower) and session_context.get('previous_urls')):
            return Intent(type='compare', urls=urls)
        
        # Check for follow-up about previous analysis
        if not urls and session_context.get('last_analysis'):
            follow_up_patterns = [
                r'\b(why|how|explain|tell me more|details?)\b',
                r'\b(what about|more info|elaborate)\b',
                r'\b(low|high|poor|good|excellent) score\b'
            ]
            if any(re.search(pattern, message_lower) for pattern in follow_up_patterns):
                return Intent(type='followup', urls=[], context='explain_last')
        
        # Check if asking question without URL (automatically search)
        question_patterns = [
            r'\b(what|who|when|where|why|how|is|are|do|does|can|should|will|would)\b',
            r'\?$'
        ]
        if not urls and any(re.search(pattern, message_lower) for pattern in question_patterns):
            # Automatically trigger search for questions
            return Intent(type='search', urls=[], search_query=message, topic=message.strip('?').strip())
        
        # If URLs present, analyze them
        if urls:
            return Intent(type='analyze', urls=urls)
        
        # Default to general chat
        return Intent(type='chat', urls=[], topic=message)
    
    def generate_response(self, intent: Intent, session_context: Dict = None) -> str:
        """Generate appropriate response based on intent"""
        
        if intent.type == 'greeting':
            return """
👋 **Hello! I'm the URL Credibility Checker AI!**

I can help you:
• 🔍 Analyze the credibility of any URL
• � **Search and find credible sources on any topic**
• �📊 Compare multiple sources
• 📚 Teach you about identifying credible information
• 💬 Answer questions about my methodology

**Try these:**
- Send me a URL: `Check https://www.nature.com`
- **Search for sources:** `Find credible sources about nutrition`
- Compare: `Compare cdc.gov vs example.com`
- Learn: `How do you score URLs?`
            """
        
        elif intent.type == 'search':
            return {
                'type': 'search',
                'query': intent.search_query,
                'message': f"""
🔎 **Searching for credible sources about:** _{intent.topic}_

I'll find relevant sources and rank them by credibility...
                """
            }
        
        elif intent.type == 'thanks':
            responses = [
                "You're welcome! Feel free to send more URLs anytime. 😊",
                "Happy to help! Let me know if you need more URLs checked. 👍",
                "My pleasure! I'm here if you need more credibility checks. ✨",
            ]
            import random
            return random.choice(responses)
        
        elif intent.type == 'educate':
            topic = intent.topic
            return self.knowledge_base.get(topic, "I don't have information on that topic yet. Try asking about methodology, credibility, domains, or fake news detection.")
        
        elif intent.type == 'chat':
            # Generic chat response
            return """
💬 I'm here to help you evaluate source credibility!

**I can:**
• 🔍 Analyze any URL's credibility
• 🔎 Search for credible sources on any topic
• 📊 Compare multiple sources
• 📚 Explain my methodology

Try asking a question or send me a URL!
            """
        
        elif intent.type == 'followup':
            if session_context and session_context.get('last_analysis'):
                last = session_context['last_analysis']
                return f"""
📋 **About your previous analysis:**

The URL scored **{last.get('tranche', 'N/A')}** ({last.get('final_score', 0):.2f}/1.00)

**Why this score?**

{self._explain_score(last)}

**Want to:**
• Check another URL?
• Learn more about my methodology?
• Compare this with another source?
            """
            else:
                return "I don't have a previous analysis to explain. Send me a URL to analyze!"
        
        return "I'm not sure how to help with that. Try sending me a URL to analyze, or ask me about my methodology!"
    
    def _explain_score(self, analysis: Dict) -> str:
        """Explain why a score was given"""
        scores = analysis.get('individual_scores', {})
        explanations = analysis.get('explanations', {})
        
        breakdown = []
        
        # Credibility
        cred_score = scores.get('credibility', 0)
        if cred_score >= 0.7:
            breakdown.append("✅ **Content analysis** detected reliable patterns")
        elif cred_score >= 0.4:
            breakdown.append("⚠️ **Content analysis** found some concerning patterns")
        else:
            breakdown.append("❌ **Content analysis** detected unreliable content patterns")
        
        # Fact-check
        fact_score = scores.get('fact_check', 0)
        if fact_score >= 0.8:
            breakdown.append("✅ **Domain** is from a highly authoritative source")
        elif fact_score >= 0.6:
            breakdown.append("👍 **Domain** has good reputation")
        else:
            breakdown.append("⚠️ **Domain** is not from a recognized authoritative source")
        
        # Citations
        cite_score = scores.get('citations', 0)
        if cite_score >= 0.7:
            breakdown.append("✅ **Citations** are abundant and well-formatted")
        elif cite_score >= 0.5:
            breakdown.append("👍 **Citations** are present but limited")
        else:
            breakdown.append("❌ **Citations** are sparse or missing")
        
        return "\n".join(breakdown)
    
    def suggest_alternatives(self, domain: str, topic: str = None) -> str:
        """Suggest more credible alternatives based on domain type"""
        suggestions = {
            'health': ['cdc.gov', 'nih.gov', 'who.int', 'mayoclinic.org'],
            'science': ['nature.com', 'science.org', 'arxiv.org', 'pubmed.ncbi.nlm.nih.gov'],
            'news': ['reuters.com', 'apnews.com', 'bbc.com'],
            'tech': ['ieee.org', 'acm.org', 'arxiv.org'],
            'general': ['britannica.com', 'wikipedia.org (with citations)']
        }
        
        # Detect topic from domain or use general
        detected_topic = 'general'
        for topic_key in suggestions.keys():
            if topic_key in domain.lower():
                detected_topic = topic_key
                break
        
        alts = suggestions[detected_topic]
        
        return f"""
🔄 **More credible alternatives for {detected_topic} topics:**

{chr(10).join(f"• {alt}" for alt in alts)}

Send me any of these URLs to verify their credibility!
        """
