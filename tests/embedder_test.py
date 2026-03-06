import sys
import os
import time
import numpy as np
from pathlib import Path

# Add project root to sys.path so we can import from 'embeddings'
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Use absolute imports from project root
try:
    from embeddings.embedder import Embedder
except ImportError:
    # Fallback for different execution contexts
    print("Warning: Direct import failed, trying relative adjustment...")
    sys.path.append(os.getcwd())
    from embeddings.embedder import Embedder

def test_embedder():
    print("--- Initializing Embedder (this may take a moment to load model) ---")
    embedder = Embedder()
    
    test_text = "The General Data Protection Regulation (GDPR) is a regulation in EU law."
    
    # 1. First run (should be a cache miss)
    print("\n[Test 1] First embedding (model run)...")
    start_time = time.time()
    vector1 = embedder.embed_text(test_text)
    duration1 = time.time() - start_time
    print(f"Done in {duration1:.4f}s. Vector shape: {vector1.shape}")
    
    # 2. Second run (should be a cache hit)
    print("\n[Test 2] Second embedding (should hit Redis cache)...")
    start_time = time.time()
    vector2 = embedder.embed_text(test_text)
    duration2 = time.time() - start_time
    print(f"Done in {duration2:.4f}s.")
    
    # Verify they are identical
    if np.allclose(vector1, vector2):
        print("Success: Vectors are identical!")
    else:
        print("Warning: Vectors differ! Check your cache implementation.")
        
    if duration2 < duration1:
        print(f"Success: Cache hit was {duration1/duration2:.1f}x faster than model run!")
    else:
        print("Warning: Cache hit wasn't faster. This might happen on the first run if Redis is cold.")

    # 3. Batch embedding
    print("\n[Test 3] Batch embedding...")
    batch_texts = [
        "Digital Services Act (DSA)",
        "Artificial Intelligence Act (AI Act)",
        "NIS2 Directive"
    ]
    start_time = time.time()
    batch_vectors = embedder.embed_text(batch_texts)
    duration3 = time.time() - start_time
    print(f"Batch embedding of {len(batch_texts)} texts took {duration3:.4f}s.")
    print(f"Batch vector shape: {batch_vectors.shape}")

if __name__ == "__main__":
    try:
        test_embedder()
    except Exception as e:
        print(f"\nTest failed: {e}")
