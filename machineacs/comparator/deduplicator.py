from metrics import levenshtein_tabulated
import json 
import argparse
import time 

parser = argparse.ArgumentParser(description="MachineACS CLI")

# Fixed: Changed dest to 'command' (singular) to match your if-statement
subparsers = parser.add_subparsers(dest="command")

# Fixed: Removed the underscore to match the variable above
dedupe_parser = subparsers.add_parser("dedupe")

# Fixed: Removed the space after the dashes
dedupe_parser.add_argument("--threshold", type=float, required=True)
dedupe_parser.add_argument("--file", required=True)

# This single line runs the CLI and dynamically builds your variables!
args = parser.parse_args()

if args.command == "dedupe":
    # Just assign them to variables here if you want to use them locally:
    file_path = args.file
    threshold = args.threshold
    
    print(f"Loaded: {file_path} at {threshold} stringency")
    # -> Next step: How will you load the JSONL file into memory?

    records = []

    start_time = time.time()

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    pairs = []
    deduplicates = []

    for i, record in enumerate(records):
        name = record["full_name"]
        pairs.append((i,name))

    del records 

    for i,name in pairs:

        for j in range(i+1, len(pairs)):
            
            ind,sec_name = pairs[j]

            max_len = max(len(name),len(sec_name))
            
            _, _, distance = levenshtein_tabulated(name,sec_name)
            
            try:
                deduplicate_score = 1 - (distance/max_len)
            except ZeroDivisionError:
                print("max_len is zero")
                continue 

            if deduplicate_score >= threshold:
                deduplicates.append((sec_name,name))

    del pairs 

    print(deduplicates)

    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")