import re
from typing import List, Dict

def calculate_exact_match(prediction: str, reference: str) -> float:
    """Simple exact match after basic normalization."""
    p = prediction.strip().lower()
    r = reference.strip().lower()
    return 1.0 if p == r else 0.0

def calculate_token_overlap(prediction: str, reference: str) -> float:
    """Calculate F1 score based on token overlap."""
    p_tokens = set(re.findall(r'\w+', prediction.lower()))
    r_tokens = set(re.findall(r'\w+', reference.lower()))
    
    if not p_tokens or not r_tokens:
        return 0.0
        
    common = p_tokens.intersection(r_tokens)
    precision = len(common) / len(p_tokens)
    recall = len(common) / len(r_tokens)
    
    if precision + recall == 0:
        return 0.0
        
    return 2 * (precision * recall) / (precision + recall)

def verify_citation(response_citations: str, expected_reference: str) -> float:
    """Check if the expected legal reference appears in the response citations."""
    if not response_citations:
        return 0.0
    
    # Normalize for search
    ref_norm = expected_reference.lower().replace("article", "art").strip()
    cit_norm = response_citations.lower().replace("article", "art").strip()
    
    if expected_reference.lower() in response_citations.lower() or ref_norm in cit_norm:
        return 1.0
    return 0.0

def calculate_faithfulness(answer: str, context: str) -> float:
    """
    Placeholder for LLM-as-a-judge faithfulness.
    In a real scenario, this would call an LLM to verify if 'answer' is supported by 'context'.
    For now, we use a simple heuristic: word overlap between answer and context.
    """
    a_tokens = set(re.findall(r'\w+', answer.lower()))
    c_tokens = set(re.findall(r'\w+', context.lower()))
    
    if not a_tokens:
        return 0.0
        
    # How many words in the answer are NOT in the context? (Simple hallucination check)
    # Note: This is very primitive compared to an LLM judge.
    common = a_tokens.intersection(c_tokens)
    overlap_ratio = len(common) / len(a_tokens)
    
    return overlap_ratio
