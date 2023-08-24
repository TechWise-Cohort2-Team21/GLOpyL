import tkinter as tk
from tkinter import ttk, Frame, messagebox
import pyperclip
from langdetect import detect
import threading
from langdetect.lang_detect_exception import LangDetectException
from code_translator import translate_line, glossary, glossary_by_language
import datetime
import openai
from gpt4all import GPT4All

from googletrans import Translator # I know it's gross code, we didn't have a choice

translated_language = "es"

supported_languages = [
    "Pitón Español",
    "Python Français",
    "Python 简体中文",  # Chinese Simplified
    "हिंदी पायथन"  # Hindi
]

model_path = "orca-mini-13b.ggmlv3.q4_0.bin"  # Update with the correct path if needed
model = GPT4All(model_path)

translated_code = ""

translation_history = []

openai.api_key = ""

window = tk.Tk()
window.title("GLOpyL")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{screen_width}x{screen_height}')
window.minsize(900, 500)
window.maxsize(window.winfo_screenwidth(), window.winfo_screenheight())

include_comments = tk.BooleanVar()
include_comments.set(True)
preserve_keywords = tk.BooleanVar()
preserve_keywords.set(False)


def lang_abbreviation_to_full(abbr: str):
    conversion = {"en": "English Python", "es": "Pitón Español", "fr": "Python Français", "zh": "Chinese",
                  "hi": "हिंदी पायथन", "zh-CN": "Python 简体中文"}
    return conversion[abbr] if abbr in conversion else "Unrecognized Language"


def get_code_summary(code, summary_model):
    global translated_language
    translator = Translator()
    summary_prompt = translator.translate("Please summarize the following code:", dest=translated_language).text
    summary_prompt += f"\n{code}"

    if summary_model == "openai":
        openai_api_key = "YOUR-API-KEY-HERE"
        if not openai_api_key or openai_api_key == "YOUR-API-KEY-HERE":
            return "Error: Please add your OpenAI API key to use this feature."

        openai.api_key = openai_api_key

        def call_openai_gpt3(prompt):
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=100
                )
                summary = response.choices[0].text.strip()
                return summary
            except Exception as e:
                return f"Error: {str(e)}"

        summary = call_openai_gpt3(summary_prompt)
    elif summary_model == "gpt4all":
        gpt4all_prompt = "Please summarize the following code:\n" + code
        summary = model.generate(gpt4all_prompt, max_tokens=200)
    else:
        summary = "Model not supported"

    return summary


def translate():
    global translated_code
    global include_comments
    global preserve_keywords

    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)

    try:
        translated_code = ""
        lines = input_text.splitlines()
        num_lines = len(lines)

        for i, line in enumerate(lines):
            translation = translate_line(line, translated_language, include_comments.get(), preserve_keywords.get())
            translated_code += translation + "\n"

            outputTextBox.delete("1.0", tk.END)
            outputTextBox.insert("1.0", translated_code)
            loading_line.place(relwidth=i / num_lines)
            loading_line.place(relwidth=0)

            add_to_history(line, translation, translated_language)  # Adding translation to history


        window.update_idletasks()  # Update the GUI to show the translated code

        # summary_language = summary_language_var.get()  # Get the selected summary language
        # code_summary = get_code_summary(translated_code, summary_language)  # Call get_code_summary with summary_language
        # summary_textbox.delete("1.0", tk.END)
        # summary_textbox.insert("1.0", code_summary)
        if tk.messagebox.askyesno("Code Summary", "Would you like to get a summary of this translated code?"):
            summary_model = summary_model_var.get()
            code_summary = get_code_summary(input_text, summary_model)
            summary_textbox.delete("1.0", tk.END)
            summary_textbox.insert("1.0", code_summary)


    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to translate code. Error: {str(e)}")


def comboclick(event):
    global translated_language
    selected_language = language_selection.get()

    if selected_language == "Pitón Español":
        translated_language = "es"
    elif selected_language == "Python Français":
        translated_language = "fr"
    elif selected_language == "Python 简体中文":
        translated_language = "zh-CN"
    elif selected_language == "हिंदी पायथन":
        translated_language = "hi"
    else:
        tk.messagebox.showwarning("Unsupported Language",
                                  f"The selected language '{selected_language}' is not supported.")
        language_selection.set("Select Language")


