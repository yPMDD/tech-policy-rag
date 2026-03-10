import time
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from rag.pipeline import RAGPipeline

def test_cache_performance():
    rag = RAGPipeline()
    query = "What is the maximum administrative fine under GDPR?"
    
    print(f"\n--- Testing Cache Performance ---")
    print(f"Query: {query}\n")
    
    # First Run (Cold Cache)
    print("Execution 1 (Cold Cache)...")
    start_cold = time.time()
    res1 = rag.ask(query)
    end_cold = time.time()
    time_cold = end_cold - start_cold
    print(f"Status: {res1['status']}")
    print(f"Time: {time_cold:.2f}s\n")
    
    # Second Run (Hot Cache)
    print("Execution 2 (Hot Cache)...")
    start_hot = time.time()
    res2 = rag.ask(query)
    end_hot = time.time()
    time_hot = end_hot - start_hot
    print(f"Status: {res2['status']}")
    print(f"Time: {time_hot:.4f}s")
    
    improvement = (time_cold / time_hot) if time_hot > 0 else float('inf')
    print(f"\nSpeedup: {improvement:.1f}x faster!")

if __name__ == "__main__":
    test_cache_performance()
