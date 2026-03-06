import os
from typing import List, Dict, Any, Optional

class VectorStoreManager:
    """
    Base manager to handle different vector store providers.
    Initially supports ChromaDB.
    """
    def __init__(self, provider: str = "chroma"):
        self.provider = provider
        if provider == "chroma":
            from .chroma.client import ChromaClient
            self.client = ChromaClient()
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def add_documents(self, 
                      ids: List[str], 
                      embeddings: List[List[float]], 
                      metadatas: List[Dict[str, Any]], 
                      documents: List[str]):
        """
        Add a batch of documents, their embeddings, and metadata to the store.
        """
        self.client.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def search(self, 
               query_embeddings: List[List[float]], 
               n_results: int = 5, 
               where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query the store for the nearest neighbors.
        """
        return self.client.query(query_embeddings=query_embeddings, n_results=n_results, where=where)

    def delete_collection(self, name: str):
        """
        Remove a collection of vectors.
        """
        self.client.delete_collection(name)

    def get_collection_info(self):
        """
        Returns info about the current collection.
        """
        return self.client.get_info()
