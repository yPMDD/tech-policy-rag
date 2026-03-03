import os
from pathlib import Path
from ingestion.downloader import download_sources
from ingestion.catalog_builder import CatalogBuilder
from ingestion.validator import validate_catalog

def run_pipeline():
    """
    Orchestrates the entire document ingestion workflow from start to finish.
    """
    # Initialize project-wide paths
    PROJECT_ROOT = Path(__file__).parent.parent
    SOURCES_YAML = PROJECT_ROOT / "data" / "sources" / "sources.yaml"
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
    DOCUMENTS_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.json"
    SCHEMA_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.schema.json"
    
    # PHASE 1: Downloader
    # Goal: Fetch files from the internet and store them in data/raw/
    print("--- Phase 1: Downloading Documents ---")
    download_sources(SOURCES_YAML, RAW_DATA_DIR)
    
    # PHASE 2: Catalog Builder
    # Goal: Scan the data/raw folder and create a JSON registry of all documents found
    print("\n--- Phase 2: Building Document Catalog ---")
    builder = CatalogBuilder(PROJECT_ROOT)
    builder.build()
    
    # PHASE 3: Validator
    # Goal: Ensure the generated JSON registry is perfect and matches our data schema
    print("\n--- Phase 3: Validating Catalog ---")
    is_valid = validate_catalog(DOCUMENTS_JSON, SCHEMA_JSON)
    
    # Final Result
    if is_valid:
        print("\nIngestion Pipeline Completed Successfully!")
    else:
        print("\nIngestion Pipeline Completed with Validation Errors.")

if __name__ == "__main__":
    # Start the engine
    run_pipeline()
