"""
rag/scope_guard.py - Detects if a query is within the legal tech policy scope.
"""

from typing import Tuple

# Keywords that define our core scope
IN_SCOPE_KEYWORDS = {
    "gdpr", "privacy", "data protection", "ai act", "artificial intelligence",
    "nis2", "cybersecurity", "cookie", "consent", "breach", "controller",
    "processor", "dpa", "edpb", "digital services act", "dsa", "digital markets act", "dma",
    "compliance", "regulation", "eu law", "policy", "tech", "digital", "ico", "dpc"
}

# Keywords that are strictly out of scope
OUT_OF_SCOPE_KEYWORDS = {
    "recipe", "cooking", "weather", "sport", "football", "movie", "music",
    "travel", "hotel", "restaurant", "joke", "story", "code", "python", "javascript"
}

class ScopeGuard:
    """
    Checks if a user query is relevant to EU Tech Policy.
    """
    def __init__(self, strictness: float = 0.5):
        self.strictness = strictness

    def check_query(self, query: str) -> Tuple[bool, str]:
        """
        Returns (is_in_scope, reason_if_out).
        """
        query_lower = query.lower()
        
        # 1. Check for explicit out-of-scope keywords
        for word in OUT_OF_SCOPE_KEYWORDS:
            if word in query_lower:
                return False, f"The query seems to be about '{word}', which is outside the scope of EU Tech Policy."

        # 2. Check if at least some in-scope keywords are present
        # (This is a naive check, but good for a base version)
        words = query_lower.split()
        in_scope_count = sum(1 for word in words if word in IN_SCOPE_KEYWORDS or any(kw in word for kw in IN_SCOPE_KEYWORDS))
        
        # If the query is very short and has no keywords, it might be out of scope or too vague
        if len(words) < 3 and in_scope_count == 0:
             return False, "The query is too short or vague to be identified as an EU Tech Policy question."

        # 3. Final heuristic: If no keywords at all are found in a longer query
        if in_scope_count == 0:
            # We are permissive here to allow natural language questions, 
            # but we can increase strictness later with an LLM-based check.
            pass

        return True, ""

if __name__ == "__main__":
    guard = ScopeGuard()
    test_queries = [
        "What are the data breach rules in GDPR?",
        "Tell me a recipe for pancakes",
        "How is AI defined?",
        "What is the weather in Paris?"
    ]
    
    for q in test_queries:
        in_scope, reason = guard.check_query(q)
        print(f"QUERY: {q} | IN SCOPE: {in_scope} | REASON: {reason}")
