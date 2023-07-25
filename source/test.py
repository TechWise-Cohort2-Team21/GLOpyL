from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

#Translates individual keyword or variable/function name
def translate_word(word: str, lang: str, keywords: dict) -> str:
    if word in keywords:
        return keywords[word]
    # if programming_language == "python":
    #     words = word.split("_")
    #     return translator.translate(" ".join(words), dest=translated_language).text.replace(" ", "_")
    words = word.split("_")
    return translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")


#Translates a line, ignoring all nonalphabetical characters
def translate_line(line: str, lang: str, keywords: dict, include_comments: bool = True) -> str:
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
            words.append(translate_word(current_word, lang, keywords))
            current_word = ""
            words.append(char)

    words.append(translate_word(current_word, lang, keywords))
    translated_line = "".join(words)
    return translated_line

#Example of how to format/dissect output from a translation
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")