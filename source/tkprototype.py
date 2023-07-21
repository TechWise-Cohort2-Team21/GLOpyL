# Prototype Tkinter GUI
import tkinter as tk
from tkinter import ttk
import test
import codecs

# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("900x500")

supported_languages = [
    "Spanish",
    "French"
]

include_comments_var = tk.BooleanVar()
include_comments_var.set(True)


# Translates the input box, places in output box

def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    include_comments = include_comments_var.get()  # Get the user's choice
    output = ""
    for line in input_text.splitlines():
        translation = test.translate_line(line, include_comments)  # Pass both line and include_comments
        output += translation + "\n"
    outputTextBox.insert("1.0", output)
    save_to_rtf(output)


def save_to_rtf(output):
    with codecs.open("output.rtf", "w", "utf-8") as output_file:
        output_file.write(output)


def comboclick(event):
    if language_selection.get() == "Spanish":
        test.translated_language = "es"
    elif language_selection.get() == "French":
        test.translated_language = "fr"


language_selection = ttk.Combobox(window, value=supported_languages, font=("Arial", 15), width=10)
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.grid(column=2, row=1, padx=10, pady=10)

inputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
inputTextBox.grid(column=1, row=2, padx=10, pady=10)

outputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
outputTextBox.grid(column=3, row=2, padx=10, pady=10)

includeCommentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments_var,
                                         font=("Arial", 15))
includeCommentsCheckbox.grid(column=2, row=2, padx=10, pady=10)

translateButton = tk.Button(window, text="Translate", font=("Arial", 16), command=translateClick, bg="Green")
translateButton.grid(column=2, row=3, padx=10, pady=10)

window.mainloop()
