"""Test the full filter pipeline with examples from the issues."""

import sys
sys.path.insert(0, r'c:\Users\moham\Python\Sedrati\machineacs')

from filters.regex import regex_filters
from filters.whitespace import whitespace
from filters.grammar import grammar

test_cases = [
    ("Artifici     al intelligence is trans 2023-12-01 f !!! orming healthcare",
     "Artificial intelligence is transforming healthcare"),
    ("https://dirty-si !!! te.ai/data Machine learning models are evolving fast",
     "Machine learning models are evolving fast"),
    ("Ma <div class='noise'>HTML fragme !!! nt</div> chine learning models are ev http://example.com/ref/123 olving fast",
     "Machine learning models are evolving fast"),
]

for i, (dirty, expected) in enumerate(test_cases, 1):
    print(f"Test Case {i}")
    print("="*60)
    print(f"Dirty:    {dirty}")

    # Apply filters in order (regex -> whitespace -> grammar)
    step1 = regex_filters(dirty)
    step2 = whitespace(step1)
    step3 = grammar(step2)

    print(f"Clean:    {step3}")
    print(f"Expected: {expected}")
    match = "PASS" if step3 == expected else "FAIL"
    print(f"Result: {match}")
    print()
