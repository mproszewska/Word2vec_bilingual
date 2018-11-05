import tkinter as tk
    
import GraphFrame as gf
import SourcesFrame as sf

class WordsFrame(tk.Frame):
    def search(self,color,entry,text):
        word = entry.get()
        labels = []
        if color=="blue":
            if len(sf.bVectorSpace)==0: return
            labels = sf.bVectorSpace[0][1:]
        if color=="red":
            if len(sf.rVectorSpace)==0: return
            labels = sf.rVectorSpace[0][1:]
        if len(labels)==0: return
        text.delete('1.0',tk.END)
        for l in labels:
            if l[0:len(word)]==word:
                text.insert(tk.END,l+"\n")

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.rowconfigure(0, minsize=20)
        self.columnconfigure(0, minsize=40)
        self.columnconfigure(5, minsize=40)

        bEntry = tk.Entry(self)
        bEntry.grid(row=1, column=1)

        rEntry = tk.Entry(self)
        rEntry.grid(row=1, column=4)

        bScrollbar = tk.Scrollbar(self)
        bText = tk.Text(self,width=21,height=5)
       # bText.config(state=tk.DISABLED)

        bText.focus_set()
        bScrollbar.grid(row=3,column=1)
        bText.grid(row=3,column=1)
        bScrollbar.config(command=bText.yview)
        bText.config(yscrollcommand=bScrollbar.set)

        rScrollbar = tk.Scrollbar(self)
        rText = tk.Text(self, width=21, height=5)
       # rText.config(state=tk.DISABLED)

        rText.focus_set()
        rScrollbar.grid(row=3, column=4)
        rText.grid(row=3, column=4)
        rScrollbar.config(command=rText.yview)
        rText.config(yscrollcommand=rScrollbar.set)

        bAddButton = tk.Button(self, bg="royalblue", text="?", command=lambda: self.search("blue",bEntry,bText))
        bAddButton.grid(row=1, column=2)

        rAddButton = tk.Button(self, bg="firebrick", text="?", command=lambda: self.search("red",rEntry,rText))
        rAddButton.grid(row=1, column=3)
