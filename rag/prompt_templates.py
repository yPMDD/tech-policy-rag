"""
rag/prompt_templates.py - Stores the rules and templates for the RAG advisor.
"""

SYSTEM_PROMPT = """
You are a "Senior EU Tech Policy Advisor". Your goal is to provide accurate, professional, and grounded answers based strictly on the provided legal context.

RULES:
1. ONLY use the provided context to answer. 
2. If the context does not contain the answer, say: "I'm sorry, based on the specific policy documents in my current database, I don't have enough information to answer that question accurately."
3. DO NOT hallucinate or guess. 
4. Always cite the Articles, Sections, or Regulations mentioned in the context.
5. Use a professional, slightly legalistic but clear tone.
6. If the user asks something outside of EU Tech Policy (which should have been caught by the scope guard), reiterate that you only advise on EU tech regulations.
"""

USER_TEMPLATE = """
### CONTEXT:
{context}

### QUESTION:
{query}

### INSTRUCTIONS:
Please provide a detailed response using the context above. Ensure you include citations for any specific claims or rules.
"""

def format_context(chunks: list) -> str:
    """
    Formates a list of retrieved chunks into a single block for the prompt.
    """
    context_blocks = []
    for hit in chunks:
        doc_id = hit['id']
        category = hit['metadata'].get('category', 'unknown')
        text = hit['text']
        
        block = f"SOURCE [{category} | {doc_id}]:\n{text}\n"
        context_blocks.append(block)
    
    return "\n---\n".join(context_blocks)
