import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from code_translator import translate_line
import pyperclip
from tkinter import messagebox
from langdetect import detect
import threading
from langdetect.lang_detect_exception import LangDetectException
from code_translator import translate_line, glossary, glossary_by_language

translated_language = "es"
supported_languages = [
    "Spanish Python",
    "French Python",
    "Chinese Python",
    "Hindi Python"
]
translated_code = ""

window = tk.Tk()
window.title("GLOpyL")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{screen_width}x{screen_height}')
window.minsize(900, 500)
window.maxsize(screen_width, screen_height)

include_comments = tk.BooleanVar()
include_comments.set(True)
preserve_keywords = tk.BooleanVar()
preserve_keywords.set(False)


def lang_abbreviation_to_full(abbr: str):
    conversion = {"en": "English", "es": "Spanish", "fr": "French", "zh": "Chinese", "hi": "Hindi"}
    return conversion[abbr] if abbr in conversion else None


def translate():
    global translated_code
    global include_comments
    global preserve_keywords

    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)

    try:
        translated_code = ""

        for line in input_text.splitlines():
            translation = translate_line(line, translated_language, include_comments.get(), preserve_keywords.get())
            translated_code += translation + "\n"

        outputTextBox.insert("1.0", translated_code)

    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to translate code. Error: {str(e)}")


def comboclick(event):
    global translated_language
    selected_language = language_selection.get()

    if selected_language == "Spanish Python":
        translated_language = "es"
    elif selected_language == "French Python":
        translated_language = "fr"
    elif selected_language == "Chinese Python":
        translated_language = "zh"
    elif selected_language == "Hindi Python":
        translated_language = "hi"
    else:
        tk.messagebox.showwarning("Unsupported Language",
                                  f"The selected language '{selected_language}' is not supported.")
        language_selection.set("Select Language")


def copy_input_to_clipboard():
    try:
        original_code = inputTextBox.get("1.0", tk.END)
        pyperclip.copy(original_code)
        tk.messagebox.showinfo("Copy to Clipboard", "Original code has been copied to the clipboard.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to copy original code to the clipboard. Error: {str(e)}")


def copy_output_to_clipboard():
    try:
        translated_code = outputTextBox.get("1.0", tk.END)
        pyperclip.copy(translated_code)
        tk.messagebox.showinfo("Copy to Clipboard", "Translated code has been copied to the clipboard.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to copy translated code to the clipboard. Error: {str(e)}")


def saveFile():
    global translated_code
    fileType = fileTypeVar.get()

    try:
        with open("translated_code" + fileType, "w", encoding="utf-8") as file:
            if fileType == ".rtf":
                # Write RTF header and content
                file.write("{\\\\rtf1\\\\ansi\\\\deff0\\n")
                file.write(translated_code.replace("\\n", "\\\\par\\n"))
                file.write("}")
            elif fileType == ".py":
                lines = translated_code.split("\n")
                for line in lines:
                    file.write(f"# {line}\n")
                input_text = inputTextBox.get("1.0", tk.END)
                file.write("\n\n\n")
                file.write(input_text)
            else:
                file.write(translated_code)
        tk.messagebox.showinfo("File Saved", "Translated code has been saved successfully.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save translated code to the file. Error: {str(e)}")


def openSettings():
    global include_comments
    global preserve_keywords

    settingsWindow = tk.Toplevel(window)
    settingsWindow.title("Settings")

    include_comments_checkbox = tk.Checkbutton(settingsWindow, text="Include Comments", variable=include_comments)
    include_comments_checkbox.pack()

    preserve_keywords_checkbox = tk.Checkbutton(settingsWindow, text="Preserve Keywords", variable=preserve_keywords)
    preserve_keywords_checkbox.pack()

    settingsWindow_width = 200
    settingsWindow_height = 200
    settingsWindow.geometry(f"{settingsWindow_width}x{settingsWindow_height}")


def detect_language_and_update():
    input_text = inputTextBox.get("1.0", tk.END).strip()

    try:
        human_language = lang_abbreviation_to_full(detect(input_text))
        detected_language_var.set(f"{human_language} Python")
    except LangDetectException:
        detected_language_var.set("Error Detecting Language")

    translate()


def debounce(wait):
    def decorator(fn):
        def debounced(*args, **kwargs):
            nonlocal timer
            timer.cancel()
            timer = threading.Timer(wait, lambda: fn(*args, **kwargs))
            timer.start()

        timer = threading.Timer(wait, lambda: None)
        timer.start()
        return debounced

    return decorator


