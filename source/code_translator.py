from googletrans import Translator
import keywords

translator = Translator()
translation_memory = {}
glossary = {}
glossary_by_language = {
    "es": {},  # Spanish
    "fr": {},  # French
    "zh-CN": {},  # Chinese
    "hi": {}   # Hindi
}

def translate_word(word: str, lang: str, preserve_keywords: bool = False) -> str:
    if word in glossary_by_language[lang]:
        return glossary_by_language[lang][word]
    if word in glossary:
        return glossary[word]
    if lang not in translation_memory:
        translation_memory[lang] = {}
    if word in translation_memory[lang]:
        return translation_memory[lang][word]

    if lang == "es":
        dictionary = keywords.es
    elif lang == "fr":
        dictionary = keywords.fr
    elif lang == "zh-CN":
        dictionary = keywords.zh
    elif lang == "hi":
        dictionary = keywords.hi
    else:
        dictionary = {}

    if word in dictionary:
        if preserve_keywords:
            return word
        return dictionary[word]

    translated_word = word
    words = word.split("_")
    try:
        translated_word = translator.translate(" ".join(words), dest=lang).text.replace(" ", "_")
    except Exception as e:
        print(f"Error translating word '{word}': {str(e)}")
        print(lang)
    translation_memory[lang][word] = translated_word
    return translated_word


def translate_line(line: str, lang: str, include_comments: bool = True, preserve_keywords: bool = False) -> str:
    if not include_comments and line.lstrip().startswith("#"):
        return ""

    result = []
    current_word = ""

    for char in line:
        if char.isalpha() or char == "_":
            current_word += char
        elif current_word == "":
            if char == "#" and not include_comments:
                break
            result.append(char)
        else:
            result.append(translate_word(current_word, lang, preserve_keywords))
            current_word = ""
            result.append(char)

    result.append(translate_word(current_word, lang, preserve_keywords))
    translated_line = "".join(result)
    return translated_line
# Example of how to format/dissect output from a translation
# print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")