import pytest
from pathlib import Path
import shutil
import tempfile
import sys

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_config():
    return {
        "filters": {
            "whitespace": True,
            "grammar": True,
            "regex": True,
            "newlines": True
        },
        "regex_patterns": [
            {"pattern": "bad_word", "replacement": "****"}
        ]
    }

@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace with data directory structure."""
    temp_dir = tempfile.mkdtemp()
    data_dir = Path(temp_dir) / "data"
    data_dir.mkdir()
    
    yield Path(temp_dir)
    
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_file(temp_workspace):
    """Creates a sample text file to clean."""
    file_path = temp_workspace / "data" / "test_file.txt"
    content = "Hello  world! This is a   test file."
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path
