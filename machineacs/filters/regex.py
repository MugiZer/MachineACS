import re
from typing import Dict, Any, Optional, Pattern, List

# URL pattern that handles embedded junk
URL_WITH_JUNK = re.compile(
    r"https?://"
    r"(?:www\.)?"
    r"[\w\s.!?,'\":-]+"
    r"\.(?:com|edu|ai|ca|us|org|net|io|gov)"
    r"(?:/[\w\s.!?,'\":/\-]*)?"
)

# Email patterns
CONTACT_EMAIL = re.compile(
    r"contact\s+me\s+at\s+[\w\s.!?,'\":-]+@[\w\s.!?,'\":-]+\.(?:com|edu|ai|ca|us|org|net|io)\b"
)
EMAIL_WITH_JUNK = re.compile(
    r"[\w.!?,'\":-]+@[\w\s.!?,'\":-]+\.(?:com|edu|ai|ca|us|org|net|io)\b"
)

# Date pattern
DATE_PATTERN = re.compile(r"(\d{4}|\d{2})-\d{2}-(\d{4}|\d{2})\b")

# HTML tags
HTML_PAIRED = re.compile(r"<[\s\w='\"!?,:;/-]+>.*?</[\s\w='\"!?,:;/-]+>")
HTML_SINGLE = re.compile(r"<[\s\w='\"!?,:;/-]+>")

# Punctuation cleanup patterns
MULTIPLE_PUNCTUATION = re.compile(r'([.,!?\'"-]\s*){2,}')
SHRAPNEL = re.compile(r"\s+([.,!?])\s+")
CLEAN_NON_ALPHANUM = re.compile(r"[^\w\s\d.,!?\'\" -]")
CLEAN_NON_ALPHANUM_CSV = re.compile(r"[^\w\s\d,!?\'\" -]")
SPLIT_WORD_PUNCT = re.compile(r'(\w)\s*[.,!?\'"-]+\s*([a-z])')
SPLIT_WORD_PUNCT_CSV = re.compile(r'(\w)\s*[.!?\'"-]+\s*([a-z])')
SPLIT_BY_SPACES = re.compile(r'([a-z])\s{2,}([a-z])')

# URL removal pattern
_URL_REMOVAL_PATTERN = re.compile(
    r"https?://"
    r"[^\s]*"
    r"(?:\s+[^\s]*)*?"
    r"\.(?:com|edu|ai|ca|us|org|net|io|gov)"
    r"(?:/[^\s]*)*"
    r"(?=\s+[a-zA-Z]|\s*$)"
)

# Patterns to apply in order
CLEANUP_PATTERNS: List[Pattern] = [
    CONTACT_EMAIL,
    EMAIL_WITH_JUNK,
    DATE_PATTERN,
    HTML_PAIRED,
    HTML_SINGLE,
]


def _remove_url_with_junk(line: str) -> str:
    """
    Remove URLs even if they have junk/punctuation injected.

    Args:
        line: The text line to process.

    Returns:
        The line with URLs removed.
    """
    return _URL_REMOVAL_PATTERN.sub(" ", line)


def regex_filters(line: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Apply regex-based filters to clean a line of text.

    Removes URLs, emails, HTML tags, dates, and normalizes punctuation.

    Args:
        line: The text line to process.
        config: Optional configuration dict. If it contains 'file_type': 'csv',
                comma-preserving patterns are used.

    Returns:
        The cleaned line.
    """
    file_type = config.get("file_type") if config else None
    is_csv = file_type == "csv"

    # Remove URLs with embedded junk
    line = _remove_url_with_junk(line)

    # Clean emails, HTML, dates
    for pattern in CLEANUP_PATTERNS:
        line = pattern.sub(" ", line)

    # Merge words split by punctuation
    if is_csv:
        line = SPLIT_WORD_PUNCT_CSV.sub(r'\1\2', line)
    else:
        line = SPLIT_WORD_PUNCT.sub(r'\1\2', line)

    # Deduplicate mixed punctuation
    if not is_csv:
        line = MULTIPLE_PUNCTUATION.sub(r'\1', line)

    # Remove illegal characters
    if is_csv:
        line = CLEAN_NON_ALPHANUM_CSV.sub("", line)
    else:
        line = CLEAN_NON_ALPHANUM.sub("", line)

    # Merge fragments separated by multiple spaces
    line = SPLIT_BY_SPACES.sub(r'\1\2', line)

    # Remove floating punctuation
    if not is_csv:
        line = SHRAPNEL.sub(r" \1", line)

    return line
