"""
rag/citation_engine.py - Formats chunks into professional citations.
"""

from typing import List, Dict, Any

class CitationEngine:
    """
    Parses retrieved metadata to generate clean references.
    """
    def __init__(self):
        pass

    def format_citations(self, hits: List[Dict[str, Any]]) -> str:
        """
        Creates a list of unique sources retrieved for this query.
        """
        sources = set()
        for hit in hits:
            category = hit['metadata'].get('category', 'unknown').upper()
            doc_id = hit['id'].split('_')[0] # Usually the doc_id part before chunk index
            sources.add(f"{category} (Document: {doc_id})")
        
        if not sources:
            return "No specific sources used."
            
        header = "Evidence retrieved from:\n"
        source_list = "\n".join([f"- {s}" for s in sorted(list(sources))])
        return header + source_list

    def extract_article_refs(self, text: str) -> List[str]:
        """
        Heuristic to extract 'Article XY' mentions from generated text.
        (Future improvement: use NLP or RegEx)
        """
        import re
        pattern = r"Article\s+\d+[a-z]*"
        matches = re.findall(pattern, text, re.IGNORECASE)
        return sorted(list(set(matches)))
