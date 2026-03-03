import json
import yaml
import os
from pathlib import Path
from datetime import datetime

class CatalogBuilder:
    """
    Scans the downloaded files and maps them to the metadata registry (documents.json).
    Ensures that physical files and their source definitions stay in sync.
    """
    def __init__(self, project_root):
        # Store the base project directory for path resolution
        self.project_root = Path(project_root)
        self.sources_yaml = self.project_root / "data" / "sources" / "sources.yaml"
        self.documents_json = self.project_root / "data" / "metadata" / "documents.json"
        
    def build(self):
        # Load the source manifest (the list of what we WANTED to download)
        with open(self.sources_yaml, 'r') as f:
            config = yaml.safe_load(f)
            
        sources = config.get('sources', [])
        documents = []
        
        for source in sources:
            # Ignore documents that are not enabled
            if not source.get('enabled', True):
                continue
                
            doc_id = source['id']
            # Use the explicit 'category' field as the folder name — single source of truth
            category = source.get('category', source.get('authority', 'unknown').lower().replace(' ', '_'))
            fmt = source['format']
            filename = source.get('filename', f"{doc_id}.{fmt}")

            # Construct the relative path where we expect the file to be
            raw_path = f"data/raw/{category}/{filename}"
            
            # CRITICAL: Only include documents in the catalog if the physical file actually exists
            if not (self.project_root / raw_path).exists():
                print(f"Warning: {raw_path} does not exist. Skipping.")
                continue

            # Build a structured document object that adheres to documents.schema.json
            doc_entry = {
                "doc_id": doc_id,
                "title": source['name'],
                "category": category,  # Explicit logical category — single source of truth for folder names
                "jurisdiction": source.get('jurisdiction', []),
                "domain": source.get('domain', []), # Maps to the 'tags' or 'policy area'
                "doc_type": source['doc_type'],
                "authority": source['authority'],
                "publisher": source.get('publisher', ''),
                "language": source.get('language', 'en'),
                "source_url": source['url'],
                "format": fmt,
                "version": {
                    "label": "1.0", # Initial version label
                    "retrieved_at": datetime.now().isoformat(), # Timestamp of cataloging
                    "content_hash": None # Placeholder for future data integrity checks (MD5/SHA)
                },
                "ingestion": {
                    "extractor": None, # Will be updated when text extraction is performed
                    "ocr_used": False,
                    "warnings": []
                },
                "paths": {
                    "raw": raw_path, # Path to the original PDF/HTML
                    "extracted": None, # Future path for raw text
                    "cleaned": None # Future path for processed chunks
                }
            }
            documents.append(doc_entry)
            
        # Wrap everything in a top-level metadata object
        output = {
            "generated_at": datetime.now().isoformat(),
            "schema_version": 1,
            "documents": documents
        }
        
        # Save the registry to disk as JSON
        with open(self.documents_json, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Successfully updated {self.documents_json} with {len(documents)} entries.")

if __name__ == "__main__":
    # Resolve project root relative to this script
    PROJECT_ROOT = Path(__file__).parent.parent
    builder = CatalogBuilder(PROJECT_ROOT)
    builder.build()
