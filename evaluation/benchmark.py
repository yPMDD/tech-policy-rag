import json
import os
import time
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from rag.pipeline import RAGPipeline
from evaluation.metrics import calculate_token_overlap, verify_citation, calculate_faithfulness

def run_benchmark():
    print("Starting RAG Benchmark...")
    
    # Initialize RAG
    rag = RAGPipeline()
    
    # Load dataset
    dataset_path = "evaluation/datasets/eu_policy_qa.json"
    with open(dataset_path, "r") as f:
        questions = json.load(f)
        
    results = []
    
    for item in questions:
        print(f"Evaluating: {item['question'][:50]}...")
        
        start_time = time.time()
        # Query the RAG engine
        response = rag.ask(item['question'])
        end_time = time.time()
        
        # Extract context from the new field in Pipeline
        context = response.get('retrieved_context', "")
        
        # Calculate metrics
        overlap_score = calculate_token_overlap(response['answer'], item['expected_answer'])
        citation_score = verify_citation(str(response['citations']), item['context_reference'])
        faithfulness_score = calculate_faithfulness(response['answer'], context)
        
        results.append({
            "id": item["id"],
            "question": item["question"],
            "expected_answer": item["expected_answer"],
            "actual_answer": response["answer"],
            "metrics": {
                "token_overlap": round(overlap_score, 3),
                "citation_accuracy": citation_score,
                "faithfulness": round(faithfulness_score, 3),
                "latency_sec": round(end_time - start_time, 2)
            }
        })
        
    # Calculate averages
    avg_overlap = sum(r['metrics']['token_overlap'] for r in results) / len(results)
    avg_citation = sum(r['metrics']['citation_accuracy'] for r in results) / len(results)
    avg_faithfulness = sum(r['metrics']['faithfulness'] for r in results) / len(results)
    avg_latency = sum(r['metrics']['latency_sec'] for r in results) / len(results)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_questions": len(results),
            "avg_token_overlap": round(avg_overlap, 3),
            "avg_citation_accuracy": round(avg_citation, 3),
            "avg_faithfulness": round(avg_faithfulness, 3),
            "avg_latency": round(avg_latency, 2)
        },
        "detailed_results": results
    }
    
    # Ensure reports directory exists
    reports_dir = PROJECT_ROOT / "evaluation" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Save report
    report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path = reports_dir / report_name
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Benchmark complete! Report saved to: {report_path}")
    print(f"Summary: Overlap: {avg_overlap:.2f} | Citation: {avg_citation:.2f} | Faithfulness: {avg_faithfulness:.2f}")

if __name__ == "__main__":
    run_benchmark()
