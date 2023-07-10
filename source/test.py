from googletrans import Translator, constants
from pprint import pprint


translated_language = "es"
programming_language = "python"
translator = Translator()
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")


keyword_file = open("keywords_en2"+translated_language+".txt", "r")
keywords = {}
for line in keyword_file:
    old, trans = line.strip().split(" ")
    keywords[old] = trans  
keyword_file.close()


def translate_word(word: str) -> str:
    if word in keywords:
        return keywords[word]
    if programming_language == "python":
        words = word.split("_")
        return translator.translate(" ".join(words), dest=translated_language).text.replace(" ", "_")


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


input = open("input.txt", "r")
with open("output.txt", "w") as output:
    for line in input:
        translation = translate_line(line)
        output.write(translation)
        #print(translation[:-1])
input.close()
output.close()