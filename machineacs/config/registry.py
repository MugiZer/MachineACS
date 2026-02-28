from typing import Dict, Any, List, Tuple, Callable, Optional

from filters.whitespace import whitespace
from filters.grammar import grammar
from filters.regex import regex_filters
from filters.newlines import newlines

FilterFunc = Callable[[str], str]
FilterFuncWithConfig = Callable[[str, Dict[str, Any]], str]

FILTER_REGISTRY: Dict[str, Callable] = {
    "whitespace": whitespace,
    "grammar": grammar,
    "regex": regex_filters,
    "newlines": newlines,
}

_ACTIVE_FILTER_CACHE: Dict[int, Tuple[List[Tuple[str, Callable]], bool]] = {}


def apply_filters(line: str, config: Dict[str, Any]) -> str:
    """
    Apply enabled filters to a line of text.

    Args:
        line: The text line to process.
        config: Configuration dict with 'filters' key containing filter settings.

    Returns:
        The processed line after applying all enabled filters.
    """
    config_id = id(config)

    if config_id not in _ACTIVE_FILTER_CACHE:
        non_grammar: List[Tuple[str, Callable]] = []
        has_grammar = False

        filters_config = config.get("filters", {})
        for name, enabled in filters_config.items():
            if enabled and name in FILTER_REGISTRY:
                if name == "grammar":
                    has_grammar = True
                elif name != "newlines":
                    non_grammar.append((name, FILTER_REGISTRY[name]))

        _ACTIVE_FILTER_CACHE[config_id] = (non_grammar, has_grammar)

    non_grammar_filters, has_grammar = _ACTIVE_FILTER_CACHE[config_id]
    filters_config = config.get("filters", {})

    # Pass 1: Apply all non-grammar filters
    for name, fn in non_grammar_filters:
        if name == "regex":
            line = fn(line, config)
        else:
            line = fn(line)

    # Pass 2: Polish with regex and whitespace to clean up
    if filters_config.get("regex"):
        line = FILTER_REGISTRY["regex"](line, config)
    if filters_config.get("whitespace"):
        line = FILTER_REGISTRY["whitespace"](line)

    # Pass 3: Apply grammar last (needs clean input)
    if has_grammar and line.strip():
        line = FILTER_REGISTRY["grammar"](line)

    return line


def clear_cache() -> None:
    """Clear the filter cache, useful for testing."""
    _ACTIVE_FILTER_CACHE.clear()
