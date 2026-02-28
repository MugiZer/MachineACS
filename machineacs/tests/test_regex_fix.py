"""Quick test to verify the regex fixes work correctly."""

import sys
sys.path.insert(0, r'c:\Users\moham\Python\Sedrati\machineacs')

from filters.regex import regex_filters

# Test case 1: Original issue
test_line = "Artifici     al intelligence is trans 2023-12-01 f !!! orming healthcare"
print("Test 1 - Original dirty line:")
print(f"  {test_line}")
result = regex_filters(test_line)
print("After regex_filters:")
print(f"  {result}")
print()

# Test case 2: URL with punctuation inside
test_line2 = "https://dirty-si !!! te.ai/data Machine learning models are evolving fast"
print("Test 2 - URL with embedded punctuation:")
print(f"  {test_line2}")
result2 = regex_filters(test_line2)
print("After regex_filters:")
print(f"  {result2}")
print()

# More test cases
test_cases = [
    "Ma <div class='noise'>HTML fragme !!! nt</div> chine learning models are ev http://example.com/ref/123 olving fast",
    "contact me at user@provider.ai for more info",
    "The st ?? ock market saw record highs today",
    "f !!! orming",
    "trans 2023-12-01 f !!! orming",
    "<span>extra tags</span> some text",
    "text <div class='noise'>HTML fragment</div> more text",
    "info@web-data.com",
    "The hist contact me at user@provider.ai ory of ancient civilizaton is fascinatng",
]

print("Additional test cases:")
for i, line in enumerate(test_cases, 1):
    result = regex_filters(line)
    print(f"{i}. Input:  {line}")
    print(f"   Output: {result}")
    print()
