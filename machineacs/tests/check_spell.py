from spellchecker import SpellChecker

def main():
    try:
        spell = SpellChecker()
        word1 = "helo"
        word2 = "tesst"
        word3 = "wrold"
        corr1 = spell.correction(word1)
        corr2 = spell.correction(word2)
        corr3 = spell.correction(word3)
        print(f"Correction of '{word1}': '{corr1}'")
        print(f"Correction of '{word2}': '{corr2}'")
        print(f"Correction of '{word3}': '{corr3}'")
        
        # Check known words
        print(f"Correction of 'hello': '{spell.correction('hello')}'")
        
        # Check candidates
        print(f"Candidates for 'helo': {spell.candidates(word1)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
