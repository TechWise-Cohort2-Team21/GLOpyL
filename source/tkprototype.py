# Prototype Tkinter GUI
import tkinter as tk
from tkinter import ttk
import test

# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("900x500")

supported_languages = [
    "Spanish",
    "French"
]


# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input:
        translation = test.translate_line(line)
        output.join(translation)
    outputTextBox.insert(output)

def comboclick(event):
    if language_selection.get() == "Spanish":
        test.translated_language = "es"
    elif language_selection.get() == "French":
        test.translated_language = "fr"




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



window.mainloop()
