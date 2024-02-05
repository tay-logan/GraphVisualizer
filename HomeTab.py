import tkinter as tk
from tkinter import ttk
from Templates import LowerRibbonTab
from PopupWarning import PopupWarning
from Utils import getFolderPath, NoneSelected
from LocalDataHandler import *

class ImportPopup(tk.Toplevel):
    """Main class to create the import pop up"""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.store = parent.store
        var = tk.StringVar()

        self.appFrame = tk.Frame(self)
        self.grid_columnconfigure(0,weight=1)
        self.folderPathList = []

        if self.store.textSize.name == "Normal":
            self.geometry("600x250+500+300")
        else:
            self.geometry("600x275+500+300")
            
        
        self.title("")
        self.configure(background="white")
        self.appFrame.configure(background="white")
        theme = self.store.theme
        self.textSize = self.store.textSize

        titleLabel = tk.Label(self, text="Import Data", foreground="#3387EA", background="white",
                                font=(theme.fontTypeFace, self.textSize.popUpWarningHeader, "bold"))
        titleLabel.grid(row = 0, column = 0, sticky= "W", pady = 2, padx=5)

        label2 = tk.Label(self, text="Selected:", foreground="grey", background="white",
                                font=(theme.fontTypeFace, self.textSize.LowerRibbonSectionHeader, "bold"))
        label2.grid(row = 2, column = 0, sticky= "W", pady = 5, padx=5)

        self.select_folderBtn = ttk.Button(self, text="Select Folder", style = "secondaryButtonGray.TButton", command =self.selectFolderButton)
        self.select_folderBtn.grid(row = 1, column = 0, sticky = "W", pady = 5, padx = 5)

        self.close_folderBtn = ttk.Button(self, text="Cancel", style = "secondaryButtonGray.TButton", command = self.destroy)
        self.close_folderBtn.grid(row = 10, column = 3, sticky = "SE", pady = 100, padx = 10)

        self.import_folderBtn = ttk.Button(self, style = "primaryButton.TButton", text="Import", command=self.importBtnCallback)
        self.import_folderBtn.grid(row = 10, column = 4, sticky = "SE", pady = 100, padx = 10)        
        
        # self.pack(fill=tk.BOTH, ipadx=10, expand=1)
        
    def selectFolderButton(self):
        try:
            newFolder = getFolderPath()
        except NoneSelected:
            tk.messagebox.showwarning(title="Warning", message="Please select a folder that contains valid participant data.")
        else:
            self.folderPathList.append(newFolder)
            
            newRow = len(self.folderPathList) - 1

            folderlabel = tk.Label(self.appFrame, text=newFolder, foreground="grey", background="white",
                            font=(self.store.theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "bold"))
            folderlabel.grid(row=newRow, column=0, pady=2)

            self.appFrame.place(x=10, y= 100)
        finally:
            self.select_folderBtn.focus_set()
            
        
    def importBtnCallback(self):
        dataHandler = self.store.dataHandler
        
        fileCount = 0
        for folder in self.folderPathList:
            fileCount += dataHandler.importFromFolder(folder)
            
        dataHandler.updateDataHandler()
        self.parent.updateLabels()
       
        self.destroy()
        
        if fileCount == 0:
            tk.messagebox.showwarning(title="Warning", message="Please select a folder that contains valid participant data.")

        else:
            print("New Data Imported!\n")
              

