import re

MULTI_SPACE = re.compile(r" {2,}")


def whitespace(line: str) -> str:
    """
    Normalize whitespace in a line of text.

    Strips leading/trailing whitespace and collapses multiple spaces into one.

    Args:
        line: The text line to process.

    Returns:
        The line with normalized whitespace.
    """
    line = line.strip()
    return MULTI_SPACE.sub(" ", line)
