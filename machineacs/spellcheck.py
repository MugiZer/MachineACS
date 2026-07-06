import argparse
import re
import sys
from difflib import get_close_matches
from pathlib import Path

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a text file against a dictionary.")
    parser.add_argument("text_file", help="Path to the text file to check.")
    parser.add_argument("dictionary_file", help="Path to the dictionary file.")
    parser.add_argument(
        "--suggestions",
        type=int,
        default=5,
        help="Number of suggestions to show for each misspelled word (default: 5).",
    )
    args = parser.parse_args()

    if args.suggestions < 0:
        parser.error("--suggestions must be 0 or greater")

    return args


def load_dictionary(dictionary_path: Path) -> tuple[set[str], list[str]]:
    words: list[str] = []
    seen: set[str] = set()

    with dictionary_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            word = raw_line.strip().lower()
            if word and word not in seen:
                seen.add(word)
                words.append(word)

    return seen, words


def find_misspellings(
    text_path: Path,
    dictionary_words: set[str],
) -> list[dict[str, object]]:
    misspellings: list[dict[str, object]] = []

    with text_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            for match in WORD_PATTERN.finditer(line):
                original_word = match.group(0)
                normalized_word = original_word.lower()

                if normalized_word in dictionary_words:
                    continue

                misspellings.append(
                    {
                        "word": original_word,
                        "normalized": normalized_word,
                        "line": line_number,
                        "column": match.start() + 1,
                    }
                )

    return misspellings


def build_suggestions(
    word: str,
    dictionary_list: list[str],
    limit: int,
) -> list[str]:
    if limit == 0:
        return []

    cutoff = 0.6 if len(word) > 4 else 0.5
    return get_close_matches(word.lower(), dictionary_list, n=limit, cutoff=cutoff)


def main() -> int:
    args = parse_args()
    text_path = Path(args.text_file)
    dictionary_path = Path(args.dictionary_file)

    if not text_path.is_file():
        print(f"Error: text file not found: {text_path}", file=sys.stderr)
        return 1

    if not dictionary_path.is_file():
        print(f"Error: dictionary file not found: {dictionary_path}", file=sys.stderr)
        return 1

    dictionary_words, dictionary_list = load_dictionary(dictionary_path)
    misspellings = find_misspellings(text_path, dictionary_words)

    if not misspellings:
        print("No misspellings found.")
        return 0

    print(f"Misspelled words found: {len(misspellings)}")
    for entry in misspellings:
        suggestions = build_suggestions(
            entry["normalized"],
            dictionary_list,
            args.suggestions,
        )
        suggestion_text = ", ".join(suggestions) if suggestions else "(no suggestions)"
        print(
            f"{entry['word']} at line {entry['line']}, column {entry['column']}: "
            f"{suggestion_text}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
