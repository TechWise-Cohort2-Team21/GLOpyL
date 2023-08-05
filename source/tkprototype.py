import tkinter as tk
from tkinter import ttk
from tkinter import Frame
import keywords
from code_translator import translate_line
import codecs
import pyperclip
from tkinter import messagebox
from langdetect import detect, detect_langs
import threading
from langdetect.lang_detect_exception import LangDetectException


# Global variables
translatedCodeText = None
translated_language = "es"
programming_language = "python"
current_keywords = keywords.es
supported_languages = [
    "Spanish Python",
    "French Python"
]


window = tk.Tk()
window.title("GLOpyL")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{screen_width}x{screen_height}')
window.minsize(900, 500)
window.maxsize(screen_width, screen_height)


include_comments = tk.BooleanVar()
include_comments.set(True)


def extract_comments(code):
    comments = [line for line in code.splitlines() if line.strip().startswith("#")]
    return " ".join(comments)


def translateClick():
    global translated_code

    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)


    if not input_text.strip():
        tk.messagebox.showwarning("Empty Input", "Please enter code to translate.")
        return

    try:
        human_language = detect(input_text)
        detected_language_var.set(f"{human_language} Python")

        translated_output = ""
        english_output = ""
        for line in input_text.splitlines():
            translation = translate_line(line, translated_language, current_keywords)

            translated_output += "# " + translation + "\\n"

            english_output += line + "\\n"


        output = translated_output + english_output
        outputTextBox.insert("1.0", output)
        translated_code = output

    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to translate code. Error: {str(e)}")


def comboclick(event):
    global current_keywords
    global translated_language
    selected_language = language_selection.get()

    if selected_language == "Spanish Python":
        translated_language = "es"
        current_keywords = keywords.es
    elif selected_language == "French Python":
        translated_language = "fr"
        current_keywords = keywords.fr
    else:
        # Handle unsupported language selection
        tk.messagebox.showwarning("Unsupported Language", f"The selected language '{selected_language}' is not supported.")
        # Optionally, reset the selection to a default value
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



translated_code = "..."


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
            else:
                file.write(translated_code)
        tk.messagebox.showinfo("File Saved", "Translated code has been saved successfully.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save translated code to the file. Error: {str(e)}")


include_comments = tk.BooleanVar()
include_comments.set(True)


def openSettings():
    global include_comments

    settingsWindow = tk.Toplevel(window)
    settingsWindow.title("Settings")

    # Update the include_comments variable based on the user's selection
    include_comments_checkbox = tk.Checkbutton(settingsWindow, text="Include Comments", variable=include_comments)
    include_comments_checkbox.pack()

    settingsWindow_width = 200
    settingsWindow_height = 200
    main_window_x = window.winfo_x()
    main_window_y = window.winfo_y()
    main_window_width = window.winfo_width()
    main_window_height = window.winfo_height()
    settingsWindow.geometry(f"{settingsWindow_width}x{settingsWindow_height}"
                            f"+{main_window_x + main_window_width // 2 - settingsWindow_width // 2}"
                            f"+{main_window_y + main_window_height // 2 - settingsWindow_height // 2}")


def detect_language_and_update():
    input_text = inputTextBox.get("1.0", tk.END).strip()

    try:
        human_language = detect(input_text)
        detected_language_var.set(f"{human_language} Python")
    except LangDetectException:
        detected_language_var.set("Meow?!")

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


@debounce(0.5)  # Delay of 0.5 seconds
def on_key_release(event):
    detect_language_and_update()

titleFrame = Frame(window, bg="lightgray")
titleFrame.place(relx=0, rely=0, relheight=0.15, relwidth=1)
titleLabel = ttk.Label(titleFrame, text="🌎 GLOpyL", font=("Bahnschrift Light", 40),
                       background="lightgray")  # height=20, width=50,
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

translateButton = tk.Button(window, text="Translate", font=("Bahnschrift Light", 25), command=translateClick,
                            bg="lightgray")
translateButton.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)

fileTypeVar = tk.StringVar()
fileTypeOptionMenu = tk.OptionMenu(window, fileTypeVar, ".py", ".txt", ".rtf")
fileTypeOptionMenu.place(relx=0.63, rely=0.75)

saveButton = tk.Button(window, text="Save", command=saveFile)
saveButton.place(relx=0.63, rely=0.8)

# Create the "Settings" button
settingsButton = tk.Button(window, text="Settings",
                           command=openSettings)
settingsButton.place(relx=0.8, rely=0.9, relwidth=0.15,
                     relheight=0.05)
...

window.mainloop()
