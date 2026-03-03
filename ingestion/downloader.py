import os
import yaml
import requests
from pathlib import Path

def download_sources(sources_path, raw_dir):
    """
    Reads the sources.yaml file and downloads all enabled documents 
    into their respective authority-based subdirectories.
    """
    # Load the YAML configuration file
    with open(sources_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Get global defaults and the list of individual sources
    defaults = config.get('defaults', {})
    sources = config.get('sources', [])
    
    for source in sources:
        # Skip documents that have been marked as disabled in the YAML
        if not source.get('enabled', True):
            continue
            
        source_id = source['id']
        url = source['url']
        fmt = source['format']
        
        # Use the explicit 'filename' from YAML if it exists, otherwise generate one from ID
        filename = source.get('filename', f"{source_id}.{fmt}")
        
        # Determine the authority (e.g., EDPB, GDPR) to use as a subdirectory name
        # We lowercase it and replace spaces with underscores for clean folder names
        authority = source.get('authority', 'unknown').lower().replace(' ', '_')
        dest_dir = Path(raw_dir) / authority
        
        # Ensure the authority subdirectory exists; create it if it doesn't
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / filename
        
        # Skip the download if the file is already on disk (idempotency)
        if dest_path.exists():
            print(f"Skipping {source_id}, file already exists at {dest_path}")
            continue
            
        print(f"Downloading {source_id} from {url}...")
        try:
            # Fetch the document from the web with a 30-second safety timeout
            response = requests.get(url, timeout=30)
            response.raise_for_status() # Raise an error if the HTTP request failed
            
            # Write the binary content (PDF/HTML) to the destination path
            with open(dest_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded {source_id} to {dest_path}")
        except Exception as e:
            # Log any download errors (like 404s or network timeouts)
            print(f"Failed to download {source_id}: {e}")

if __name__ == "__main__":
    # Setup paths relative to this script's location
    PROJECT_ROOT = Path(__file__).parent.parent
    SOURCES_YAML = PROJECT_ROOT / "data" / "sources" / "sources.yaml"
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
    
    # Trigger the download process
    download_sources(SOURCES_YAML, RAW_DATA_DIR)
