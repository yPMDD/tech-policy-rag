import os
import redis
import hashlib
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    """
    Manages embedding cache in Redis to avoid redundant computations.
    """
    def __init__(self):
        host = os.getenv("REDIS_HOST")
        port = int(os.getenv("REDIS_PORT"))
        password = os.getenv("REDIS_PASSWORD")
        self.db_key_prefix = os.getenv("REDIS_DB_KEY")
        
        try:
            self.redis = redis.Redis(
                host=host, 
                port=port, 
                password=password,
                decode_responses=False
            )
            # Test connection
            self.redis.ping()
        except redis.ConnectionError as e:
            print(f"Warning: Could not connect to Redis: {e}")
            self.redis = None

    def _get_hash(self, text: str) -> str:
        """Generate a stable hash for a given text segment."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get_embedding(self, text: str):
        """Retrieve embedding from Redis if it exists."""
        if not self.redis:
            return None
            
        key = f"{self.db_key_prefix}:emb:{self._get_hash(text)}"
        cached = self.redis.get(key)
        
        if cached:
            # Convert back to numpy array from binary
            return np.frombuffer(cached, dtype=np.float32)
        return None

    def set_embedding(self, text: str, embedding: np.ndarray):
        """Store embedding in Redis."""
        if not self.redis:
            return
            
        key = f"{self.db_key_prefix}:emb:{self._get_hash(text)}"
        # Store as raw binary for efficiency
        self.redis.set(key, embedding.astype(np.float32).tobytes())
