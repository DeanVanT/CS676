"""
Internet Search Module for URL Credibility Checker
Uses SerpAPI for Google search - free tier: 100 searches/month
Get your free API key at: https://serpapi.com/users/sign_up
"""

from typing import List, Dict
import os

class SearchEngine:
    """
    Performs web searches using SerpAPI (Google results).
    Free tier: 100 searches/month, no credit card required.
    """
    
    def __init__(self):
        # API key embedded
        self.api_key = '33ac2a621762c56967e962a20e4e83c853b1888fdd887ab0d8cee46628d6500d'
    
    def search_question(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search Google via SerpAPI and return actual results.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of dicts with 'title', 'url', 'snippet' keys
        """
        if not self.api_key:
            print("ERROR: No API key configured. Cannot search.")
            return []
            
        try:
            from serpapi import GoogleSearch
            
            params = {
                "q": query,
                "num": max_results,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results_data = search.get_dict()
            
            results = []
            if "organic_results" in results_data:
                for item in results_data["organic_results"][:max_results]:
                    results.append({
                        'title': item.get('title', 'No title'),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', 'No description available')
                    })
            
            print(f"SerpAPI found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def search_and_filter(self, query: str, max_results: int = 10, min_results: int = 5) -> List[Dict[str, str]]:
        """
        Search and filter out duplicate domains.
        Returns diverse sources from different domains.
        
        Args:
            query: Search query
            max_results: Maximum results to fetch initially
            min_results: Minimum unique results to return
            
        Returns:
            List of unique domain results
        """
        try:
            all_results = self.search_question(query, max_results=max_results)
            
            # Filter to unique domains
            seen_domains = set()
            unique_results = []
            
            for result in all_results:
                url = result['url']
                # Extract domain
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                
                # Remove www.
                if domain.startswith('www.'):
                    domain = domain[4:]
                
                if domain not in seen_domains:
                    seen_domains.add(domain)
                    unique_results.append(result)
                
                if len(unique_results) >= min_results:
                    break
            
            return unique_results
            
        except Exception as e:
            print(f"Search filter error: {e}")
            return []
    
    def search_topic_with_context(self, topic: str, context: str = "credible sources") -> List[Dict[str, str]]:
        """
        Search for a topic with added context for better results.
        
        Args:
            topic: The main topic (e.g., "cigarette addiction")
            context: Context to add (default: "credible sources")
            
        Returns:
            Search results
        """
        enhanced_query = f"{topic} {context}"
        return self.search_and_filter(enhanced_query, max_results=8, min_results=5)


def test_search():
    """Test function for development"""
    search = SearchEngine()
    
    print("Testing search: 'Are cigarettes addictive?'")
    results = search.search_question("Are cigarettes addictive?", max_results=5)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:100]}...")


if __name__ == "__main__":
    test_search()
