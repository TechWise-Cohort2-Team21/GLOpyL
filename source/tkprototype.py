# Prototype Tkinter GUI
import tkinter as tk
from test import translate_word, translate_line

# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("900x500")

# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete("1.0", tk.END)
    input_text = inputTextBox.get("1.0", tk.END)
    output = ""
    for line in input_text.splitlines():
        translation = translate_line(line)
        output += translation + "\n"
    outputTextBox.insert(tk.END, output)

inputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
inputTextBox.grid(column=1, row=1, padx=10, pady=10)

outputTextBox = tk.Text(window, height=10, width=30, font=("Arial", 16))
outputTextBox.grid(column=3, row=1, padx=10, pady=10)

translateButton = tk.Button(window, text="Translate", font=("Arial", 16), command=translateClick)
translateButton.grid(column=2, row=2, padx=10, pady=10)

window.mainloop()
