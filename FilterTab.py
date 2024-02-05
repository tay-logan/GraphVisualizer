import tkinter as tk
from tkinter import ttk
from Templates import LowerRibbonTab, CheckBoxController, LowerRibbonGrid, ChildFrame
from PIL import ImageTk
from PIL import Image
from FilterPopup import FilterPopup
from LocalDataHandler import saveFile, readFile

class FilterChip(ChildFrame):
    def __init__(self, parent: tk.Widget, filter, deleteCallback, count):
        super().__init__(parent)
        theme = self.store.theme
        textSize = self.store.textSize
        self.filter = filter
        self.deleteCallback = deleteCallback    
        
        row = count % 2
        col = count // 2
        self.outerFrame = ChildFrame(parent, background="white")
        self.outerFrame.grid(row=row, column=col, padx=8, pady=3)
        
        self.filterText = tk.Label(self.outerFrame,
                                   text=str(filter),
                                   font=(theme.fontTypeFace, 
                                         textSize.lowerRibbonTextWidget, 
                                         "normal"),
                                   background="white",
                                   foreground="#3387EA")
        self.filterText.grid(row=0, column=0)
        
        closeImg = tk.PhotoImage(file='assets/images/buttons/Red X.png')
        self.deleteBtn = ttk.Button(self.outerFrame,
                                    image=closeImg,
                                    takefocus=False,
                                    style="fliter_chips.TButton",
                                    command=self.close)
        self.deleteBtn.img = closeImg # this is still psychotic
        self.deleteBtn.grid(row=0, column=1)
        
    def close(self):
        self.outerFrame.destroy()
        self.deleteCallback(self.filter.filterID)
            

class FilterTab(LowerRibbonTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(height=113, width=1350)
        
        # loads in data handler from the store
        self.dataHandler = self.store.dataHandler
        
        self.filters = []
        
        self.store.dataHandler.register_data_update_callback(self.updateFilterList)
        
        # Makes grid to have divisions
        self.grid = LowerRibbonGrid(self)
        
        # Enables divisions for parent class
        self.grid.enableDivisions(padx=10)
        
        # Creates a new frame that holds all the things related to the timezome settings
        self.timezoneSettingsFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.timezoneSettingsFrame)

        timeZoneLabel = tk.Label(self.timezoneSettingsFrame, 
                            text="Time Zone", 
                            font=(self.theme.fontTypeFace, 
                                self.textSize.LowerRibbonSectionHeader, 
                                "bold"), 
                            background=self.theme.lowerRibbonBackground)
        timeZoneLabel.pack(pady=(6, 0), padx=9, anchor="nw")
        
        # Creates a new frame for the timezone options
        timezoneSettingsOptions = ChildFrame(self.timezoneSettingsFrame, 
                                            background=self.theme.lowerRibbonBackground)
        timezoneSettingsOptions.pack(pady=8)
        
        self.timezoneController = CheckBoxController(self.updateTimezone)
        timezomes = ["Local Time", "UTC Time"]

        for timezone in timezomes:
            newTimezone = self.timezoneController.addCheckBox(timezoneSettingsOptions, timezone)
            newTimezone.pack(anchor="w")
        
            # Sets the text size according to the settings
            if readFile("settings", ["time"]) in timezone:
                newTimezone.setState(True)      
        
        self.filtersFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.filtersFrame)
        
        filterLabel = tk.Label(self.filtersFrame, 
                               text="Filters", 
                               font=(self.theme.fontTypeFace, 
                                    self.textSize.LowerRibbonSectionHeader, 
                                    "bold"), 
                               background=self.theme.lowerRibbonBackground)
        filterLabel.pack(pady=(8, 0), padx=9, anchor="nw")
        
        self.filtersList = ChildFrame(self.filtersFrame, 
                                            background=self.theme.lowerRibbonBackground)
        self.filtersList.pack(pady=8)

        
        filtersOptions = ChildFrame(self.filtersFrame, 
                                            background=self.theme.lowerRibbonBackground)
        filtersOptions.pack(pady=(0, 8), fill="x", anchor="w")

        self.clearBtn = ttk.Button(filtersOptions, text="Clear", takefocus=False, command=self.clearFilters, style="secondaryButton.TButton", width=7)
        self.clearBtn.grid(row = 0, column = 0, sticky = 'W', padx = 10)

        self.addBtn = ttk.Button(filtersOptions, text="Add", takefocus=False, command=self.addFilters, style="primaryButton.TButton", width=7)
        self.addBtn.grid(row = 0, column = 1, sticky = 'W', padx = 10)
        
    def updateTimezone(self, timezone):
        """Updates the time zone of the app, and saves the option to the settings file"""
        newTimezone = timezone.split()[0]
        saveFile("settings", ["time"], newTimezone)
        self.store.dataHandler.changeTimezone(newTimezone)

        
    def updateFilterList(self):
        filters = self.dataHandler.getAllFilters()
        for i, filter in enumerate(filters):
            if filter.chipDisplay is not None:
                filter.chipDisplay.outerFrame.destroy()
                
            filter.chipDisplay = FilterChip(self.filtersList, 
                                            filter, 
                                            self.dataHandler.deleteFilter,
                                            i)
            
    def clearFilters(self):
        self.dataHandler.deleteAllFilters()

    def addFilters(self):
        FilterPopup(self.store)