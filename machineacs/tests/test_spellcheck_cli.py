import subprocess
import sys
from pathlib import Path

from spellcheck import build_suggestions, find_misspellings, load_dictionary


def test_find_misspellings_and_suggestions(tmp_path):
    dictionary_path = tmp_path / "dictionary.txt"
    dictionary_path.write_text("hello\nworld\ntest\nsample\n", encoding="utf-8")

    text_path = tmp_path / "input.txt"
    text_path.write_text("Helo world\nThis is a tesst sample.\n", encoding="utf-8")

    dictionary_words, dictionary_list = load_dictionary(dictionary_path)
    misspellings = find_misspellings(text_path, dictionary_words)

    assert [item["word"] for item in misspellings] == ["Helo", "This", "is", "a", "tesst"]
    assert misspellings[0]["line"] == 1
    assert misspellings[0]["column"] == 1
    assert build_suggestions("helo", dictionary_list, 2) == ["hello"]


def test_cli_reports_misspellings(tmp_path):
    dictionary_path = tmp_path / "dictionary.txt"
    dictionary_path.write_text(
        "hello\nworld\nthis\nis\na\ntest\nsample\n",
        encoding="utf-8",
    )

    text_path = tmp_path / "input.txt"
    text_path.write_text("Helo world\nThis is a tesst sample.\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(Path.cwd() / "spellcheck.py"),
            str(text_path),
            str(dictionary_path),
            "--suggestions",
            "1",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Misspelled words found: 2" in result.stdout
    assert "Helo at line 1, column 1: hello" in result.stdout
    assert "tesst at line 2, column 11: test" in result.stdout


def test_cli_handles_clean_text(tmp_path):
    dictionary_path = tmp_path / "dictionary.txt"
    dictionary_path.write_text("hello\nworld\n", encoding="utf-8")

    text_path = tmp_path / "input.txt"
    text_path.write_text("Hello world\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(Path.cwd() / "spellcheck.py"),
            str(text_path),
            str(dictionary_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "No misspellings found."
