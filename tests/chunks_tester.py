"""
chunks_tester.py - Diagnostic script to inspect the quality of generated text chunks.

Run with: uv run python tests/chunks_tester.py [doc_id]
Example:  uv run python tests/chunks_tester.py gdpr_legal_text
          uv run python tests/chunks_tester.py          (shows summary for ALL docs)
"""
import sys
from pathlib import Path

# Navigate up from tests/ to the project root, then into the cleaned folder
CLEANED_DIR = Path(__file__).parent.parent / "data" / "cleaned" / "en"

def test_all():
    """Print a summary table of all documents and their chunk statistics."""
    # Chunks now live in: cleaned/en/{category}/{doc_id}/chunk_NNN.txt
    chunks_by_doc = {}
    for f in sorted(CLEANED_DIR.rglob("chunk_*.txt")):
        # The doc_id is the parent folder name, category is the grandparent
        doc_id = f.parent.name
        category = f.parent.parent.name
        key = f"{category}/{doc_id}"
        chunks_by_doc.setdefault(key, []).append(f)

    print(f"\n{'CATEGORY/DOC_ID':<55} {'CHUNKS':>6}  {'MIN (bytes)':>11}  {'MAX (bytes)':>11}  {'AVG (bytes)':>11}")
    print("-" * 105)
    total_chunks = 0
    for key, files in chunks_by_doc.items():
        sizes = [f.stat().st_size for f in files]
        print(f"{key:<55} {len(files):>6}  {min(sizes):>11,}  {max(sizes):>11,}  {int(sum(sizes)/len(sizes)):>11,}")
        total_chunks += len(files)
    print("-" * 105)
    print(f"{'TOTAL':<55} {total_chunks:>6}")

def test_doc(doc_id):
    """Show a preview of each chunk for a specific document."""
    # Search recursively to find the doc_id folder regardless of category
    matches = list(CLEANED_DIR.rglob(f"{doc_id}/chunk_*.txt"))
    files = sorted(matches)

    if not files:
        print(f"No chunks found for doc_id: '{doc_id}'")
        print("Available doc IDs:")
        ids = sorted(set(f.parent.name for f in CLEANED_DIR.rglob("chunk_*.txt")))
        for i in ids:
            print(f"  - {i}")
        return

    doc_folder = files[0].parent
    print(f"\n=== Chunk inspection for: {doc_id} ({len(files)} chunks) ===")
    print(f"    Path: {doc_folder.relative_to(CLEANED_DIR.parent.parent)}\n")

    for f in files:
        content = f.read_text(encoding="utf-8")
        words = content.split()
        print(f"[{f.name}]  {len(words):,} words  |  {f.stat().st_size:,} bytes")
        # Show first 200 characters as a content preview
        print(f"  Preview: {content[:200].strip()!r}")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_doc(sys.argv[1])
    else:
        test_all()
