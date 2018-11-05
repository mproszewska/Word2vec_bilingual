import tkinter as tk    
from PIL import Image

import SourcesFrame as sf 
import MessageWindow as mw
import MakeGraph as mg

bWords,rWords = list(),list()
def getWords():
    return [bWords,rWords]
class GraphFrame(tk.Frame):

    def addWord(self,color,entry):
        global bWords,rWords
        word = entry.get()
        if word=="": return
        entry.delete(0,tk.END)
        VectorSpace = []
        if color=="blue":   VectorSpace = sf.bVectorSpace
        if color=="red":    VectorSpace = sf.rVectorSpace
        if len(VectorSpace)==0:
            w.MessageWindow(title="Warning", message="No word entered.")
            return
        labels = VectorSpace[0]
        for index in range(len(labels)):
            if labels[index] == word:
                if color=="blue":
                    if index in bWords:
                        mw.MessageWindow(title="Warning",message="This word is already on the list.")
                        return
                    bWords.append(index)
                if color=="red":
                    if index in rWords:
                        mw.MessageWindow(title="Warning",message="This word is already on the list.")
                        return
                    rWords.append(index)
                mw.MessageWindow(title="Graph", message="Word: \""+word+"\" added")
                return
        mw.MessageWindow(title="Warning",message="This word is not in vector space")
        return

    def list(self):
        message = "Blue:\n"
        global bWords,rWords
        if len(sf.bVectorSpace)>0:
            labels = sf.bVectorSpace[0]
            for word_index in bWords:
                try: word_index = int(word_index)
                except: mw.MessageWindow(title="Error", message="Error occurred during reading list.")
                message += (" "+str(labels[word_index])+"\n")
        message += "\nRed:\n"
        if len(sf.bVectorSpace)>0:
            labels = sf.rVectorSpace[0]
            for word_index in rWords:
                try: word_index = int(word_index)
                except: mw.MessageWindow(title="Error", message="Error occurred during reading list.")
                message += (" " + labels[word_index] + "\n")
        mw.MessageWindow(title="Graph: list",message = message[:-1])

    def clear(self):
        global bWords,rWords
        del bWords[:],rWords[:]
        
    def makeGraph(self):
        global bWords, rWords
        bFilename = "png/blue.png"
        rFilename = "png/red.png"
        mg.MakeGraph(bWords,rWords, sf.bVectorSpace,sf.rVectorSpace,bFilename,rFilename)
        bImg = Image.open(bFilename)
        bImg.show()
        rImg = Image.open(rFilename)
        rImg.show()


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #layout
        self.rowconfigure(0,minsize=20)
        self.rowconfigure(2,minsize=40)
        self.columnconfigure(0,minsize=30)
        self.columnconfigure(5,minsize=30)

        bEntry = tk.Entry(self)
        bEntry.grid(row=1,column=1)

        rEntry = tk.Entry(self)
        rEntry.grid(row=1,column=4)

        bAddButton = tk.Button(self,bg="royalblue",text="+", command=lambda: self.addWord("blue",bEntry))
        bAddButton.grid(row=1,column=2)

        rAddButton = tk.Button(self,bg="firebrick",text="+", command = lambda: self.addWord("red",rEntry))
        rAddButton.grid(row=1,column=3)

        graphButton = tk.Button(self,text="graph",width=15, command = self.makeGraph)
        graphButton.grid(row=3,column=1,columnspan=4)

        listButton = tk.Button(self, text="words",width=15, command= self.list)
        listButton.grid(row=3, column=1, columnspan=4,sticky="w")

        listButton = tk.Button(self, text="clear",width=15, command= self.clear)
        listButton.grid(row=3, column=1, columnspan=4,sticky="e")
       
        # Load words from file
        global bWords,rWords
        variables = {}
        variables.update({"bWords": []})
        variables.update({"rWords": []})
        try:
            exec(open("data/words.txt").read(), variables)
            bWords = variables["bWords"]
            rWords = variables["rWords"]
        except:
            bWords,rWords = [],[]