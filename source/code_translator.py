from googletrans import Translator, constants
from pprint import pprint
import keywords

translator = Translator()

# Translates individual keyword or variable/function name
def translate_word(word: str, lang: str, current_keywords) -> str:
    if lang == "es":
        dictionary = keywords.es
    elif lang == "fr":
        dictionary = keywords.fr
    else:
        dictionary = current_keywords

    if word in dictionary:
        return dictionary[word]
    words = word.split("_")
    return translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")

def translate_line(line: str, lang: str, current_keywords, include_comments: bool = True) -> str:
    if not include_comments and line.startswith("#"):
        return ""

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
