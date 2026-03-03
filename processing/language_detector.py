from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for reproducible language detection results
DetectorFactory.seed = 0

def is_english(text):
    """
    Detects if the provided text is primarily in English.
    Returns True if detected as 'en', False otherwise.
    """
    if not text or len(text.strip()) < 20:
        # Not enough text to accurately detect language
        return True 
        
    try:
        lang = detect(text)
        return lang == 'en'
    except LangDetectException:
        return False

if __name__ == "__main__":
    # Example usage
    tests = [
        "This is a sample sentence in English.",
        "Ceci est une phrase en français.",
        "Dies ist ein Satz auf Deutsch."
    ]
    for t in tests:
        print(f"'{t}' -> Is English? {is_english(t)}")
