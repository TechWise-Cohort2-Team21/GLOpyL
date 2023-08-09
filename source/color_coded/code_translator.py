from googletrans import Translator, constants
from pprint import pprint
import keywords



translator = Translator()

translation_memory = {}



def translate_word(word, lang, current_keywords):
    global length_incrementer

    if lang == "es":
        dictionary = keywords.es
    elif lang == "fr":
        dictionary = keywords.fr
    else:
        dictionary = current_keywords
    
    if word in dictionary:
        translated_word = [dictionary[word][0], dictionary[word][1], (length_incrementer + 1), (length_incrementer + 1 + len(dictionary[word][0]))]
        length_incrementer += len(dictionary[word][0])
    else:
        words = word.split("_")
#        if word == ' ':
#            translated_word = [' ', 0, length_incrementer, length_incrementer + 1]
#        else:
#            translated_word = [translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"),
#                                6,
#                                (length_incrementer + 1),
#                                (length_incrementer + 1 + len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")))]
#            length_incrementer += 1 + len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"))
        translated_word = [translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"),
                            6,
                            (length_incrementer + 1),
                            (length_incrementer + 1 + len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")))]
        length_incrementer += len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"))


    return translated_word

def translate_line(line: str, lang: str, current_keywords, include_comments: bool = True) -> str:
    global length_incrementer
    length_incrementer = 0
    if not include_comments and line.lstrip().startswith("#"):
        return line
    ...

    ...


    words = []
    current_word = ""

    for char in line:
        if char.isalpha() or char == "_":
            current_word += char
        #if char == " ":
        #    words.append("a")
        elif current_word == "":
            words.append(char)
        else:
            words.append(translate_word(current_word, lang, current_keywords))
            current_word = ""
            words.append(char)
                    

    words.append(translate_word(current_word, lang, current_keywords))
    translated_line = []
    translated_line.append(words)


    for i in translated_line:
        for j in range(len(i)):
            if i[j] == ' ':
                i[j] = [' ', 0, (i[j-1][3]), (i[j-1][3]) + 1]

                for k in range(j, len(i)):
                    if len(i[k]) > 2:
                        if type(i[k]) == list:
                            i[k][2] += 1
                            i[k][3] += 1



    

    return translated_line

length_incrementer = 0


print(translate_line("apple and pear and orange", "es", "es"))

