import tkinter
from tkinter import ttk
import os

class TreeWindows(tkinter.Frame):
    def __init__(self,master,path,otherWin):
        self.path=os.path.abspath(path)
        frame=tkinter.Frame(master)
        frame.grid(row=0,column=0,padx=15, pady=15)
        self.otherWin = otherWin
        self.tree=ttk.Treeview(frame)
        self.tree.pack(side=tkinter.LEFT,fill=tkinter.Y)

        root = self.tree.insert("", "end", text=self.getLastPath(self.path), open=True, values=(self.path))
        self.loadTrea(root,self.path)

        self.sy=tkinter.Scrollbar(frame)
        self.sy.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.sy.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.sy.set)

        self.tree.bind("<<TreeviewSelect>>",self.func)
    def func(self,event):
        self.v=event.widget.selection()
        for sv in self.v:
            file=self.tree.item(sv)["text"]
            print(file)
            self.otherWin.ev.set(file)



    def loadTrea(self,parent,parent_path):
        for file_name in os.listdir(parent_path):
            abs_path=os.path.join(parent_path,file_name)
            treey=self.tree.insert(parent,"end",text=self.getLastPath(abs_path),values=(abs_path))
            if os.path.isdir(abs_path):
                self.loadTrea(treey,abs_path)

    def getLastPath(self,path):
        pathList=os.path.split(path)
        return pathList[-1]