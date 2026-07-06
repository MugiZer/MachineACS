import argparse
import json
from pathlib import Path

def get_inputs(file_choices):
    
    # 1. SETUP: Load the JSON first so we know what the filter choices are
    BASE_DIR = Path(__file__).resolve().parent.parent 
    CONFIG_PATH = BASE_DIR / "config" / "settings.json"

    with CONFIG_PATH.open() as f:
        full_config = json.load(f)

    # 2. CREATE MASTER PARSER: One parser for everything
    parser = argparse.ArgumentParser(description="get all user inputs")

    # Flag for Files (-f)
    parser.add_argument(
        "-f", "--files", 
        choices=file_choices, 
        nargs="+", 
        required=True
    )

    # Flag for Settings (-s)
    parser.add_argument(
        "-s", "--settings", 
        choices=full_config["filters"].keys(), 
        nargs="+", 
        required=True
    )

    # 3. PARSE ONCE: This is the only time we call this in the whole app
    args = parser.parse_args()

    # 4. REBUILD CONFIG: Apply the user's choices to the JSON data
    full_config["filters"] = {
        name: enabled 
        for name, enabled in full_config["filters"].items()
        if enabled and name in args.settings 
    }

    # Return both the files to process and the updated config
    return args.files, full_config