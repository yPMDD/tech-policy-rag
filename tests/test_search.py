import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from embeddings.pipeline import get_embedder
from vectorstore.manager import VectorStoreManager

def test_search():
    print("--- Initializing Search Test ---")
    embedder = get_embedder()
    v_manager = VectorStoreManager(provider="chroma")
    
    queries = [
        "What are the rules for data breaches?",
        "How is AI defined in the EU AI Act?",
        "Right to be informed according to ICO"
    ]
    
    for query in queries:
        print(f"\nQUERY: {query}")
        print("-" * 30)
        
        # 1. Embed the query
        query_vector = embedder.embed_text(query).tolist()
        
        # 2. Search the vector store
        results = v_manager.search(
            query_embeddings=[query_vector],
            n_results=2
        )
        
        # 3. Print results
        for i in range(len(results['ids'][0])):
            chunk_id = results['ids'][0][i]
            doc_text = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            
            print(f"RESULT {i+1} (Score: {distance:.4f})")
            print(f"ID: {chunk_id} | Category: {metadata.get('category')}")
            # Ensure text can be printed on Windows consoles with limited encoding
            safe_text = doc_text[:200].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            print(f"Snippet: {safe_text}...")
            print("-" * 10)

if __name__ == "__main__":
    test_search()
