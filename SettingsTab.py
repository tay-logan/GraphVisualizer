import tkinter as tk
from tkinter import ttk
import os
from PopupWarning import PopupWarning
from Templates import LowerRibbonTab, LowerRibbonGrid, CheckBoxController, ChildFrame
from LocalDataHandler import saveFile, readFile

class SettingsTab(LowerRibbonTab):
    def __init__(self, parent):
        super().__init__(parent)
        # loads in data handler from the store
        self.dataHandler = self.store.dataHandler
        
        # Makes grid to have divisions
        self.grid = LowerRibbonGrid(self)
        
        # Enables divisions for parent class
        self.grid.enableDivisions(padx=10)

        # # Creates a new frame that holds all the things related to the theme settings
        # self.themeSettingsFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        # self.grid.addSection(self.themeSettingsFrame)

        # self.textSize = self.store.textSize
        theme = self.store.theme
        
        # # Creates a title label for the theme settings
        # themeSettingsLabel = tk.Label(self.themeSettingsFrame, 
        #                                 text="Theme", 
        #                                 font=(theme.fontTypeFace, self.textSize.upperRibbonBtnFont, "bold"), 
        #                                 background=self.theme.lowerRibbonBackground)
        # themeSettingsLabel.pack(pady=(6, 0), padx=9, anchor="nw")
        
        # # Creates a new frame for the theme options
        # themeSettingsOptions = ChildFrame(self.themeSettingsFrame, 
        #                                     background=self.theme.lowerRibbonBackground)
        # themeSettingsOptions.pack(padx=(4, 15), pady=8)
        
        # # Creates the controller for the theme options
        # self.themeController = CheckBoxController(self.selectTheme)
        
        # textSizes = ["Light Mode", "Dark Mode"]
        
        # # Adds the two theme options in order
        # for testSize in textSizes:
        #     newTextSize = self.themeController.addCheckBox(themeSettingsOptions, testSize)
        #     newTextSize.pack(anchor="w")
            
        #     # Sets the theme according to the settings
        #     if readFile("settings", ["theme"]) in testSize:
        #         newTextSize.setState(True)      
        
        
        # Creates a new frame that holds all the things related to the text size settings
        self.textSettingsFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.textSettingsFrame)
        
        # Creates a title label for the text size settings
        textSizeSettingsLabel = tk.Label(self.textSettingsFrame, 
                                        text="Text Size", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        textSizeSettingsLabel.pack(pady=(6, 0), padx=9, anchor="nw")
        
        # Creates a new frame for the text size options
        textSettingsOptions = ChildFrame(self.textSettingsFrame, 
                                            background=self.theme.lowerRibbonBackground)
        textSettingsOptions.pack(padx=(4, 15), pady=8)
        
        # Creates the controller for the text size options
        self.textSizeController = CheckBoxController(self.selectTextSize)
        
        textSizes = ["Normal Size", "Large Size"]
        
        # Adds the two text size options in order
        for testSize in textSizes:
            newTextSize = self.textSizeController.addCheckBox(textSettingsOptions, testSize)
            newTextSize.pack(anchor="w")
            
        # Sets the text size according to the settings
            if readFile("settings", ["text_size"]) in testSize:
                newTextSize.setState(True)
                         
    
        # Creates a new frame that holds all the things related to the user guide settings
        self.userGuideFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.userGuideFrame)
        
        # Creates a new frame for the user guide options
        self.userGuideOptions = ChildFrame(self.userGuideFrame, 
                                            background=self.theme.lowerRibbonBackground)
        self.userGuideOptions.pack(padx=(4, 15))
        
        # Creates a title label for the User Guide section
        self.userGuideSettingsLabel = tk.Label(self.userGuideOptions, 
                                        text="User Guide", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        self.userGuideSettingsLabel.pack(pady=(6, 0), padx=9, anchor="nw")

        # Creates a description for the User Guide section
        self.userGuideSettingsLabel = tk.Label(self.userGuideOptions, 
                                        text="Learn how to use Graph Visualizer.", 
                                        font=(theme.fontTypeFace, self.textSize.LowerRibbonSectionHeader, "normal"), 
                                        background=self.theme.lowerRibbonBackground)
        self.userGuideSettingsLabel.pack(pady=(6, 0), padx=9, anchor="nw")

        # Creates a button to show the user guide
        self.clearBtn = ttk.Button(self.userGuideOptions,
                                   text="Show User Guide",
                                   takefocus=False,
                                   style="secondaryButton.TButton",
                                   command=self.openUserGuide)
        self.clearBtn.pack(pady=(6, 0), padx=9, anchor="nw")
        
        
    def selectTheme(self, themeName):
        """Updates the theme of the app, and saves option to the settings file"""
        saveFile("settings", ["theme"], themeName.split()[0])
        self.store.appTheme.changeTheme(f"{themeName.split()[0]}")
        self.store.restartApp()
        
    def selectTextSize(self, textSize):
        """Updates the text size of the app, and saves option to the settings file"""
        saveFile("settings",  ["text_size"], textSize.split()[0])
        self.store.appTheme.changeTextSize(f"{textSize.split()[0]}")
        self.store.restartApp()
        
    def openUserGuide(self):
        """Opens the user guide of the app"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "local/user_guide.pdf")
        try:
            os.startfile(filename)
        except FileNotFoundError:
            # Warns the user that the user guide cant be found
            PopupWarning(bodyTxt="User Guide was not found")
        