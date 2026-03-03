from bs4 import BeautifulSoup
from pathlib import Path

def extract_text_from_html(html_path):
    """
    Extracts cleaned legal text from an HTML file using BeautifulSoup4.
    Targets main content areas and strips navigation/UI elements.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
            script_or_style.decompose()

        # Target specific content containers if known (e.g., gdpr-info.eu uses specific classes)
        # For now, we extract all text but focus on structured paragraphs
        text = soup.get_text(separator='\n')
        
        # Basic cleanup of extra whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error parsing HTML {html_path}: {e}")
        return None

if __name__ == "__main__":
    # Example usage for testing
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        content = extract_text_from_html(path)
        if content:
            print(content[:500] + "...")
