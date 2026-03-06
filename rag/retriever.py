"""
rag/retriever.py - Handles context retrieval from the vector store.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from embeddings.pipeline import get_embedder
from vectorstore.manager import VectorStoreManager

class Retriever:
    """
    Connects the Embedder and VectorStore to retrieve relevant legal context.
    """
    def __init__(self, provider: str = "chroma"):
        self.embedder = get_embedder()
        self.vector_store = VectorStoreManager(provider=provider)

    def get_context(self, query: str, n_results: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves the most relevant chunks for a given query.
        """
        # 1. Embed user query
        query_vector = self.embedder.embed_text(query).tolist()
        
        # 2. Build metadata filter if category is provided
        where_filter = {"category": category} if category else None
        
        # 3. Search vector store
        results = self.vector_store.search(
            query_embeddings=[query_vector],
            n_results=n_results,
            where=where_filter
        )
        
        # 4. Format results into a list of dictionaries
        formatted_results = []
        if results and 'ids' in results and results['ids']:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i]
                })
        
        return formatted_results

if __name__ == "__main__":
    # Quick standalone test
    retriever = Retriever()
    hits = retriever.get_context("How is AI defined?", n_results=2)
    for hit in hits:
        print(f"[{hit['score']:.4f}] {hit['id']}: {hit['text'][:100]}...")
