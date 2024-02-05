import tkinter as tk
from tkinter import ttk
from Store import Store
from Templates import ChildFrame
from AppTheme import AppTheme
from LocalDataHandler import readFile

class PopupWarning(tk.Toplevel):
    """Main class to create the pop up"""
    def __init__(self, title: str = "Warning", bodyTxt: str = "you did and oopsie "):
        # Defines root attributes of the popup
        super().__init__()
        self.root = self
        self.root.iconbitmap("assets/images/icons/warning.ico")
        self.title("")
        self.geometry('420x240+1000+500')
        self.configure(background ="white")
        
        # Creates the store, and adds the datahandler and the theme
        self.store = Store()   
        self.store.set("root", self.root)   

        appTheme = AppTheme(styleName="clam", themeName="Light", textSize="Normal")
        self.store.set("appTheme", appTheme)
        self.store.set("theme", appTheme.theme)
        self.store.set("textSize", appTheme.textSize)
        readFile("settings")

        
        self.store.set("title", title)
        self.store.set("bodyTxt", bodyTxt)
 
        # Creates the frame where the app will sit on
        app = App(self)
        
        # Toplevel has no main loop
        
class App(ChildFrame):
    """The main frame where the warning will sit over"""
    def __init__(self, parent: PopupWarning):
        super().__init__(parent)
        self.configure(background="white")
        self.theme = self.store.theme
        self.textSize = self.store.textSize
        
        titleLabel = tk.Label(self, text=self.store.title, foreground="#3387EA", background="white",
                              font=(self.theme.fontTypeFace, self.textSize.popUpWarningHeader, "bold"))
        titleLabel.pack(fill="both", anchor="nw", ipady=10)
        
        bodyTxt = tk.Label(self, text=self.store.bodyTxt, background="white", 
                           font=(self.theme.fontTypeFace, self.textSize.lowerRibbonBtnFont, "normal"), wraplength=400)
        
        bodyTxt.pack(fill="both", anchor="nw", expand=1)
        
        acceptBtn = ttk.Button(self, 
                               style="primaryButton.TButton", 
                               text="Dismiss",
                               takefocus=False,
                               command=self.close)
        acceptBtn.pack(ipady=5, pady=20)
        
        
        self.pack(fill=tk.BOTH, ipadx=10, expand=1)
        
    def close(self):
        self.store.root.destroy()
        
