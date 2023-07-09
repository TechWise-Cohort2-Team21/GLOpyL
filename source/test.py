#!pip3 install googletrans==3.1.0a0

from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

# translate a spanish text to english text (by default)
#translation = translator.translate("Hola Mundo")
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

keywords_en2es = {"def":"defina", "if":"si", "return":"regresa", "True":"Cierto"}

def translate_word(word: str) -> str:
    if word in keywords_en2es:
        return keywords_en2es[word]
    words = word.split("_") #change for other programming languages
    return "_".join([translator.translate(s, dest="es").text for s in words])

def translate_line(line: str) -> str:
    #todo: deal with lines that include "#"
    items = []
    current_word = ""
    for char in line:
        if not char.isalpha() and char!="_":
            if current_word!="":
                items.append(translate_word(current_word))
                current_word = ""
            items.append(char)
        else:
            current_word += char
    if current_word != "":
        items.append(translate_word(current_word))
    return "".join(items)

english = open("input.txt", "r")
with open("output.txt", "w") as spanish:
    for line in english:
        spanish.write(translate_line(line))
english.close()
spanish.close()