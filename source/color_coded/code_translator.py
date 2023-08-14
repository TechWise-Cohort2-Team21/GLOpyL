from googletrans import Translator
import keywords

translator = Translator()
translation_memory = {}

special_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '.', ':', ',', '[', ']', '{', '}', '+', '=', '-', '<', '>', '/', '\\', '\t']


def translate_word(word: str, lang: str, preserve_keywords: bool = False) -> str:
    global length_incrementer
    if lang not in translation_memory:
        translation_memory[lang] = {}
    if word in translation_memory[lang]:
        return translation_memory[lang][word]

    if lang == "es":
        dictionary = keywords.es
    elif lang == "fr":
        dictionary = keywords.fr
    elif lang == "zh":
        dictionary = keywords.zh
    elif lang == "hi":
        dictionary = keywords.hi
    else:
        dictionary = {}

    #if word in dictionary:
    #    if preserve_keywords:
    #        return word
    #    return dictionary[word]
    
    #translated_word = word
    #words = word.split("_")
    #try:
    #    translated_word = translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")
    #except Exception as e:
    #    print(f"Error translating word '{word}': {str(e)}")
    #translation_memory[lang][word] = translated_word
    #return translated_word

    if word in dictionary:
        translated_word = [dictionary[word][0], dictionary[word][1], (length_incrementer + 1), (length_incrementer + 1 + len(dictionary[word][0]))]
        length_incrementer += len(dictionary[word][0])
    

    else:
        words = word.split("_")
        translated_word = [translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"),
                            6,
                            (length_incrementer + 1),
                            (length_incrementer + 1 + len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")))]
        length_incrementer += len(translator.translate(" ".join(words), dest=lang).text.replace(" ", "_"))


    return translated_word


def translate_line(line: str, lang: str, include_comments: bool = True, preserve_keywords: bool = False) -> str:
    global length_incrementer
    length_incrementer = 0
    if not include_comments and line.lstrip().startswith("#"):
        return ""

    #result = []
    #current_word = ""

    #for char in line:
    #    if char.isalpha() or char == "_":
    #        current_word += char
    #    elif current_word == "":
    #        if char == "#" and not include_comments:
    #            break
    #        result.append(char)
    #    else:
    #        result.append(translate_word(current_word, lang, preserve_keywords))
    #        current_word = ""
    #        result.append(char)

    #result.append(translate_word(current_word, lang, preserve_keywords))
    #translated_line = "".join(result)
    #return translated_line

    words = []
    current_word = ""

    for char in line:
        if char == '\t':
            words.append([char, 0, length_incrementer, length_incrementer + 1])
            length_incrementer += 1
        elif char in special_char:
            current_word += char
        elif char.isalpha() or char == "_":
            current_word += char
        elif current_word == "" and char not in special_char:
            words.append(char)
        else:
            words.append(translate_word(current_word, lang))
            current_word = ""
            words.append(char)

    
                    


    
    words.append(translate_word(current_word, lang))
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


print(translate_line("this is a test sentence", "es"))
