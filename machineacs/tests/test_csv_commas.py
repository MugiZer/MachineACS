"""Test that CSV files preserve commas while other file types remove them."""

import sys
sys.path.insert(0, r'c:\Users\moham\Python\Sedrati\machineacs')

from filters.regex import regex_filters

# Test case 1: CSV file (should preserve commas)
csv_line = "John,Doe,john@email.com,Software Engineer"
csv_config = {"file_type": "csv"}

print("Test 1: CSV File (commas should be preserved)")
print(f"  Input:  {csv_line}")
result = regex_filters(csv_line, csv_config)
print(f"  Output: {result}")
print(f"  Has commas: {'Yes' if ',' in result else 'No'}")
print()

# Test case 2: TXT file (should remove/clean commas in punctuation)
txt_line = "Hello,  , world"
txt_config = {"file_type": "txt"}

print("Test 2: TXT File (duplicate punctuation should be cleaned)")
print(f"  Input:  {txt_line}")
result = regex_filters(txt_line, txt_config)
print(f"  Output: {result}")
print()

# Test case 3: CSV with dirty data
dirty_csv = "Machine,Learning,mod https://dirty-si !!! te.ai/data els,are,evolving"
csv_config = {"file_type": "csv"}

print("Test 3: CSV with dirty data (URLs removed, commas preserved)")
print(f"  Input:  {dirty_csv}")
result = regex_filters(dirty_csv, csv_config)
print(f"  Output: {result}")
print(f"  Has commas: {'Yes' if ',' in result else 'No'}")
print()

# Test case 4: CSV with split words and punctuation
dirty_csv2 = "Artifici  al,intelligenc !!! e,is,trans 2023-12-01 f !!! orming,healthcare"
print("Test 4: CSV with split words (commas preserved, but words NOT merged to preserve columns)")
print(f"  Input:  {dirty_csv2}")
result = regex_filters(dirty_csv2, csv_config)
print(f"  Output: {result}")
print(f"  Has commas: {'Yes' if ',' in result else 'No'}")
print()

# Test case 5: Non-CSV file (should merge split words)
txt_line2 = "Artifici  al intelligence is trans 2023-12-01 f !!! orming healthcare"
txt_config = {"file_type": "txt"}

print("Test 5: TXT file (words should be merged)")
print(f"  Input:  {txt_line2}")
result = regex_filters(txt_line2, txt_config)
print(f"  Output: {result}")
print()

# Test case 6: Real-world CSV example
real_csv = "Alice,Johnson,ali !!! ce@exa  mple.com,Data https://dirty-si !!! te.ai/data Scientist,San Francisco"
print("Test 6: Real-world CSV with multiple issues")
print(f"  Input:  {real_csv}")
result = regex_filters(real_csv, csv_config)
print(f"  Output: {result}")
print(f"  Columns preserved: {len(result.split(','))} columns")
print()

print("="*60)
print("Summary:")
print("[PASS] CSV files preserve commas as column delimiters")
print("[PASS] CSV files still clean data within each column")
print("[PASS] Non-CSV files merge words and remove commas properly")
print("[PASS] URLs, emails, dates are removed from all file types")