def add_to_history(input_text, translated_text, language):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    translation_history.append((input_text, translated_text, language, timestamp))


from tkinter import ttk


def view_history():
    history_window = tk.Toplevel(window)
    history_window.title("Translation History")
    history_window.geometry("800x400")

    history_tree = ttk.Treeview(history_window, columns=("Timestamp", "Language", "Original", "Translated"))
    history_tree.heading("#1", text="Timestamp")
    history_tree.heading("#2", text="Language")
    history_tree.heading("#3", text="Original")
    history_tree.heading("#4", text="Translated")
    history_tree.pack(fill=tk.BOTH, expand=1)

    for input_text, translated_text, language, timestamp in translation_history:
        history_tree.insert("", tk.END, values=(timestamp, language, input_text, translated_text))

    def revert_to_selected():
        selected_items = history_tree.selection()
        selected_translations = [history_tree.item(item)["values"][3] for item in selected_items]
        concatenated_translation = "\n".join(selected_translations)
        outputTextBox.delete("1.0", tk.END)
        outputTextBox.insert("1.0", concatenated_translation)

    revert_button = tk.Button(history_window, text="Revert to Selected", command=revert_to_selected)
    revert_button.pack()


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
        detected_language_var.set(f"{human_language}")
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
    # selected_language.set("Pitón Español")  # Default to Spanish
    language_dropdown = ttk.Combobox(glossary_window, textvariable=selected_language)
    # language_dropdown['values'] = supported_languages
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

    def edit_term(event):
        selected_term_index = glossary_list.curselection()[0]  # Fixed variable name
        lang = selected_language.get()
        selected_term, selected_translation = list(glossary_by_language[lang].items())[selected_term_index]

        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Term")

        term_entry = tk.Entry(edit_window)
        term_entry.insert(0, selected_term)
        term_entry.pack()

        translation_entry = tk.Entry(edit_window)
        translation_entry.insert(0, selected_translation)
        translation_entry.pack()

        def save_changes():
            new_term = term_entry.get()
            new_translation = translation_entry.get()
            del glossary_by_language[lang][selected_term]  # Remove old term
            glossary_by_language[lang][new_term] = new_translation  # Add new term
            update_glossary_list()
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.pack()

        cancel_button = tk.Button(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.pack()

    def delete_term():
        selected_term_index = glossary_list.curselection()[0]
        lang = selected_language.get()
        selected_term = list(glossary_by_language[lang].keys())[selected_term_index]

        if tk.messagebox.askyesno("Delete Term", f"Are you sure you want to delete '{selected_term}'?"):
            del glossary_by_language[lang][selected_term]  # Remove the term
            update_glossary_list()  # Refresh the glossary listw

    glossary_list = tk.Listbox(glossary_window)  # Fixed variable name
    glossary_list.pack()
    glossary_list.bind('<Double-Button-1>', edit_term)  # Moved binding after the creation of Listbox

    update_glossary_list()

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

    delete_button = tk.Button(glossary_window, text="Delete Term", command=delete_term)
    delete_button.pack()

    glossary_list.pack()
    update_glossary_list()


@debounce(0.5)  # Delay of 0.5 seconds
def on_key_release(event):
    detect_language_and_update()


sidebar = Frame(window, bg="grey80")
sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

globe = ttk.Label(sidebar, text="🌎", font=("Bahnschrift Light", 130), background="grey80")  # height=20, width=50,
globe.place(relx=0.1, rely=0)
titleLabel = ttk.Label(sidebar, text="GLOpyL", font=("Bahnschrift Light", 45),
                       background="grey80")  # height=20, width=50,
titleLabel.place(relx=0.09, rely=0.3)
descLabel = ttk.Label(sidebar, text="subverting English's \nmonopoly on code.", font=("Arial", 16), background="grey80")
descLabel.place(relx=0.1, rely=0.41)
glopyl_introduction = tk.Text(sidebar, font=("Bahnschrift Light", 12), wrap="word", border=0, bg="grey80")
glopyl_introduction.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.9)
glopyl_introduction.insert("1.0",
                           "This program translates Python code into a different world languages. At the moment, it is functional for English to Spanish and English to French. \n\nMore languages coming soon!")
