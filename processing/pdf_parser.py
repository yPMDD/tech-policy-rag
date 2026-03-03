import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF file using PyMuPDF (fitz).
    Handles page-by-page extraction and basic text cleanup.
    """
    text = ""
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Iterate through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # 'text' flag extracts the raw text layer
            page_text = page.get_text("text")
            
            # Simple page break marker for later segmentation
            text += f"\n--- PAGE {page_num + 1} ---\n"
            text += page_text
            
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    # Example usage for testing
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        content = extract_text_from_pdf(path)
        if content:
            print(content[:500] + "...")
