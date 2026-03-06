import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

class ChromaClient:
    """
    Wrapper for ChromaDB persistent client.
    """
    def __init__(self, collection_name: str = "tech_policy_docs"):
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"} # Use cosine similarity
        )

    def add(self, 
            ids: List[str], 
            embeddings: List[List[float]], 
            metadatas: List[Dict[str, Any]], 
            documents: List[str]):
        """
        Add items to ChromaDB.
        """
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def query(self, 
              query_embeddings: List[List[float]], 
              n_results: int = 5, 
              where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar vectors.
        """
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )

    def delete_collection(self, name: str):
        self.client.delete_collection(name)

    def get_info(self):
        return {
            "count": self.collection.count(),
            "name": self.collection.name,
            "metadata": self.collection.metadata
        }
