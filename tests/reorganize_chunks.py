"""
Reorganizes the flat data/cleaned/en/ directory into a nested structure:
  data/cleaned/en/{category}/{doc_id}/chunk_NNN.txt

Run once with: python reorganize_chunks.py
"""
import shutil
from pathlib import Path

CLEANED_DIR = Path(__file__).parent.parent / "data" / "cleaned" / "en"

# Same category mapping used in processing/pipeline.py
def get_category(doc_id):
    if doc_id.startswith('edpb_'):
        return 'edpb'
    elif doc_id.startswith(('gdpr_', 'gdpr_info_')):
        return 'gdpr'
    elif doc_id.startswith(('eu_ai_act_', 'eu_ai_', 'nis2_')):
        return 'eu_ai_act'
    elif doc_id.startswith('ico_'):
        return 'ico'
    elif doc_id.startswith('ie_dpc_'):
        return 'irish_dpc'
    else:
        return 'other'

def reorganize():
    moved = 0
    files = list(CLEANED_DIR.glob("*_chunk_*.txt"))

    for f in files:
        # Parse: e.g. "edpb_01_2021_breach_examples_chunk_003.txt"
        # The last two parts are "chunk" and "NNN", everything before is doc_id
        parts = f.stem.rsplit("_chunk_", 1)
        if len(parts) != 2:
            print(f"Skipping unrecognized filename: {f.name}")
            continue

        doc_id = parts[0]
        chunk_num = parts[1]  # e.g. "003"
        category = get_category(doc_id)

        # Target: data/cleaned/en/{category}/{doc_id}/chunk_NNN.txt
        target_dir = CLEANED_DIR / category / doc_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"chunk_{chunk_num}.txt"

        shutil.move(str(f), str(target_path))
        moved += 1

    print(f"Reorganized {moved} chunk files into nested structure.")

if __name__ == "__main__":
    reorganize()
