from pathlib import Path

def segment_text(text, chunk_size=1500, chunk_overlap=200):
    """
    Splits long text documents into smaller chunks (segments) for RAG embedding.
    Ensures that context is preserved via overlapping segments.
    """
    if not text:
        return []
        
    chunks = []
    # Convert text to a list of words for token-like counting
    words = text.split()
    
    # Iterate through the words and create overlapping slices
    for i in range(0, len(words), chunk_size - chunk_overlap):
        # Create a chunk from current position up to chunk_size
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        # Stop if we have reached the end of the text
        if i + chunk_size >= len(words):
            break
            
    return chunks

if __name__ == "__main__":
    # Example usage for testing
    sample = "Word " * 1500
    segments = segment_text(sample, chunk_size=500, chunk_overlap=100)
    print(f"Total chunks: {len(segments)}")
    for j, s in enumerate(segments):
        print(f"Chunk {j+1} length: {len(s.split())} words")
