import tkinter as tk
from tkinter import ttk
from tkinter import Frame
import keywords
from test import translate_line
import codecs
import pyperclip
from tkinter import messagebox


#Global variables
translated_language = "es"
programming_language = "python"
current_keywords = keywords.es
supported_languages = [
    "Spanish Python",
    "French Python"
]


# Creates the window
window = tk.Tk()
window.title("GLOpyL")
#window.geometry("900x500")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{screen_width}x{screen_height}')
window.minsize(900, 500)
window.maxsize(screen_width, screen_height)
#window.config(bg="skyblue")


# Setup for comments checkbox
include_comments = tk.BooleanVar()
include_comments.set(True)  # Set to True by default


# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input_text.splitlines():
        translation = translate_line(line, translated_language, current_keywords, include_comments=include_comments.get())
        output += translation + "\n"
    outputTextBox.insert("1.0", output)


#to be used later for export purposes
# def save_to_rtf(output):
#     with codecs.open("output.rtf", "w", "utf-8") as output_file:
#         output_file.write(output)


def comboclick(event):
    global current_keywords
    if language_selection.get() == "Spanish Python":
        translated_language = "es"
        current_keywords = keywords.es
    elif language_selection.get() == "French Python":
        translated_language = "fr"
        current_keywords = keywords.fr


def copy_input_to_clipboard():
    original_code = inputTextBox.get("1.0", tk.END)
    pyperclip.copy(original_code)
    tk.messagebox.showinfo("Copy to Clipboard", "Original code has been copied to the clipboard.")


def copy_output_to_clipboard():
    translated_code = outputTextBox.get("1.0", tk.END)
    pyperclip.copy(translated_code)
    tk.messagebox.showinfo("Copy to Clipboard", "Translated code has been copied to the clipboard.")


titleLabel = ttk.Label(window, text="GLOpyL", font=("Arial", 50)) #height=20, width=50, 
titleLabel.grid(column=1, row=0, padx=100, pady=30)


inputFrame = Frame(window, width=400, height= 400)
inputFrame.grid(row=1, column=0, padx=50) #, padx=10, pady=5

inputHeaderFrame = Frame(inputFrame, width=400, height=50)
inputHeaderFrame.grid(row=0, column=0)
inputTextBox_label = ttk.Label(inputHeaderFrame, text="English Python", font="Arial")
inputTextBox_label.grid(column=0, row=0)
copyInputButton = tk.Button(inputHeaderFrame, text="Copy", font=("Arial", 16), command=copy_input_to_clipboard)
copyInputButton.grid(column=1, row=0) #, padx=10, pady=10

inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Arial", 16))
inputTextBox.grid(column=0, row=1) #, padx=10, pady=10


outputFrame = Frame(window, width=400, height=400)
outputFrame.grid(row=1, column=1)

outputHeaderFrame = Frame(outputFrame, width=400, height=50)
outputHeaderFrame.grid(row=0, column=0)
language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Arial", 15)) #width=15
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.grid(column=0, row=0)
copyOutputButton = tk.Button(outputHeaderFrame, text="Copy", font=("Arial", 16), command=copy_output_to_clipboard)
copyOutputButton.grid(column=1, row=0)

outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Arial", 16))
outputTextBox.grid(column=0, row=1)


translateButton = tk.Button(window, text="Translate", font=("Arial", 16), command=translateClick, bg="Green")
translateButton.grid(column=2, row=4, padx=10, pady=10)

commentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments, font=("Arial", 14))
commentsCheckbox.grid(column=1, row=4, padx=10, pady=10, sticky="w")

window.mainloop()
