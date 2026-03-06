"""
embeddings/pipeline.py - Official entry point for the Embedding Layer.

This module provides:
1. run_embeddings_pipeline(): Processes all chunks in the registry into vectors.
2. get_embedder(): Returns a pre-configured Embedder instance for use in RAG.
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path to ensure absolute imports work
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import our modules
from embeddings.embedder import Embedder
from embeddings.batch_embed import run_batch_embedding

def run_embeddings_pipeline():
    """
    Orchestrates a full batch embedding run for the entire document registry.
    Updates documents.json with the new vector paths.
    """
    print("\n--- Starting Embeddings Pipeline (Knowledge Base) ---")
    run_batch_embedding()
    print("--- Embeddings Pipeline Completed ---")

def get_embedder(model_name: str = "all-MiniLM-L6-v2"):
    """
    Factory function to get a pre-configured Embedder instance.
    This is what you'll use in the final RAG pipeline for user queries.
    """
    return Embedder(model_name=model_name)

if __name__ == "__main__":
    # If run directly as a script, execute the full batch pipeline
    run_embeddings_pipeline()
