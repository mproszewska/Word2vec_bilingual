import importlib
import tkinter as tk
import pathlib
import PIL
import atexit
import os
import sys

import Word2Vec as wv
import SourcesFrame as sf
import GraphFrame as gf
import WordsFrame as wf
import MessageWindow as mw
import SaveToFile as sv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+"/lib")
@atexit.register
def atexit():
    for f in sf.unsaved_files:
        os.remove(f)

class App(tk.Tk):

    def exit(self):
        mw.YesNoWindow(title="Exit",message="Unsaved data will be lost.\n Do you want to exit?",yes=self.quit)

    def save(self):
        sv.SaveVectorSpaces(sf.bVectorSpace,sf.rVectorSpace)
        sv.SaveList(sf.bWords,sf.rWords,sf.bVectorSpace, sf.rVectorSpace)
        sf.unsaved_files = []
        mw.MessageWindow(title="Save", message="Saved.\n")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        self.frames = {}

        for F in (gf.GraphFrame, sf.SourcesFrame, wf.WordsFrame):
            frame = F(container)
            self.frames[F] = frame
            frame.grid(row=0, column=0,sticky = "nsew")

        self.show_frame(gf.GraphFrame)

        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        menu.add_command(label="Graph",command=lambda: self.show_frame(gf.GraphFrame))
        menu.add_command(label="Words",command=lambda: self.show_frame(wf.WordsFrame))
        menu.add_command(label="Sources",command=lambda: self.show_frame(sf.SourcesFrame))
        menu.add_command(label="Save", command=self.save)
        menu.add_command(label="Exit", command=self.exit)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = App()
app.title("Word2Vec: bilingual")
app.geometry("850x250")
app.mainloop()