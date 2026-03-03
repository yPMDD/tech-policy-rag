import json
from jsonschema import validate, ValidationError
from pathlib import Path

def validate_catalog(documents_json, schema_json):
    """
    Validates that the generated documents.json registry perfectly 
    matches the constraints defined in documents.schema.json.
    """
    # Load the document registry (the file we just created)
    with open(documents_json, 'r') as f:
        data = json.load(f)
        
    # Load the formal JSON Schema definition
    with open(schema_json, 'r') as f:
        schema = json.load(f)
        
    try:
        # Perform the validation check
        validate(instance=data, schema=schema)
        print("Validation Successful: documents.json conforms to the schema.")
        return True
    except ValidationError as e:
        # If the data is missing a required field or has a bad format, show exactly where it failed
        print(f"Validation Failed: {e.message}")
        print(f"Failed at path: {'/'.join(str(v) for v in e.path)}")
        return False

if __name__ == "__main__":
    # Setup paths relative to project root
    PROJECT_ROOT = Path(__file__).parent.parent
    DOCUMENTS_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.json"
    SCHEMA_JSON = PROJECT_ROOT / "data" / "metadata" / "documents.schema.json"
    
    # Execute the validation
    validate_catalog(DOCUMENTS_JSON, SCHEMA_JSON)
