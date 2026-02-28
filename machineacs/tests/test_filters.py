import pytest
from filters.whitespace import whitespace
from filters.regex import regex_filters
from filters.grammar import grammar

@pytest.mark.parametrize("input_text, expected", [
    ("  hello   world  ", "hello world"),
    ("test  string", "test string"), 
    ("   ", "")
])
def test_whitespace_filter(input_text, expected):
    assert whitespace(input_text) == expected

@pytest.mark.parametrize("input_text, expected", [
    ("wrold", "world"),
    ("tesst", "test"),
    ("correct word", "correct word")
])
def test_grammar_filter(input_text, expected):
    # Tests that the grammar filter corrects misspelled words
    assert grammar(input_text) == expected 


def test_regex_filters_punctuation():
    input_text = "Hello!!! world..."
    expected = "Hello! world."
    assert regex_filters(input_text).strip() == expected

def test_regex_filters_urls():
    input_text = "Check this https://www.example.com site"
    expected = "Check this  site"
    assert regex_filters(input_text).strip() == expected

def test_regex_filters_emails():
    input_text = "Contact user@example.com for info"
    expected = "Contact  for info"
    assert regex_filters(input_text).strip() == expected

def test_regex_filters_html():
    input_text = "<div class='test'>Content</div>"
    expected = "Content"
    assert regex_filters(input_text).strip() == expected

def test_regex_filters_quotes():
    # Test that single and double quotes are kept
    assert regex_filters("It's \"great\"").strip() == "It's \"great\""
    
    # Test that consecutive quotes are collapsed
    assert regex_filters('Double "" quotes').strip() == 'Double " quotes'
    assert regex_filters("Triple ''' quotes").strip() == "Triple ' quotes"
