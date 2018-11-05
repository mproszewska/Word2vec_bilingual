import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
from shutil import copyfile
from pathlib import Path

import GraphFrame as gf
import Word2Vec as wv
import MessageWindow as mw

bVectorSpace, rVectorSpace = [],[]
up_to_date = True
unsaved_files = []
class SourcesFrame(tk.Frame):

    def reload(self):
        def yes():
            try:
                global bVectorSpace, rVectorSpace, up_to_date
                if up_to_date: return
                bVectorSpace,rVectorSpace = wv.start()
            except Exception as e:
                mw.MessageWindow("Error", "Error occurred during generating vector spaces"+str(e))
                return
            mw.MessageWindow("Reload", "Vector spaces are up-to-date.")
            up_to_date = True
            del gf.bWords[:],gf.rWords[:]

        mw.YesNoWindow(title="Clear", message="Vector spaces will be generated.\nIt may take some time.", yes=yes)

    def list(self):
        # List of files in folder sources
        message = "Blue:\n"
        files = [f for f in os.listdir("sources/blue")]
        for f in files:
            message += (" "+f+"\n")
        message += "\nRed:\n"
        files = [f for f in os.listdir("sources/red")]
        for f in files:
            message += (" " + f + "\n")
        global up_to_date
        if not up_to_date: message+="\nVector spaces are not up-to-date.\n"
        mw.MessageWindow("List",message[:-1])

    def clear(self):
        def yes():
            files = [f for f in os.listdir("data")]
            for f in files:
                os.remove("data/" + f)
            files = [f for f in os.listdir("sources/blue")]
            for f in files:
                os.remove("sources/blue/"+f)
            files = [f for f in os.listdir("sources/red")]
            for f in files:
                os.remove("sources/red/"+f)
            mw.MessageWindow("Clear", "Files removed")
            global up_to_date,bVectorSpace,rVectorSpace
            up_to_date,bVectorSpace,rVectorSpace = True,[],[]
            del gf.bWords[:],gf.rWords[:]

        mw.YesNoWindow(title="Clear",message="All sources will be deleted.",yes=yes)

    last_dir = os.path.expanduser('~')
    def chooseFile(self,text):

        tk.Tk().withdraw()
        try:
            filename = askopenfilename(initialdir=self.last_dir)
        except:
            mw.MessageWindow(title="Error",message="Can't open home directory")
            return
        try:
            text['text']=filename
        except: return
        self.last_dir = filename[0:filename.rfind('/')]

    def addFile(selfself,color,text):
        filename = text['text']
        if filename=="":
            mw.MessageWindow(title="Warning", message="Select file.")
            return
        name = filename[filename.rfind('/') + 1:]
        try:
            new_name = "sources/" + color + "/" + name
            copyfile(filename, new_name)
            global unsaved_files
            unsaved_files.append(new_name)
        except:
            mw.MessageWindow(title="Error", message="Can't copy selected file.")
        text['text']=""
        mw.MessageWindow(title="Sources", message="File added.")
        global up_to_date
        up_to_date = False

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #layout
        self.rowconfigure(0,minsize=20)
        self.rowconfigure(3,minsize=20)

        bChooseFileButton = tk.Button(self,width=45, height=1,bg="white", anchor="w", command = lambda: self.chooseFile(bChooseFileButton))
        bChooseFileButton.grid(row=1,column=1,columnspan=3)

        rChooseFileButton = tk.Button(self,width=45, heigh=1, bg="white", anchor="w",command = lambda: self.chooseFile(rChooseFileButton))
        rChooseFileButton.grid(row=2,column=1,columnspan=3)

        bAddButton = tk.Button(self, bg="royalblue", text="+", command = lambda: self.addFile("blue",bChooseFileButton))
        bAddButton.grid(row=1, column=4)

        rAddButton = tk.Button(self, bg="firebrick", text="+", command = lambda: self.addFile("red",rChooseFileButton))
        rAddButton.grid(row=2, column=4)

        listButton = tk.Button(self,text="List",width=15, command = self.list)
        listButton.grid(row=4,column=1,columnspan=4)

        clearButton = tk.Button(self, text="Clear",width=15, command = self.clear)
        clearButton.grid(row=4, column=1,columnspan=4,sticky="e")

        realoadButton = tk.Button(self, text="Reload",width=15,command=self.reload)
        realoadButton.grid(row=4, column=1,columnspan=4,sticky="w")

        # Load vector spaces from file
        global bVectorSpace,rVectorSpace
        variables = {}
        variables.update({"bVectorSpace": [None]*3})
        variables.update({"rVectorSpace": [None]*3})
        try:
            exec(open("data/vectorspaces.py").read(), variables)
            bVectorSpace = variables["bVectorSpace"]
            rVectorSpace = variables["rVectorSpace"]
        except:
            bVectorSpace,rVectorSpace = [],[]

def getVectorSpace(color):
    if color=="blue": return bVectorSpace
    if color=="red": return rVectorSpace
    raise Exception

def getUnsavedFiles():
    return unsaved_files