import json
from pathlib import Path
from processing.pdf_parser import extract_text_from_pdf
from processing.html_parser import extract_text_from_html
from processing.ocr_handler import extract_text_via_ocr
from processing.cleaner import clean_text
from processing.language_detector import is_english
from processing.segmenter import segment_text

def run_processing_pipeline():
    """
    Orchestrates the conversion of raw binary files (PDF/HTML) into 
    cleaned, segmented text chunks for the embedding layer.
    """
    PROJECT_ROOT = Path(__file__).parent.parent
    DOCUMENTS_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.json"
    
    # Load the document registry
    with open(DOCUMENTS_JSON, 'r') as f:
        registry = json.load(f)
        
    processed_count = 0
    
    for doc in registry.get('documents', []):
        doc_id = doc['doc_id']
        raw_path = PROJECT_ROOT / doc['paths']['raw']
        fmt = doc['format']
        category = doc['category']

        print(f"--- Processing {doc_id} ({fmt}) ---")
        
        # 1. PARSING: Extract text based on format
        raw_text = None
        if fmt == 'pdf':
            raw_text = extract_text_from_pdf(raw_path)
            # OCR Fallback if text extraction yielded nothing
            if not raw_text or len(raw_text.strip()) < 50:
                print(f"Text layer missing for {doc_id}, switching to OCR...")
                raw_text = extract_text_via_ocr(raw_path)
        elif fmt == 'html':
            raw_text = extract_text_from_html(raw_path)
            
        if not raw_text:
            print(f"Failed to extract text for {doc_id}. Skipping.")
            continue
            
        # 2. VALIDATION: Check language
        if not is_english(raw_text):
            print(f"Skipping {doc_id}, non-English content detected.")
            continue
            
        # 3. REFINEMENT: Clean text
        cleaned_text = clean_text(raw_text)
        
        # Save extracted raw text (Silver Layer) using the correct category subfolder
        extracted_dir = PROJECT_ROOT / "data" / "extracted" / category
        extracted_dir.mkdir(parents=True, exist_ok=True)
        extracted_file = extracted_dir / f"{doc_id}.txt"
        with open(extracted_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
            
        # 4. SEGMENTATION: Chunk the text (Gold Layer)
        # Write into nested structure: data/cleaned/en/{category}/{doc_id}/chunk_NNN.txt
        # This mirrors the structure of data/raw/ and data/extracted/ for full consistency.
        chunks = segment_text(cleaned_text)
        doc_cleaned_dir = PROJECT_ROOT / "data" / "cleaned" / "en" / category / doc_id
        doc_cleaned_dir.mkdir(parents=True, exist_ok=True)

        # Save each chunk as chunk_000.txt, chunk_001.txt, etc. inside the doc folder
        for idx, chunk in enumerate(chunks):
            chunk_file = doc_cleaned_dir / f"chunk_{idx:03d}.txt"
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk)

        # 5. REGISTRY UPDATE: Write the extracted/cleaned paths back into documents.json.
        #    This is done after every document so the registry is always accurate,
        #    even if the pipeline is interrupted mid-run.
        doc['paths']['extracted'] = str(extracted_file.relative_to(PROJECT_ROOT))
        # Point to the doc-specific chunk folder, not the generic cleaned/en/ root
        doc['paths']['cleaned'] = str(doc_cleaned_dir.relative_to(PROJECT_ROOT))
        doc['ingestion']['extractor'] = 'policylens-processing-v1'
        
        # Persist the updated registry to disk immediately after each document
        with open(DOCUMENTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2)
        
        processed_count += 1
        
    print(f"\nProcessing Completed: {processed_count} documents transformed into semantic chunks.")

if __name__ == "__main__":
    run_processing_pipeline()
