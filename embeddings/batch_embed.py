import os
import sys
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from embeddings.embedder import Embedder
DOCUMENTS_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.json"
VECTORS_DIR = PROJECT_ROOT / "data" / "vectors"

def run_batch_embedding():
    """
    Orchestrates the embedding process for all documents in the registry.
    """
    if not DOCUMENTS_JSON.exists():
        print(f"Error: {DOCUMENTS_JSON} not found. Run processing pipeline first.")
        return

    with open(DOCUMENTS_JSON, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    embedder = Embedder()
    VECTORS_DIR.mkdir(parents=True, exist_ok=True)

    total_chunks_processed = 0
    
    for doc in registry.get('documents', []):
        doc_id = doc['doc_id']
        category = doc['category']
        cleaned_path = PROJECT_ROOT / doc['paths']['cleaned']
        
        if not cleaned_path.exists():
            print(f"Skipping {doc_id}, cleaned directory not found at {cleaned_path}")
            continue

        print(f"--- Embedding {doc_id} ({category}) ---")
        
        # Collect all chunks for this document
        chunk_files = sorted(list(cleaned_path.glob("chunk_*.txt")))
        if not chunk_files:
            continue

        texts = []
        for cf in chunk_files:
            with open(cf, 'r', encoding='utf-8') as f:
                texts.append(f.read())

        # Generate embeddings (uses Redis cache internally)
        embeddings = embedder.embed_text(texts)

        # Save vectors to disk
        # We save as a single .npy file per document for efficiency
        doc_vector_dir = VECTORS_DIR / category
        doc_vector_dir.mkdir(parents=True, exist_ok=True)
        vector_file = doc_vector_dir / f"{doc_id}.npy"
        
        np.save(vector_file, embeddings)
        
        # Update registry with vector path
        doc['paths']['vectors'] = str(vector_file.relative_to(PROJECT_ROOT))
        doc['ingestion']['embedder'] = 'policylens-embedding-v1'
        
        total_chunks_processed += len(texts)

    # Save updated registry
    with open(DOCUMENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)

    print(f"\nEmbedding Completed: {total_chunks_processed} chunks vectorized and stored in {VECTORS_DIR}")

if __name__ == "__main__":
    run_batch_embedding()
