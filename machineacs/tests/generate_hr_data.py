import json
import random
import csv
import unicodedata
from pathlib import Path

# --- Realistic Data Pools ---
FIRST_NAMES = ["James", "Maria", "Robert", "Elena", "Michael", "Sofia", "David", "Anna", "William", "Isabella", "John", "Mia", "Thomas", "Chloe", "Daniel", "Zoé", "Matthew", "André", "Anthony", "Héctor", "Christopher", "Camila", "Joseph", "Lucia"]
LAST_NAMES = ["Smith", "Garcia", "Johnson", "Martinez", "Williams", "Rodriguez", "Brown", "Hernandez", "Jones", "Lopez", "Miller", "Gonzalez", "Davis", "Perez", "Martin", "Sanchez"]
JOB_TITLES = ["Software Engineer", "Data Analyst", "HR Manager", "Product Manager", "DevOps Engineer", "Frontend Developer", "Backend Engineer", "Marketing Director", "Sales Associate", "Customer Support Specialist"]
CITIES = ["Montreal", "Montréal", "Paris", "London", "Zurich", "Zürich", "Sao Paulo", "São Paulo", "New York", "Tokyo", "Berlin", "Sydney", "Toronto"]
DEPARTMENTS = ["Engineering", "Human Resources", "Finance", "Product", "Operations", "Marketing", "Sales", "Customer Service"]

def generate_base_employee(emp_id: int) -> dict:
    """Generate a clean, standard employee record."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    
    # 85% chance they are active
    is_active = random.random() < 0.85 
    
    return {
        "employee_id": emp_id,
        "full_name": f"{first} {last}",
        "age": random.randint(22, 65),
        "salary": round(random.uniform(50000, 150000), 2),
        "job_title": random.choice(JOB_TITLES),
        "city": random.choice(CITIES),
        "country": "Unknown", # Simplified for this script
        "email": f"{first.lower()}.{last.lower()}@company.com",
        "is_active": is_active,
        "department": random.choice(DEPARTMENTS)
    }

def dirtify_record(record: dict) -> dict:
    """Apply specific dirty variations to an employee record."""
    dirty = record.copy()
    
    # 1. Mixed Types
    if random.random() < 0.5:
        dirty["age"] = str(dirty["age"])
        
    if random.random() < 0.3:
        dirty["salary"] = str(dirty["salary"])
    elif random.random() < 0.2:
        # Float Noise (only if it remained a float)
        noise = random.choice([0.00000000000001, -0.00000000000002])
        dirty["salary"] = dirty["salary"] + noise
        
    if random.random() < 0.4:
        # Boolean to string variations
        dirty["is_active"] = random.choice(["true", "True", "1", "false", "False", "0"])
        # Fix logic so "true" actually means True, though Canonicalizer should handle both
        if dirty["is_active"] in ["false", "False", "0"] and record["is_active"]:
             dirty["is_active"] = random.choice(["true", "True", "1"])
        elif dirty["is_active"] in ["true", "True", "1"] and not record["is_active"]:
             dirty["is_active"] = random.choice(["false", "False", "0"])

    # 2. Unicode Variations (Decomposed NFD)
    # Apply to ~30% of records overall, but only if they have accents
    if random.random() < 0.3:
        for key in ["full_name", "city"]:
            val = dirty.get(key)
            if isinstance(val, str) and any(c in val for c in ["é", "á", "í", "ó", "ú", "ñ", "ü", "ã"]):
               dirty[key] = unicodedata.normalize('NFD', val)

    # 3. Nulls and Missing Fields
    if random.random() < 0.2:
        choice = random.choice(["null", "empty", "missing"])
        if choice == "null":
            dirty["city"] = None
        elif choice == "empty":
            dirty["city"] = ""
        else:
            dirty.pop("city", None)
            
    if random.random() < 0.15:
        choice = random.choice(["null", "empty", "missing"])
        if choice == "null":
            dirty["department"] = None
        elif choice == "empty":
            dirty["department"] = ""
        else:
            dirty.pop("department", None)

    # 4. Key Insertion Order Randomization
    # Rebuild dictionary with shuffled keys
    keys = list(dirty.keys())
    random.shuffle(keys)
    shuffled_dirty = {k: dirty[k] for k in keys}
    
    return shuffled_dirty

def main():
    num_unique = 170
    num_duplicates = 30
    total_records = num_unique + num_duplicates
    
    # Needs to be deterministic for the 30 pairs to actually match
    # However we want the dirtifying to be random so they look different
    
    # 1. Generate 170 clean base records
    base_records = [generate_base_employee(i + 1000) for i in range(num_unique)]
    
    # 2. Pick 30 records to be our "duplicate pairs"
    # We sample indices to duplicate
    duplicate_indices = random.sample(range(num_unique), num_duplicates)
    
    # 3. Create the final list by dirtifying all 170, plus dirtifying the 30 duplicates AGAIN
    final_records = []
    
    # Dirtify the main 170
    for record in base_records:
        final_records.append(dirtify_record(record))
        
    # Dirtify the 30 duplicates (creates a different dirty variation of the same base data)
    for idx in duplicate_indices:
        final_records.append(dirtify_record(base_records[idx]))
        
    # 4. Global Shuffle to space out the duplicates
    random.shuffle(final_records)
    
    # 5. Write Outputs
    output_dir = Path("machineacs/tests/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSONL
    jsonl_path = output_dir / "dirty_hr_data.jsonl"
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for record in final_records:
            # We DONT want json.dumps to sort_keys here, we want to preserve our shuffled insertion order
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
            
    # JSON
    json_path = output_dir / "dirty_hr_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        # standard json.dump doesn't easily preserve per-object key order if they differ in a list
        # but in Python 3.7+ dicts preserve order, and json.dump respects it if sort_keys=False
        json.dump(final_records, f, ensure_ascii=False, indent=2)

    # CSV
    csv_path = output_dir / "dirty_hr_data.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        # CSV needs a fixed header, so we collect all possible keys
        all_keys = ["employee_id", "full_name", "age", "salary", "job_title", "city", "country", "email", "is_active", "department"]
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for record in final_records:
            # Missing keys will be written as empty strings by DictWriter
            writer.writerow(record)

    # TXT 
    txt_path = output_dir / "dirty_hr_data.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        for record in final_records:
            # Simple pipe delimited format
            row = "|".join(str(record.get(k, "")) for k in all_keys)
            f.write(row + '\n')

    print(f"✅ Successfully written '{total_records}' records to '{output_dir.absolute()}'")
    print(f"✅ Included '{num_duplicates}' duplicate base records with different dirty variations.")
    print(f"Files generated: JSONL, JSON, CSV, TXT")

if __name__ == "__main__":
    main()