class HomeTab(LowerRibbonTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(height=113, width=1350)

        self.importImgs = {"Gray Plus" : tk.PhotoImage(file='assets/images/buttons/Gray Plus.png'), 
                           "Blue Plus" : tk.PhotoImage(file='assets/images/buttons/Blue Plus.png')}
        self.importBtn = ttk.Button(self, 
                               text="Import Data",
                               compound="top",
                               image=self.importImgs["Gray Plus"], 
                               takefocus=False, 
                               command= lambda: ImportPopup(self),
                               style="lower_ribbon_unselected.TButton")
        self.importBtn.img = self.importImgs["Gray Plus"] # this is psychotic
        self.importBtn.pack(anchor="nw", padx=24, pady=24, ipadx=4, ipady=12, side="left")  
        
        self.importBtn.bind("<Enter>", self.hover_on_plus)
        self.importBtn.bind("<Leave>", self.hover_off_plus)

        self.clearImgs = {"Gray Minus" : tk.PhotoImage(file='assets/images/buttons/Gray Minus.png'), 
                           "Blue Minus" : tk.PhotoImage(file='assets/images/buttons/Blue Minus.png')}
        self.clearBtn = ttk.Button(self, 
                               text="Clear Data",
                               compound="top",
                               image=self.clearImgs["Gray Minus"], 
                               takefocus=False, 
                               command=self.hideGraps,
                               style="lower_ribbon_unselected.TButton")
        self.clearBtn.img = self.clearImgs["Gray Minus"] # this is psychotic
        self.clearBtn.pack(anchor="nw", padx=24, pady=24, ipadx=4, ipady=12, side = 'left')  
        
        self.clearBtn.bind("<Enter>", self.hover_on_minus)
        self.clearBtn.bind("<Leave>", self.hover_off_minus)
        
        filesframe = tk.Frame(self, background=self.theme.lowerRibbonBackground)
        filesframe.place(x=400, y= 5)
        
        self.recentLabel = tk.Label(filesframe, text="Recently Uploaded Files:", background=self.theme.lowerRibbonBackground,
                              font=(self.theme.fontTypeFace, 
                                    self.textSize.LowerRibbonSectionHeader, 
                                    "bold"))
        self.recentLabel.grid(row=0, column= 0, sticky= "w", pady =0, padx = 10, columnspan=2)
        self.fileImg = tk.PhotoImage(file='assets/images/buttons/File Img.png')
        
        row = [1, 2, 1, 2, 1, 2]
        col = [0, 0, 1, 1, 2, 2]
        
        self.recentFileBtns = []
        for i in range(6):
            fileBtn = ttk.Button(filesframe, 
                                text="-----",
                                compound="left",
                                image=self.fileImg,
                                takefocus=False, 
                                style="recent_files.TButton",
                                command = lambda x = i: self.openPrevFile(x))
            fileBtn.grid(row = row[i], column= col[i], sticky="w", pady=5, padx=10)
            
            self.recentFileBtns.append(fileBtn)
                     
    def hover_on_plus(self, e):
        self.importBtn.configure(image=self.importImgs["Blue Plus"])
        self.importBtn.img = self.importImgs["Blue Plus"]
        
    def hover_off_plus(self, e):
        self.importBtn.configure(image=self.importImgs["Gray Plus"])
        self.importBtn.img = self.importImgs["Gray Plus"]

    def hover_on_minus(self, e):
        self.clearBtn.configure(image=self.clearImgs["Blue Minus"])
        self.clearBtn.img = self.clearImgs["Blue Minus"]
        
    def hover_off_minus(self, e):
        self.clearBtn.configure(image=self.clearImgs["Gray Minus"])
        self.clearBtn.img = self.clearImgs["Gray Minus"]
   
    def show(self) -> None:
        super().show()
        self.updateLabels()
    
    def hideGraps(self):
        if tk.messagebox.askyesno(title="Clear Data?", message="Are you sure you want to clear the data?"):
            dataHandler = self.store.dataHandler
            dataHandler.deleteAllGraphs()
            dataHandler.clearData()
            dataHandler.updateDataHandler()  
            

    def openPrevFile(self, i):
        dataHandler = self.store.dataHandler

        files = readFile("imports")[::-1]

        if i < len(files):
            file = files[i]
            dataHandler.importFromFile(file)
            dataHandler.updateDataHandler()
                
    def updateLabels(self):
        file_list = readFile("imports")[::-1]
        
        fileNames = ["-----                       "] * 6
        
        for i, file in enumerate(file_list[:6]):
            participantID = file.replace("\\", "/").split("/")[-2]
            date = file.replace("\\", "/").split("/")[-3]
            
            fileNames[i] = participantID + "-" + date
    
        for i in range(6):
            self.recentFileBtns[i].config(text=fileNames[i])        