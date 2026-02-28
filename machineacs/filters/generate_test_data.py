import json
import random
import os
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Realistic entities and noise
TOPICS = [
    "Machine learning models are evolving fast",
    "Global climate change is a critical issue",
    "The stock market saw record highs today",
    "Artificial intelligence is transforming healthcare",
    "Exploring the depths of the ocean reveals mystery",
    "Sustainable energy is the future of transport",
    "The history of ancient civilizations is fascinatng"
]

NOISE = [
    "   ", # extra spaces
    "...", # double punctuation
    "!!!",
    "??",
    "http://example.com/ref/123", # URLs
    "https://dirty-site.ai/data",
    "contact me at user@provider.ai", # Emails
    "info@web-data.com",
    "2023-12-01", # Dates
    "12-31-2024",
    "<div class='noise'>HTML fragment</div>", # HTML
    "<span>extra tags</span>"
]

TYPOS = {
    "evolving": "evolvin",
    "evolvin": "evolvine",
    "critical": "critcal",
    "record": "reccord",
    "healthcare": "health-care",
    "depths": "dephts",
    "ocean": "occean",
    "sustainable": "sustainible",
    "ancient": "ancent",
    "civilizations": "civilizaton"
}

def generate_messy_text():
    text = random.choice(TOPICS)
    
    # Randomly inject typos
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() in TYPOS and random.random() < 0.3:
            words[i] = TYPOS[word.lower()]
    text = " ".join(words)
    
    # Inject random noise
    num_noise = random.randint(1, 3)
    for _ in range(num_noise):
        noise_item = random.choice(NOISE)
        pos = random.randint(0, len(text))
        text = text[:pos] + " " + noise_item + " " + text[pos:]
        
    return text

def create_txt(count=10000):
    path = DATA_DIR / "trainingdata.txt"
    with open(path, "w", encoding="utf-8") as f:
        for i in range(count):
            line = generate_messy_text()
            f.write(f"{line}\n")
            # Introduce massive newline blocks randomly
            if random.random() < 0.05:
                f.write("\n" * random.randint(3, 6))
    print(f"Created {path}")

def create_json(count=10000):
    path = DATA_DIR / "data.json"
    data = []
    for i in range(count):
        data.append({
            "id": i,
            "text": generate_messy_text(),
            "meta": {
                "source": "web_scrape",
                "score": random.random(),
                "messy_tag": "   extra_space   "
            }
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Created {path}")

def create_jsonl(count=10000):
    path = DATA_DIR / "data.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for i in range(count):
            line = {
                "id": i,
                "content": generate_messy_text(),
                "status": "raw"
            }
            f.write(json.dumps(line) + "\n")
    print(f"Created {path}")

def create_csv(count=10000):
    path = DATA_DIR / "data.csv"
    import csv
    with open(path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "label"])
        for i in range(count):
            writer.writerow([
                i, 
                "2024-01-01", 
                generate_messy_text(), 
                "training"
            ])
    print(f"Created {path}")

if __name__ == "__main__":
    create_txt()
    create_json()
    create_jsonl()
    create_csv()
