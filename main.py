import tkinter as tk
from tkinter import ttk
from Templates import ChildFrame
from Store import Store
from Ribbon import Ribbon
from AppTheme import AppTheme
from Body import Body
from DataHandler import DataHandler
from LocalDataHandler import readFile

class Main(tk.Tk):
    """Main class to create the root of the app"""
    def __init__(self):
        # Defines root attributes
        super().__init__()
        self.root = self
        self.title("Graph Visualizer")
        self.geometry('1920x1080')
        self.resizable(True, True)
        self.configure(background ="white")
        
        # Creates the store, and adds the datahandler and the theme
        self.store = Store()
        self.store.set("restartApp", self.restartApp)
        self.store.set("dataHandler", DataHandler(self.store))       
        
        appTheme = AppTheme(styleName="clam", themeName=readFile("settings", ["theme"]), textSize=readFile("settings", ["text_size"]))
        self.store.set("appTheme", appTheme)
        self.store.set("theme", appTheme.theme)
        self.store.set("textSize", appTheme.textSize)
        
        # Validates imports and settings file
        readFile("imports")
        readFile("settings") 
        
        # Creates the frame where the app will sit on      
        self.app = App(self)
        self.app.rowconfigure(0, weight=1)
        self.app.columnconfigure(0, weight=1)        
        self.mainloop()
    
    def restartApp(self):
        self.app.destroy()
        if tk.messagebox.showwarning(title="App restarting", message="The app will close, please reopen it"):
            self.destroy()
        
class App(ChildFrame):
    """The main frame where everything will sit over"""
    def __init__(self, parent: Main):
        super().__init__(parent)
        
        # Creates the ribbon and the body of the app
        self.ribbon = Ribbon(self)
        self.body = Body(self)
        
        self.pack(fill=tk.BOTH, ipadx=10)

if __name__ == '__main__':
    app = Main()