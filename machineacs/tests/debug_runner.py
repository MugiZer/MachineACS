import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tests.test_filters import test_whitespace_filter, test_grammar_filter, test_regex_filters_urls, test_regex_filters_emails, test_regex_filters_punctuation
    from filters.grammar import grammar
    from filters.whitespace import whitespace
    print("Imports successful")
except Exception as e:
    print(f"Import failed: {e}")
    # If import fails, we might still want to proceed to see errors if it's a specific function missing
    # But usually it's fatal.
    sys.exit(1)

def run_tests():
    with open("debug_log.txt", "w", encoding="utf-8") as f:
        def log(msg):
            print(msg)
            f.write(msg + "\n")
        
        log("Running whitespace tests...")
        try:
            test_whitespace_filter("  hello   world  ", "hello world")
            log("Whitespace: OK")
        except AssertionError as e:
            log(f"Whitespace FAILED: {e}")
            res = whitespace("  hello   world  ")
            log(f"  Got: '{res}'")
        except Exception as e:
            log(f"Whitespace CRASH: {e}")

        log("Running grammar tests...")
        try:
            # "helo world", "hello world"
            test_grammar_filter("helo world", "hello world")
            log("Grammar: OK")
        except AssertionError as e:
            log(f"Grammar FAILED: {e}")
            res = grammar("helo world")
            log(f"  Got: '{res}'")
            log("  Expected: 'hello world'")
        except Exception as e:
            log(f"Grammar CRASH: {e}")

        log("Running regex tests...")
        try:
            test_regex_filters_urls()
            log("Regex URLs: OK")
        except Exception as e:
            log(f"Regex URLs FAILED: {e}")
            
        try:
            test_regex_filters_emails()
            log("Regex Emails: OK")
        except Exception as e:
            log(f"Regex Emails FAILED: {e}")
            
        try:
            test_regex_filters_punctuation()
            log("Regex Punctuation: OK")
        except Exception as e:
            log(f"Regex Punctuation FAILED: {e}")

if __name__ == "__main__":
    run_tests()
