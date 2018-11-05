import tkinter as tk
    
def MessageWindow(title,message):
    window = tk.Toplevel()
    window.title(title)
    for i in [0,2,4]: window.rowconfigure(i, minsize=20)
    for i in [0,2]: window.columnconfigure(i,minsize=30)

    label = tk.Label(window,text=message)
    label.grid(row=1,column=1)
    button = tk.Button(window,text="OK",command=window.destroy)
    button.grid(row=3,column=1)

def YesNoWindow(title,message,yes):
    
    window = tk.Toplevel()
    window.title(title)
    for i in [0, 2, 4]: window.rowconfigure(i, minsize=20)
    for i in [0, 3]: window.columnconfigure(i, minsize=30)

    label = tk.Label(window, text=message)
    label.grid(row=1, column=1,columnspan=2)
    yesButton = tk.Button(window, text="Yes", command = lambda: window.destroy() or yes())
    noButton = tk.Button(window, text="No", command = lambda: window.destroy())
    yesButton.grid(row=3, column=1)
    noButton.grid(row=3, column=2)
    
def EmptyMessage(message):
    window = tk.Toplevel()
    text = tk.Label(window,text=message)
    text.grid(row=1,column=1)
    return window