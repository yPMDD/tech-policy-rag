import numpy as np
from typing import List, Union
from embeddings.models.sentence_transformer import LocalSentenceTransformer
from embeddings.cache import RedisCache

class Embedder:
    """
    Main entry point for generating embeddings with integrated caching.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = LocalSentenceTransformer(model_name)
        self.cache = RedisCache()

    def embed_text(self, text: Union[str, List[str]], use_cache: bool = True) -> np.ndarray:
        """
        Embed a single string or a list of strings, checking the cache first.
        """
        if isinstance(text, str):
            if use_cache:
                cached = self.cache.get_embedding(text)
                if cached is not None:
                    return cached
            
            embedding = self.model.encode([text])[0]
            
            if use_cache:
                self.cache.set_embedding(text, embedding)
            return embedding
        
        # Batch processing
        return self._embed_batch(text, use_cache)

    def _embed_batch(self, texts: List[str], use_cache: bool) -> np.ndarray:
        results = [None] * len(texts)
        to_embed_indices = []
        to_embed_texts = []

        if use_cache:
            for idx, text in enumerate(texts):
                cached = self.cache.get_embedding(text)
                if cached is not None:
                    results[idx] = cached
                else:
                    to_embed_indices.append(idx)
                    to_embed_texts.append(text)
        else:
            to_embed_indices = list(range(len(texts)))
            to_embed_texts = texts

        if to_embed_texts:
            embeddings = self.model.encode(to_embed_texts)
            for idx, embedding in zip(to_embed_indices, embeddings):
                results[idx] = embedding
                if use_cache:
                    self.cache.set_embedding(texts[idx], embedding)

        return np.array(results)

if __name__ == "__main__":
    # Simple status check when run directly
    print("--- Embedder Status Check ---")
    try:
        e = Embedder()
        print(f"Model: {e.model.model_name}")
        print(f"Device: {e.model.device}")
        print(f"Dimension: {e.model.get_dimension()}")
        print(f"Redis Cache: {'Connected' if e.cache.redis else 'Disconnected'}")
        print("\nEmbedder is ready.")
    except Exception as err:
        print(f"Status check failed: {err}")
