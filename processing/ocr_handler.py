import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

def extract_text_via_ocr(pdf_path):
    """
    Fallback OCR logic for PDFs that lack a text layer (scanned images).
    Converts PDF pages to images and then uses Tesseract OCR to extract text.
    Note: Requires 'tesseract' and 'poppler' to be installed on the system.
    """
    try:
        print(f"Starting OCR for {pdf_path} (this may take a while)...")
        # Convert PDF pages to a list of PIL Image objects
        images = convert_from_path(pdf_path)
        
        full_text = ""
        for i, image in enumerate(images):
            # Extract text from each page image
            page_text = pytesseract.image_to_string(image)
            full_text += f"\n--- OCR PAGE {i + 1} ---\n"
            full_text += page_text
            
        return full_text.strip()
    except Exception as e:
        print(f"OCR Error for {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    # Example usage for testing
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        content = extract_text_via_ocr(path)
        if content:
            print(content[:500] + "...")
