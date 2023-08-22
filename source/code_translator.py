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


def translate_line(line: str, lang: str, include_comments: bool = True, preserve_keywords: bool = False) -> list:
    global length_incrementer
    length_incrementer = 0
    if not include_comments and line.lstrip().startswith("#"):
        return []

    words = []
    current_word = ""
    current_color = 0

    for char in line:
        if char == '\t':
            if current_word:
                words.append(translate_word(current_word, lang))
                current_word = ""
            words.append(['\t', 0, length_incrementer, length_incrementer + 4])
            length_incrementer += 4
        elif char in special_char:
            if current_word:
                words.append(translate_word(current_word, lang))
                current_word = ""
            words.append([char, 6, length_incrementer, length_incrementer + 1])
            length_incrementer += 1
        elif char.isalpha() or char == "_":
            current_word += char
        else:
            if current_word:
                words.append(translate_word(current_word, lang))
                current_word = ""
            words.append(char)

    if current_word:
        words.append(translate_word(current_word, lang))
    
    return words


length_incrementer = 0


print(translate_line("this is a test", "es"))
