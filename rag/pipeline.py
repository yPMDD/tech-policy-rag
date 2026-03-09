"""
rag/pipeline.py - Orchestrates the full RAG flow.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from rag.scope_guard import ScopeGuard
from rag.retriever import Retriever
from rag.prompt_templates import SYSTEM_PROMPT, USER_TEMPLATE, format_context
from rag.generator import Generator
from rag.citation_engine import CitationEngine

class RAGPipeline:
    """
    The main assembly line for the Tech Policy RAG.
    """
    def __init__(self, model_name: str = "llama3"):
        self.guard = ScopeGuard()
        self.retriever = Retriever()
        self.generator = Generator(model_name=model_name)
        self.citation_engine = CitationEngine()

    def ask(self, query: str) -> dict:
        """
        The main query entry point.
        """
        # 1. Scope Guard Check
        in_scope, reason = self.guard.check_query(query)
        if not in_scope:
            return {
                "answer": f"I cannot assist with this request. {reason}",
                "sources": [],
                "status": "out_of_scope"
            }

        # 2. Retrieval
        hits = self.retriever.get_context(query, n_results=4)
        if not hits:
            return {
                "answer": "I couldn't find any relevant legal documents in my database to answer this question.",
                "sources": [],
                "status": "no_context"
            }

        # 3. Format Prompt
        context_str = format_context(hits)
        user_prompt = USER_TEMPLATE.format(context=context_str, query=query)
        
        # 4. Generate Answer
        answer = self.generator.generate(SYSTEM_PROMPT, user_prompt)
        
        # 5. Extract Citations
        citations = self.citation_engine.format_citations(hits)

        return {
            "answer": answer,
            "citations": citations,
            "retrieved_context": context_str,
            "sources": [h['id'] for h in hits],
            "status": "success"
        }

if __name__ == "__main__":
    # Final E2E Test
    rag = RAGPipeline()
    user_query = "What are the requirements for high-risk AI according to the AI Act?"
    print(f"\nQUERY: {user_query}")
    print("-" * 50)
    
    result = rag.ask(user_query)
    print(f"\nANSWER:\n{result['answer']}")
    print(f"\n{result['citations']}")
