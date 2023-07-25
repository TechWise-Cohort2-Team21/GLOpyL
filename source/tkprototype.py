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
    global translated_language
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


titleLabel = ttk.Label(window, text="GLOpyL", font=("Arial", 50), justify=tk.CENTER) #height=20, width=50,
titleLabel.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.2, )


#############
inputFrame = Frame(window, width=400, height= 400)
inputFrame.place(relx=0.1, rely=0.25, relwidth=0.4, relheight=0.5) #, padx=10, pady=5

inputHeaderFrame = Frame(inputFrame, width=400, height=50)
inputHeaderFrame.place(relx=0, rely=0, relwidth=0.9, relheight=0.1)
inputTextBox_label = ttk.Label(inputHeaderFrame, text="English Python", font="Arial")
inputTextBox_label.place(relx=0, rely=0)
copyInputButton = tk.Button(inputHeaderFrame, text="Copy", font=("Arial", 16), command=copy_input_to_clipboard)
copyInputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=1) #, padx=10, pady=10

inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Arial", 10))
inputTextBox.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.9)


############
outputFrame = Frame(window, width=400, height=400)
outputFrame.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.5)

outputHeaderFrame = Frame(outputFrame, width=400, height=50)
outputHeaderFrame.place(relx=0.1, rely=0, relwidth=0.9, relheight=0.1)
language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Arial", 15)) #width=15
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.place(relx=0, rely=0)
copyOutputButton = tk.Button(outputHeaderFrame, text="Copy", font=("Arial", 16), command=copy_output_to_clipboard)
copyOutputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Arial", 10))
outputTextBox.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.9)


#######
translateButton = tk.Button(window, text="Translate", font=("Arial", 25), command=translateClick, bg="Green")
translateButton.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

#to be included later as an optional setting
# commentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments, font=("Arial", 14))
# commentsCheckbox.grid(column=0, row=5, sticky="w") #, padx=10, pady=10

window.mainloop()
