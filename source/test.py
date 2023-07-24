from googletrans import Translator, constants
from pprint import pprint


#Keyword Dictionary: attempts to store correct keyword file in a dictionary
def make_keyword_dictionary(translated_language: str) -> dict:
    keyword_file_path = f"keywords_en2{translated_language}.txt"
    try:
        with open(keyword_file_path, "r") as keyword_file:
            keywords = {}
            for line in keyword_file:
                old, trans = line.strip().split(" ")
                keywords[old] = trans
            return keywords
    except FileNotFoundError:
        print(f"Keyword file '{keyword_file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error occurred while reading the keyword file: {str(e)}")
        exit(1)


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


#Setup: select languages and create translator object
#programming_language = "python"
translated_language = "es"
translator = Translator()
keywords = make_keyword_dictionary(translated_language)

#Applies translate functions to input file
input = open("input.txt", "r")
with open("output.rtf", "w") as output:
    for line in input:
        translation = translate_line(line, translated_language, keywords)
        output.write(translation)
input.close()
output.close()
# meow


#Example of how to format/dissect output from a translation
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")