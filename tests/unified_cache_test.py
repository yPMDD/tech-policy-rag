import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from embeddings.cache import RedisCache

def test_unified_cache():
    print("--- Unified Redis Cache Test ---")
    cache = RedisCache()
    
    if not cache.redis:
        print("FAIL: Could not connect to local Redis.")
        return

    # Test Q&A Caching
    test_query = "What is the AI Act?"
    test_response = {"answer": "A regulatory framework for AI.", "status": "success"}
    
    print(f"Caching test query: '{test_query}'")
    cache.set_query_response(test_query, test_response)
    
    retrieved = cache.get_query_response(test_query)
    print(f"Retrieved from cache: {retrieved}")
    
    if retrieved == test_response:
        print("SUCCESS: Unified Q&A caching is working on localhost:6379!")
    else:
        print("FAIL: Data mismatch in cache.")

if __name__ == "__main__":
    test_unified_cache()
