from sentence_transformers import SentenceTransformer
import torch

class LocalSentenceTransformer:
    """
    Wrapper for SentenceTransformer models.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"\n[Embedder] Initializing...")
        print(f"[Embedder] Model: {model_name}")
        print(f"[Embedder] Device detected: {self.device}")
        print(f"[Embedder] Loading weights (this can take 10-30s on first run)...")
        
        try:
            self.model = SentenceTransformer(model_name, device=self.device)
            print(f"[Embedder] Model loaded successfully.")
        except Exception as e:
            print(f"[Embedder] Error loading model: {e}")
            raise

    def encode(self, sentences: list, batch_size: int = 32):
        """
        Convert a list of sentences into embeddings.
        """
        return self.model.encode(
            sentences, 
            batch_size=batch_size, 
            show_progress_bar=False,
            convert_to_numpy=True
        )

    def get_dimension(self):
        """Returns the embedding dimension of the model."""
        return self.model.get_sentence_embedding_dimension()
