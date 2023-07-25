import tkinter as tk
from tkinter import ttk
import test
import keywords
import codecs
import pyperclip
from tkinter import messagebox

# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("900x500")

supported_languages = [
    "Spanish",
    "French"
]
currentkeywords = keywords.es

# Variable to store the previous programming language
previous_language = "python"
include_comments = tk.BooleanVar()
include_comments.set(True)  # Set to True by default

# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input_text.splitlines():
        translation = test.translate_line(line, test.translated_language, currentkeywords, include_comments=include_comments.get())
        output += translation + "\n"
    outputTextBox.insert("1.0", output)
    save_to_rtf(output)
    fake_dictionary = {"else":"démas"}
    commentsCheckbox.config(text = fake_dictionary["else"])


def save_to_rtf(output):
    with codecs.open("output.rtf", "w", "utf-8") as output_file:
        output_file.write(output)


def comboclick(event):
    #global previous_language
    global currentkeywords
    if language_selection.get() == "Spanish":
        test.translated_language = "es"
        currentkeywords = keywords.es
    elif language_selection.get() == "French":
        test.translated_language = "fr"
        currentkeywords = keywords.fr

def copy_to_clipboard():
    translated_code = outputTextBox.get("1.0", tk.END)
    pyperclip.copy(translated_code)
    tk.messagebox.showinfo("Copy to Clipboard", "Translated code has been copied to the clipboard.")


language_selection = ttk.Combobox(window, value=supported_languages, font=("Arial", 15), width=10)
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.grid(column=2, row=2, padx=10, pady=10)
language_selection_label = ttk.Label(window, text="Language:", font="Arial")
language_selection_label.grid(column=2, row=1)

inputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
inputTextBox.grid(column=1, row=3, padx=10, pady=10)
inputTextBox_label = ttk.Label(window, text="Input:", font="Arial")
inputTextBox_label.grid(column=1, row=2)

outputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
outputTextBox.grid(column=3, row=3, padx=10, pady=10)
outputTextBox_label = ttk.Label(window, text="Output:", font="Arial")
outputTextBox_label.grid(column=3, row=2)

translateButton = tk.Button(window, text="Translate", font=("Arial", 16), command=translateClick, bg="Green")
translateButton.grid(column=2, row=4, padx=10, pady=10)

copyButton = tk.Button(window, text="Copy", font=("Arial", 16), command=copy_to_clipboard)
copyButton.grid(column=2, row=5, padx=10, pady=10)

commentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments, font=("Arial", 14))
commentsCheckbox.grid(column=1, row=4, padx=10, pady=10, sticky="w")

window.mainloop()
