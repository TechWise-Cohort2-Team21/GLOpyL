from googletrans import Translator, constants
from pprint import pprint


#Setup: select languages and create translator object
translated_language = "es"
programming_language = "python"
translator = Translator()


#Example of how to format/dissect output from a translation
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")


#Keyword Dictionary: attempts to store correct keyword file in a dictionary
keyword_file_path = f"keywords_en2{translated_language}.txt"
try:
    with open(keyword_file_path, "r") as keyword_file:
        keywords = {}
        for line in keyword_file:
            old, trans = line.strip().split(" ")
            keywords[old] = trans
except FileNotFoundError:
    print(f"Keyword file '{keyword_file_path}' not found.")
    exit(1)
except Exception as e:
    print(f"Error occurred while reading the keyword file: {str(e)}")
    exit(1)


#Translates individual keyword or variable/function name
def translate_word(word: str) -> str:
    if word in keywords:
        return keywords[word]
    if programming_language == "python":
        words = word.split("_")
        return translator.translate(" ".join(words), dest=translated_language).text.replace(" ", "_")


#Translates a line, ignoring all nonalphabetical characters
def translate_line(line: str) -> str:
    words = []
    current_word = ""

    for char in line:
        if char.isalpha() or char == "_":
            current_word += char
        elif current_word == "":
            words.append(char)
        else:
            words.append(translate_word(current_word))
            current_word = ""
            words.append(char)

    words.append(translate_word(current_word))
    return "".join(words)


#Applies translate functions to input file and also handles any errors that may appear
input_file_path = "input.txt"
output_file_path = "output.txt"

try:
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        for line in input_file:
            translation = translate_line(line)
            output_file.write(translation)
except FileNotFoundError:
    print(f"Input file '{input_file_path}' not found.")
except Exception as e:
    print(f"An error occurred during file operations: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")