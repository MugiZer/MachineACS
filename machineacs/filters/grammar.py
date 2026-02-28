import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from spellchecker import SpellChecker
except ImportError:
    SpellChecker = None

from utils.logger import logger

CACHE_FILE = Path(__file__).resolve().parent.parent / "logs" / "grammar_cache.json"
CORRECTION_CACHE: Dict[str, str] = {}
MAX_WORD_LENGTH = 20

_spell_checker: Optional[SpellChecker] = None


def _get_spell_checker() -> Optional[SpellChecker]:
    """Lazily initialize the spell checker."""
    global _spell_checker
    if _spell_checker is None and SpellChecker is not None:
        _spell_checker = SpellChecker()
    return _spell_checker


def load_cache() -> None:
    """Load the correction cache from disk."""
    global CORRECTION_CACHE
    if not CACHE_FILE.exists():
        return

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                CORRECTION_CACHE.update(data)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Failed to load grammar cache: {e}")


def save_cache() -> None:
    """Save the correction cache to disk."""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(CORRECTION_CACHE, f)
    except OSError as e:
        logger.warning(f"Failed to save grammar cache: {e}")


def is_real_word(word: str) -> bool:
    """
    Determine if a word is worth spell-checking.

    Args:
        word: The word to check.

    Returns:
        True if the word should be spell-checked.
    """
    if not word:
        return False
    if any(char.isdigit() for char in word):
        return False
    if len(word) > MAX_WORD_LENGTH:
        return False
    return True


def grammar(line: str) -> str:
    """
    Apply spell-checking correction to a line of text.

    Args:
        line: The text line to process.

    Returns:
        The line with spelling corrections applied.
    """
    spell_checker = _get_spell_checker()
    if spell_checker is None:
        return line

    raw_words = line.split()
    if not raw_words:
        return line

    word_map: List[Tuple[str, Optional[str], Optional[str]]] = []
    to_check: List[str] = []

    for w in raw_words:
        m = re.match(r"^(\W*)(.*?)(\W*)$", w)
        if m:
            prefix, core, suffix = m.groups()
            if core and is_real_word(core):
                word_map.append((prefix, core, suffix))
                if core not in CORRECTION_CACHE:
                    to_check.append(core)
            else:
                word_map.append((w, None, None))
        else:
            word_map.append((w, None, None))

    if to_check:
        unknowns = spell_checker.unknown(to_check)
        for core in to_check:
            if core in unknowns:
                corrected = spell_checker.correction(core)
                CORRECTION_CACHE[core] = corrected if corrected else core
            else:
                CORRECTION_CACHE[core] = core

    corrected_line: List[str] = []
    for prefix, core, suffix in word_map:
        if core is None:
            corrected_line.append(prefix)
        else:
            corrected_line.append(prefix + CORRECTION_CACHE[core] + suffix)

    return " ".join(corrected_line)


# Load cache on module import
load_cache()