def manage_glossary():
    glossary_window = tk.Toplevel(window)
    glossary_window.title("Glossary Management")

    # Language selection dropdown
    selected_language = tk.StringVar()
    selected_language.set("es")  # Default to Spanish
    language_dropdown = ttk.Combobox(glossary_window, textvariable=selected_language)
    language_dropdown['values'] = ("es", "fr", "zh", "hi")
    language_dropdown.pack()

    def add_term():
        term = term_entry.get()
        translation = translation_entry.get()
        lang = selected_language.get()
        glossary_by_language[lang][term] = translation
        update_glossary_list()

    def update_glossary_list(*args):
        glossary_list.delete(0, tk.END)
        lang = selected_language.get()
        for term, translation in glossary_by_language[lang].items():
            glossary_list.insert(tk.END, f"{term} : {translation}")

    selected_language.trace('w', update_glossary_list)
    term_label = tk.Label(glossary_window, text="Term:")
    term_label.pack()
    term_entry = tk.Entry(glossary_window)
    term_entry.pack()

    translation_label = tk.Label(glossary_window, text="Translation:")
    translation_label.pack()
    translation_entry = tk.Entry(glossary_window)
    translation_entry.pack()

    add_button = tk.Button(glossary_window, text="Add Term", command=add_term)
    add_button.pack()

    glossary_list = tk.Listbox(glossary_window)
    glossary_list.pack()
    update_glossary_list()


@debounce(0.5)  # Delay of 0.5 seconds
def on_key_release(event):
    detect_language_and_update()


titleFrame = Frame(window, bg="grey80")
titleFrame.place(relx=0, rely=0, relheight=0.15, relwidth=1)
titleLabel = ttk.Label(titleFrame, text="🌎 GLOpyL", font=("Bahnschrift Light", 40),
                       background="grey80")  # height=20, width=50,
titleLabel.place(relx=0.1, rely=0.2)

# descLabel = ttk.Label(titleFrame, text="subverting English's monopoly on code.", font=("Arial", 18), background="lightgray")
# descLabel.place(relx=0.32, rely=0.55)


#############
inputFrame = Frame(window)
inputFrame.place(relx=0.1, rely=0.2, relwidth=0.4, relheight=0.5)  # , padx=10, pady=5

inputHeaderFrame = Frame(inputFrame, width=400, height=50)
inputHeaderFrame.place(relx=0, rely=0, relwidth=0.9, relheight=0.1)

detected_language_var = tk.StringVar()
detected_language_var.set("Detecting language...")  # Default text

detected_language_label = ttk.Label(inputHeaderFrame, textvariable=detected_language_var,
                                    font=("Bahnschrift Light", 15))
detected_language_label.place(relx=0, rely=0)  # Adjust the placement as needed

# inputTextBox_label = ttk.Label(inputHeaderFrame, text="English Python", font=("Bahnschrift Light", 15))
# inputTextBox_label.place(relx=0, rely=0)

copyInputButton = tk.Button(inputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12),
                            command=copy_input_to_clipboard)
copyInputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)  # , padx=10, pady=10

inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Bahnschrift Light", 10))
inputTextBox.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.9)

inputTextBox.bind("<KeyRelease>", on_key_release)

outputFrame = Frame(window, width=400, height=400)
outputFrame.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.5)

outputHeaderFrame = Frame(outputFrame, width=400, height=50)
outputHeaderFrame.place(relx=0.1, rely=0, relwidth=0.9, relheight=0.1)

language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Bahnschrift Light", 15),
                                  state="readonly")  # width=15
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.place(relx=0, rely=0)

copyOutputButton = tk.Button(outputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12),
                             command=copy_output_to_clipboard)
copyOutputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)

outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Bahnschrift Light", 10))
outputTextBox.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.9)

# translateButton = tk.Button(window, text="Translate", font=("Bahnschrift Light", 25), command=translate, bg="lightgray")
# translateButton.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)

fileTypeVar = tk.StringVar()
fileTypeOptionMenu = tk.OptionMenu(window, fileTypeVar, ".py", ".txt", ".rtf")
fileTypeOptionMenu.place(relx=0.63, rely=0.75)

saveButton = tk.Button(window, text="Save", command=saveFile)
saveButton.place(relx=0.63, rely=0.8)

glossary_button = tk.Button(window, text="Manage Glossary", command=manage_glossary)
glossary_button.pack()

settingsButton = tk.Button(window, text="Settings",
                           command=openSettings)
settingsButton.place(relx=0.8, rely=0.9, relwidth=0.15,
                     relheight=0.05)
...

window.mainloop()
