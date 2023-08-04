from googletrans import Translator, constants
from pprint import pprint
import keywords
import csv
import os


translator = Translator()

# Translates individual keyword or variable/function name
# Initialize the translation memory
translation_memory = {}


def translate_word(word: str, lang: str, current_keywords) -> str:
    # Check if the translation memory for this language exists
    if lang not in translation_memory:
        translation_memory[lang] = {}

    # If the word has been translated before, use the saved translation
    if word in translation_memory[lang]:
        return translation_memory[lang][word]

    if lang == "es":
        dictionary = keywords.es
    elif lang == "fr":
        dictionary = keywords.fr
    else:
        dictionary = current_keywords

    if word in dictionary:
        translated_word = dictionary[word]
    else:
        words = word.split("_")
        translated_word = translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")

    # Save the translation in the translation memory
    translation_memory[lang][word] = translated_word

    return translated_word


def translate_line(line: str, lang: str, current_keywords, include_comments: bool = True) -> str:
    if not include_comments and line.lstrip().startswith("#"):
        return line

    words = []
    current_word = ""

    for char in line:
        if char.isalpha() or char == "_":
            current_word += char
        elif current_word == "":
            words.append(char)
        else:
            words.append(translate_word(current_word, lang, current_keywords))
            current_word = ""
            words.append(char)

    words.append(translate_word(current_word, lang, current_keywords))
    translated_line = "".join(words)
    return translated_line

# Example of how to format/dissect output from a translation
# print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
