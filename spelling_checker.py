from spellchecker import SpellChecker
from autocorrect import Speller

def spell_model_activate(lng):
    if lng=="it" or lng=="en":
        spell=Speller(lang=lng)
    elif lng=="de" or lng=="fr":
        spell=SpellChecker(language=lng)
    return spell

def check_spell_en_fr_de(sentence,spell):
    #lang= input("Enter the language")
    #sentence=input("Enter the sentence")
    senten=""
    for word in sentence.split():
        misspelled= spell.unknown([word])
        if(misspelled):
            for ch in misspelled:
                word= spell.correction(ch)
        senten= senten+word+" "
    return senten

def spell_check_italian(sentence,spell):
    #sentence=input("Enter the sentence")
    senten=""
    for word in sentence.split():
        word= spell(word)
        senten= senten+word+" "
    return senten