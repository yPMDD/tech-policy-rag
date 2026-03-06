import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
import sys

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from vectorstore.manager import VectorStoreManager

DOCUMENTS_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.json"
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned" / "en"
VECTORS_DIR = PROJECT_ROOT / "data" / "vectors"

def populate_store():
    """
    Reads vectors and text chunks and populates ChromaDB.
    """
    if not DOCUMENTS_JSON.exists():
        print(f"Error: {DOCUMENTS_JSON} not found. Run embedding pipeline first.")
        return

    with open(DOCUMENTS_JSON, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    v_manager = VectorStoreManager(provider="chroma")
    
    # We'll batch documents for efficiency
    all_doc_ids = []
    all_embeddings = []
    all_metadatas = []
    all_texts = []

    print("\n--- Populating Vector Store ---")
    
    for doc in registry.get('documents', []):
        doc_id = doc['doc_id']
        category = doc['category']
        vector_path = PROJECT_ROOT / doc['paths'].get('vectors', "")
        chunks_path = PROJECT_ROOT / doc['paths'].get('cleaned', "")

        if not vector_path.exists() or not chunks_path.exists():
            print(f"Skipping {doc_id}: Vector or Cleaned path missing.")
            continue

        print(f"Processing {doc_id}...")
        
        # Load vectors (.npy file containing array of vectors)
        embeddings = np.load(vector_path)
        
        # Load corresponding text chunks
        chunk_files = sorted(list(chunks_path.glob("chunk_*.txt")))
        
        if len(embeddings) != len(chunk_files):
            print(f"Warning: Vector count ({len(embeddings)}) mismatch with chunk count ({len(chunk_files)}) for {doc_id}")
            continue

        for i, (emb, cf) in enumerate(zip(embeddings, chunk_files)):
            chunk_id = f"{doc_id}_{i:03d}"
            
            with open(cf, 'r', encoding='utf-8') as f:
                text = f.read()

            all_doc_ids.append(chunk_id)
            all_embeddings.append(emb.tolist())
            all_metadatas.append({
                "doc_id": doc_id,
                "category": category,
                "chunk_index": i,
                "source": doc.get('source_url', 'unknown')
            })
            all_texts.append(text)

    if all_texts:
        print(f"Adding {len(all_texts)} items to ChromaDB...")
        # ChromaDB handles batching internally, but we can do it explicitly if needed
        # For now, we'll send everything in one go as it's small (249 items)
        v_manager.add_documents(
            ids=all_doc_ids,
            embeddings=all_embeddings,
            metadatas=all_metadatas,
            documents=all_texts
        )
        print("Success: Vector store populated.")
    else:
        print("No documents found to add.")

if __name__ == "__main__":
    populate_store()
