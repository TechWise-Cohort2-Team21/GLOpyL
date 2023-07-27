import tkinter as tk
from tkinter import ttk
from tkinter import Frame
import keywords
from code_translator import translate_line
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
    global translated_code  # This allows us to modify the global variable

    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input_text.splitlines():
        translation = translate_line(line, translated_language, current_keywords, include_comments=include_comments.get())
        output += translation + "\n"

    outputTextBox.insert("1.0", output)
    translated_code = output  # Save the translated code to the global variable



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


translated_code = "..."  # the translated code


# Then in your saveFile function...
def saveFile():
    global translated_code  # This allows us to access the global variable
    # Get the selected file type
    fileType = fileTypeVar.get()
    # Save the translated code as a file of the selected type
    with open("translated_code" + fileType, "w", encoding="utf-8") as file:
        file.write(translated_code)


titleFrame = Frame(window, bg="lightgray")
titleFrame.place(relx=0, rely=0, relheight=0.15, relwidth=1)
titleLabel = ttk.Label(titleFrame, text="🌎 GLOpyL", font=("Bahnschrift Light", 40), background="lightgray") #height=20, width=50,
titleLabel.place(relx=0.1, rely=0.2)
# descLabel = ttk.Label(titleFrame, text="subverting English's monopoly on code.", font=("Arial", 18), background="lightgray")
# descLabel.place(relx=0.32, rely=0.55)


#############
inputFrame = Frame(window)
inputFrame.place(relx=0.1, rely=0.2, relwidth=0.4, relheight=0.5) #, padx=10, pady=5

inputHeaderFrame = Frame(inputFrame, width=400, height=50)
inputHeaderFrame.place(relx=0, rely=0, relwidth=0.9, relheight=0.1)
inputTextBox_label = ttk.Label(inputHeaderFrame, text="English Python", font=("Bahnschrift Light", 15))
inputTextBox_label.place(relx=0, rely=0)
copyInputButton = tk.Button(inputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12), command=copy_input_to_clipboard)
copyInputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8) #, padx=10, pady=10

inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Bahnschrift Light", 10))
inputTextBox.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.9)


############
outputFrame = Frame(window, width=400, height=400)
outputFrame.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.5)

outputHeaderFrame = Frame(outputFrame, width=400, height=50)
outputHeaderFrame.place(relx=0.1, rely=0, relwidth=0.9, relheight=0.1)
language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Bahnschrift Light", 15), state="readonly") #width=15
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.place(relx=0, rely=0)
copyOutputButton = tk.Button(outputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12), command=copy_output_to_clipboard)
copyOutputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)

outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Bahnschrift Light", 10))
outputTextBox.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.9)



translateButton = tk.Button(window, text="Translate", font=("Bahnschrift Light", 25), command=translateClick, bg="lightgray")
translateButton.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)


fileTypeVar = tk.StringVar()
fileTypeOptionMenu = tk.OptionMenu(window, fileTypeVar, ".py", ".txt", ".csv")
fileTypeOptionMenu.place(relx=0.63, rely=0.75)  # Adjust the coordinates and dimensions as needed

saveButton = tk.Button(window, text="Save", command=saveFile)
saveButton.place(relx=0.63, rely=0.8)  # Adjust the coordinates and dimensions as needed
...


#to be included later as an optional setting
# commentsCheckbox = tk.Checkbutton(window, text="Include Comments", variable=include_comments, font=("Arial", 14))
# commentsCheckbox.grid(column=0, row=5, sticky="w") #, padx=10, pady=10

window.mainloop()
