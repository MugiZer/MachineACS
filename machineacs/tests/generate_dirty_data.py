import json
import csv
import random
from pathlib import Path

# Base sentences to "dirty up"
CLEAN_SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial intelligence is transforming the world.",
    "Python is a versatile programming language.",
    "Machine learning models require clean data.",
    "Natural language processing is a field of AI.",
    "Data cleaning is a crucial step in the pipeline.",
    "Quality data leads to better performance.",
    "FastAPI makes building APIs easy and fast.",
    "Structured data facilitates efficient analysis.",
    "A clean dataset is a happy dataset."
]

DIRTY_CHUNKS = ["!!!", "???", " @@@ ", " ### ", "   ", "\n\n", "...", "---", "   ", " "]
TYPOS = {"the": "teh", "quick": "quik", "jumps": "jmps", "language": "langage", "models": "modles", "field": "feild"}

def dirty_up(text):
    # Add random whitespace
    if random.random() > 0.3:
        text = "  " * random.randint(1, 3) + text + "  " * random.randint(1, 3)
    
    # Randomly inject typos
    for clean, dirty in TYPOS.items():
        if random.random() > 0.8:
            text = text.replace(clean, dirty)
            
    # Randomly inject special character chunks
    if random.random() > 0.5:
        text += random.choice(DIRTY_CHUNKS)
        
    # Occasionally make it all caps or lowercase
    if random.random() > 0.9:
        text = text.upper()
    elif random.random() > 0.9:
        text = text.lower()
        
    return text

def generate_data(num_lines=1000):
    output_dir = Path("tests/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. TXT
    with open(output_dir / "dirty_data.txt", "w", encoding="utf-8") as f:
        for _ in range(num_lines):
            line = dirty_up(random.choice(CLEAN_SENTENCES))
            f.write(line + "\n")
            if random.random() > 0.8: # Add empty lines
                f.write("\n")

    # 2. JSONL
    with open(output_dir / "dirty_data.jsonl", "w", encoding="utf-8") as f:
        for i in range(num_lines):
            item = {
                "id": i,
                "text": dirty_up(random.choice(CLEAN_SENTENCES)),
                "metadata": {"source": "simulation", "dirty": True}
            }
            f.write(json.dumps(item) + "\n")

    # 3. CSV
    with open(output_dir / "dirty_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "content", "label"])
        for i in range(num_lines):
            writer.writerow([i, dirty_up(random.choice(CLEAN_SENTENCES)), "unlabeled"])

    # 4. JSON
    json_data = []
    for i in range(num_lines):
        json_data.append({
            "record_id": i,
            "data": dirty_up(random.choice(CLEAN_SENTENCES))
        })
    with open(output_dir / "dirty_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    print(f"Successfully generated 1000 lines/records for txt, jsonl, csv, and json in {output_dir}")

if __name__ == "__main__":
    generate_data()