glopyl_introduction.config(state="disabled")

############

functional_frame = Frame(window)
functional_frame.place(relx=0.2, rely=0, relwidth=0.6, relheight=1)

inputFrame = Frame(functional_frame, background="pink")
inputFrame.place(relx=0.04, rely=0.05, relwidth=0.44, relheight=0.9)
inputHeaderFrame = Frame(inputFrame)
inputHeaderFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
detected_language_var = tk.StringVar()
detected_language_var.set("Detecting language...")  # Default text
detected_language_label = ttk.Label(inputHeaderFrame, textvariable=detected_language_var,
                                    font=("Bahnschrift Light", 15))
detected_language_label.place(relx=0, rely=0)  # Adjust the placement as needed
copyInputButton = tk.Button(inputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12),
                            command=copy_input_to_clipboard, bg="lightgray")
copyInputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)  # , padx=10, pady=10
inputTextBox = tk.Text(inputFrame, height=10, width=30, font=("Bahnschrift Light", 10), border=0)
inputTextBox.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
inputTextBox.bind("<KeyRelease>", on_key_release)

outputFrame = Frame(functional_frame)
outputFrame.place(relx=0.52, rely=0.05, relwidth=0.44, relheight=0.9)
outputHeaderFrame = Frame(outputFrame)
outputHeaderFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
language_selection = ttk.Combobox(outputHeaderFrame, value=supported_languages, font=("Bahnschrift Light", 15),
                                  state="readonly", width=15)
language_selection.current(0)
language_selection.bind("<<ComboboxSelected>>", comboclick)
language_selection.place(relx=0, rely=0)
copyOutputButton = tk.Button(outputHeaderFrame, text="COPY", font=("Bahnschrift Light", 12),
                             command=copy_output_to_clipboard, bg="grey80")
copyOutputButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.8)
outputTextBox = tk.Text(outputFrame, height=10, width=30, font=("Bahnschrift Light", 10), border=0)
outputTextBox.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
loading_line = ttk.Label(outputFrame, background="grey80")
loading_line.place(relx=0, rely=0.98, relwidth=0, relheight=0.02)


#########

settings_frame = Frame(window)
settings_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)
settingsButton = tk.Button(settings_frame, text="Settings", command=openSettings, background="grey80")
settingsButton.place(relx=0, rely=0.05, relwidth=0.8, relheight=0.05)
glossary_button = tk.Button(settings_frame, text="Manage Glossary", command=manage_glossary, background="grey80")
glossary_button.place(relx=0, rely=0.15, relwidth=0.8, relheight=0.05)
fileTypeVar = tk.StringVar(window, ".py")
fileTypeOptionMenu = tk.OptionMenu(settings_frame, fileTypeVar, ".py", ".txt", ".rtf")
fileTypeOptionMenu.config(background="grey80")
fileTypeOptionMenu.place(relx=0, rely=0.25, relwidth=0.35, relheight=0.05)
saveButton = tk.Button(settings_frame, text="Save", command=saveFile, background="grey80")
saveButton.place(relx=0.45, rely=0.25, relwidth=0.35, relheight=0.05)

summary_model_label = tk.Label(settings_frame, text="Summary AI:")
summary_model_label.place(relx=0, rely=0.35, relwidth=0.35, relheight=0.05)
summary_model_var = tk.StringVar()
summary_model_var.set("openai")  # Default to OpenAI
summary_model_dropdown = ttk.Combobox(settings_frame, textvariable=summary_model_var)
summary_model_dropdown['values'] = ("openai", "gpt4all")
summary_model_dropdown.place(relx=0.45, rely=0.35, relwidth=0.35, relheight=0.05)

summary_label = tk.Label(settings_frame, text="Code Summary:")
summary_label.place(relx=0, rely=0.45, relwidth=0.8, relheight=0.05)
summary_textbox = tk.Text(settings_frame, height=5, wrap=tk.WORD)
summary_textbox.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.45)

view_history_button = tk.Button(window, text="View History", command=view_history)
view_history_button.pack()


window.mainloop()
