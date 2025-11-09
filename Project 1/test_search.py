from search_engine import SearchEngine
import sys

print("Testing web search...")
sys.stdout.flush()

try:
    s = SearchEngine()
    print("SearchEngine initialized")
    sys.stdout.flush()
    
    results = s.search_question('is smoking bad for health', max_results=5)
    print(f"search_question returned, type: {type(results)}")
    sys.stdout.flush()

    print(f"Found {len(results)} results\n")

    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   URL: {r['url']}")
        print(f"   Snippet: {r['snippet'][:100]}...\n")

    if not results:
        print("ERROR: No results returned!")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
