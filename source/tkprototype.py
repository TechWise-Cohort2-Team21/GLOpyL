import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from code_translator import translate_line
import codecs
import pyperclip
from tkinter import messagebox


#Global variables
translated_language = "es"
programming_language = "python"
supported_languages = [
    "Spanish Python",
    "French Python"
]


# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("900x500")
window.minsize(900, 500)
window.maxsize(window.winfo_screenwidth(), window.winfo_screenheight())


# Setup for comments checkbox
include_comments = tk.BooleanVar()
include_comments.set(True)  # Set to True by default


# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input_text.splitlines():
        translation = translate_line(line, translated_language, include_comments=include_comments.get())
        output += translation + "\n"
    outputTextBox.insert("1.0", output)


#to be used later for export purposes
# def save_to_rtf(output):
#     with codecs.open("output.rtf", "w", "utf-8") as output_file:
#         output_file.write(output)


def comboclick(event):
    global translated_language
    if language_selection.get() == "Spanish Python":
        translated_language = "es"
    elif language_selection.get() == "French Python":
        translated_language = "fr"


def copy_input_to_clipboard():
    original_code = inputTextBox.get("1.0", tk.END)
    pyperclip.copy(original_code)
    tk.messagebox.showinfo("Copy to Clipboard", "Original code has been copied to the clipboard.")


def copy_output_to_clipboard():
    translated_code = outputTextBox.get("1.0", tk.END)
    pyperclip.copy(translated_code)
    tk.messagebox.showinfo("Copy to Clipboard", "Translated code has been copied to the clipboard.")


sidebar = Frame(window, bg="lightgray")
sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)
globe = ttk.Label(sidebar, text="🌎", font=("Bahnschrift Light", 130), background="lightgray") #height=20, width=50,
globe.place(relx=0.1, rely=0)
titleLabel = ttk.Label(sidebar, text="GLOpyL", font=("Bahnschrift Light", 45), background="lightgray") #height=20, width=50,
titleLabel.place(relx=0.09, rely=0.3)
descLabel = ttk.Label(sidebar, text="subverting English's \nmonopoly on code.", font=("Arial", 16), background="lightgray")
descLabel.place(relx=0.1, rely=0.41)
glopyl_introduction = tk.Text(sidebar, font=("Bahnschrift Light", 12), wrap="word", border=0, bg="lightgray")
glopyl_introduction.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.9)
glopyl_introduction.insert("1.0", "This program translates Python code into a different world languages. At the moment, it is functional for English to Spanish and English to French. \n\nMore languages coming soon!")
glopyl_introduction.config(state="disabled")


functional_frame = Frame(window)
functional_frame.place(relx=0.2, rely=0, relwidth=0.6, relheight=1)


inputFrame = Frame(functional_frame)
inputFrame.place(relx=0.04, rely=0.1, relwidth=0.44, relheight=0.6) 

inputHeaderFrame = Frame(inputFrame)
inputHeaderFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
inputTextBox_label = ttk.Label(inputHeaderFrame, text="English Python", font=("Bahnschrift Light", 15))
inputTextBox_label.place(relx=0, rely=0)
copyInputButton = tk.Button(inputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12), command=copy_input_to_clipboard, bg="lightgray")
copyInputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8) #, padx=10, pady=10

inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Bahnschrift Light", 10), border=0)
inputTextBox.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


outputFrame = Frame(functional_frame)
outputFrame.place(relx=0.52, rely=0.1, relwidth=0.44, relheight=0.6)

outputHeaderFrame = Frame(outputFrame)
outputHeaderFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Bahnschrift Light", 15), state="readonly", width=15)
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.place(relx=0, rely=0)
copyOutputButton = tk.Button(outputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12), command=copy_output_to_clipboard, bg="lightgray")
copyOutputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)

outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Bahnschrift Light", 10), border=0)
outputTextBox.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)



translateButton = tk.Button(functional_frame, text="Translate", font=("Bahnschrift Light", 25), command=translateClick, bg="lightgray")
translateButton.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)

#to be included later as an optional setting
# commentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments, font=("Arial", 14))
# commentsCheckbox.grid(column=0, row=5, sticky="w") #, padx=10, pady=10

window.mainloop()
