import re
import unicodedata

def clean_text(text):
    """
    Normalizes extracted text to remove boilerplate, fix whitespace, 
    and standardize encoding issues.
    """
    if not text:
        return ""
        
    # 1. Normalize unicode characters (e.g., fix ligatures like 'fi' or 'fl')
    text = unicodedata.normalize('NFKC', text)
    
    # 2. Remove common PDF/HTML boilerplate noise
    # Remove strings like "Page X of Y" or solitary page numbers
    text = re.sub(r'(?i)Page \d+ of \d+', '', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # 3. Standardize whitespacing
    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace more than two newlines with exactly two (preserving paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 4. Strip leading/trailing whitespace from the whole document
    return text.strip()

if __name__ == "__main__":
    # Example usage
    sample = "This is a   test.\n\n\nPage 1 of 5\n\n\nNormalized text content."
    print("Before:\n", sample)
    print("\nAfter:\n", clean_text(sample))
