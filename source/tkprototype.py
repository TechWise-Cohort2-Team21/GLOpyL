# Prototype Tkinter GUI
import tkinter as tk
import test

# Creates the window
window = tk.Tk()
window.title("GLOpyL")
window.geometry("400x400")

# Translates the input box, places in output box
def translateClick():
    outputTextBox.delete()
    input = inputTextBox.get()
    output = ""
    for line in input:
        translation = test.translate_line(line)
        output.join(translation)
    outputTextBox.insert(output)


inputTextBox = tk.Text(window, height=3, width=9, font=("Arial", 16))
inputTextBox.grid(column=1, row=1)

outputTextBox = tk.Text(window, height=3, width=9, font=("Arial", 16))
outputTextBox.grid(column=3, row=1)

translateButton = tk.Button(window, text="Translate", font=("Arial", 16))
translateButton.grid(column=2, row=2)



window.mainloop()
