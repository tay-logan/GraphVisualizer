import tkinter as tk
from tkinter import ttk
from Utils import cloneWidget, defocus, deleteLines

class ChildFrame(tk.Frame):
    """
    Template Frame that passes relavent information from parent to child
    """
    def __init__(self, parent, **kw):
        super().__init__(master=parent, **kw)
        self.store = parent.store
        
class ScrollableRegion:
    """
    Used to make a region where anything can be added and it creates
    a scroll bar when the space runs out
    """
    def __init__(self, parent) -> None:
        # Creates a text widget, where the rows will be on
        self.container = tk.Text(parent, height=100, state="disabled")
        self.container.pack(side="left", fill="both", expand=True)
        
        # Creates a scrollbar used to scroll through the rows
        self.scrollbar = tk.Scrollbar(parent, command=self.container.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # links the text widget to the scroll bar
        self.container.configure(yscrollcommand=self.scrollbar.set)
        self.container.configure(cursor="", takefocus=False)
        
        self.rows = []
        
    def setBackground(self, color: str):
        """
        Sets the background of the custom scroll region global backround
        """
        self.container.configure(background=color, selectbackground=color)
        
    def addRow(self) -> tk.Frame:
        """
        Creates a new row in the scrollable region, and returns the frame
        where the child widget can be added
        """
        
        # Sets the state to normal to allow for a new row to be added
        self.container.configure(state="normal")
        
        # Creates a new frame to be added to the row
        newFrame = tk.Frame(self.container)
        self.rows.append(newFrame)

        # Adds the frame to the text widget as a new window
        self.container.window_create("end", window=newFrame)
        self.container.insert("end", "\n")
        
        # Sets the state to disabled, to prevent user input and
        # preserve desired behavior
        self.container.configure(state="disabled")
        
        # returns the frame where the child widget can be added
        return newFrame
        
    def deleteRows(self, start: int = 0, end: int = -1, inc: int = 1) -> None:
        """
        Deletes the specified row(s) from the scrollable region
        """
        if end == -1:
            end = len(self.rows)

        # loops through each row, and deletes them one at a time
        delCount = 0
        for i in range(start, end, inc):
            deleteLines(self.container, i-delCount)
            delCount += 1
            
    def deleteRow(self, index: int):
        deleteLines(self.container, index)
        
class OptionsBox(ttk.Combobox):
    """
    Creates a custom combo box and passes in selected command and command to follow
    """
    def __init__(self, parent, defaultTxt, selectedCommand, **kw) -> None:
        super().__init__(master=parent, **kw)
        
        self.set(defaultTxt)
        self.bind("<<ComboboxSelected>>", selectedCommand)
        self.bind("<FocusIn>", defocus)

class LowerRibbonTab(ChildFrame):
    """Lower Ribbon Template"""
    def __init__(self, parent):
        super().__init__(parent)
        self.theme = self.store.theme
        self.textSize = self.store.textSize
        
        self.configure(background=self.theme.lowerRibbonBackground)
        
    def show(self) -> None:
        """Packs the lower ribbon"""
        self.pack(side='top', anchor="nw", fill="both", expand=1)
        
    def hide(self) -> None:
        """pack_forget the lower ribbon"""
        self.pack_forget()

class UpperRibbonTab(ChildFrame):
    """Lower Ribbon Template"""
    def __init__(self, parent, tabName):
        super().__init__(parent)
        self.theme = self.store.get("theme")
        self.tabName = tabName     

        self.configure(background=self.theme.upperRibbonUnselectedBtn)
        
        # The buton that selects the tab
        self.button = ttk.Button(self, 
                                text=self.tabName, 
                                command=self.selectTab,
                                takefocus=0, 
                                style="upper_ribbon_unselected.TButton")
        self.button.bind("<Enter>", self._hover_on)
        self.button.bind("<Leave>", self._hover_off)
        self.button.pack(fill="both", padx=(0, 1), ipady=2, ipadx=11)
            
        # Creates the selection frame that shows that the tab is selected
        self.selectionFrame = tk.Frame(self, background=self.theme.upperRibbonBackground, height=2)
        self.selectionFrame.pack(fill="both", padx=(0, 1))
        
        # Places the tab button in its place on the upper ribbon
        tabNum = list(self.master.upperRibbonBtns.keys()).index(tabName)
        self.grid(column=tabNum, row=0)
        
        
    def _hover_on(self, e):
        """Hover over behavior to change colors"""
        selectedTab = self.master.selectedTab
        selectedTab.selectionFrame.configure(background=self.theme.upperRibbonBackground)
        self.selectionFrame.configure(background=self.theme.ribbonSelectedBtn)
        
    def _hover_off(self, e):
        """Hover over behavior to change back colors"""
        selectedTab = self.master.selectedTab
        self.selectionFrame.configure(background=self.theme.upperRibbonBackground)
        selectedTab.selectionFrame.configure(background=self.theme.ribbonSelectedBtn)
        
    def _deselect(self):
        self.selectionFrame.configure(background=self.theme.upperRibbonBackground)
        self.button.configure(style="upper_ribbon_unselected.TButton")
        
    def selectTab(self) -> None:
        """Selection callback"""
        
        selectedTab = self.master.selectedTab
        
        # Checks if its the first time a tab is selected
        if selectedTab is not None:
            # Prevents a tab from being selected twice in a row
            if selectedTab.tabName != self.tabName:
                # deselects the old selected tab
                selectedTab._deselect()
            else:
                return

        # Updates the select tab from the upper ribbon obj
        # and changes display to show its been selected
        self.master.selectedTab = self
        self.selectionFrame.configure(background=self.theme.ribbonSelectedBtn)
        self.button.configure(style="upper_ribbon_selected.TButton")
        
        return self.store.updateLowerRibbon(self.tabName)

class LowerRibbonGrid(ChildFrame):
    """Lower Ribbon Template"""
    def __init__(self, parent):
        super().__init__(parent)
        self.theme = self.store.get("theme")
        self.configure(background=self.theme.lowerRibbonBackground)
        
        self.addDivisions = False
        self.sectionCount = 0
        
        
        self.pack(side='top', anchor="nw", fill="both", expand=1)
        
    def enableDivisions(self, **gridkw):
        """Divisions are black lines between sections"""
        self.addDivisions = True
        
        self._divisorGridkw = gridkw | {"pady": 9}
    
    def addSection(self, widget: tk.Widget, **kw) -> tk.Frame:
        """Creates a new section and returns a frame to place child widgets"""
        column = self.sectionCount
        
        # Adds a section division if its enabled
        if self.addDivisions and self.sectionCount != 0:
            column = self.sectionCount * 2 - 1
            divisorClone = self.getNewDivision()
            divisorClone.grid(row=0, 
                            column=column,
                            **self._divisorGridkw)

            column += 1
            
        widget.grid(row=0, column=column, **kw)
        self.sectionCount += 1
    
    def getNewDivision(self) -> tk.Frame:
        return tk.Frame(self, height=95, background=self.theme.lowerRibbonTextColor)
    
class NamedCheckBox(ChildFrame):
    """Named Check Button Template"""
    def __init__(self, parent, text, selectCallback, **kw):
        super().__init__(parent, **kw)
        self.theme = self.store.theme
        self.textSize = self.store.textSize
        self.configure(background=self.theme.lowerRibbonBackground)
        self.name = text
        self.selectCallback = selectCallback
        self._selected = False
        
        # dict to hold the two checkbox button images
        self.checkboxImgs = {"Empty Square" : tk.PhotoImage(file='assets/images/buttons/Empty Checkbox.png'), 
                           "Filled Square" : tk.PhotoImage(file='assets/images/buttons/Selected Checkbox.png')}
        
        # Button that detects the selection
        self.button = ttk.Button(self, 
                                 image=self.checkboxImgs["Empty Square"],
                                 takefocus=False,
                                 style="settings_tab_checkbox_button.TButton",
                                 command=self.selectAction)
        self.button.grid(row=0, column=0)
        
        # Label that has the name of the checkbox
        self.label = tk.Label(self, 
                              text=self.name,
                              font=(self.theme.fontTypeFace, 
                                    self.textSize.lowerRibbonNamedCheckboxLabel, 
                                    "normal"),
                              background=self.theme.lowerRibbonBackground)
        self.label.grid(row=0, column=1)
            
    
    def selectAction(self):
        """only does callback if its not currently selected"""
        if not self._selected:            
            self.selectCallback(self.name)
    
    def setState(self, state: bool):         
        """Sets the selected state of the button"""  
        self._selected = state
        
        # Updates the image of the checkbox
        img = self.checkboxImgs["Filled Square" if state else "Empty Square"]
        self.button.configure(image=img)
        self.button.img = img
        
class CheckBoxController():
    """Controller to handler selection behavior of a group of checkboxes"""
    def __init__(self, selectedCallback) -> None:
        # Holds the currently selected checkbox
        self.selected = None
        
        # Saves gthe selected callback to update parent
        self.selectedCallback = selectedCallback
        
        # List of all managed checkboxes
        self.checkBoxes = []
        
    def addCheckBox(self, parent, text) -> NamedCheckBox:
        """Creates a new checkbox"""
        newCheckBox = NamedCheckBox(parent, text, self.select)

        # Adds the new check box to the list
        self.checkBoxes.append(newCheckBox)
        
        # Returns the check box for further customization
        return newCheckBox
    
    # Updates all checkbox visuals to show updates,
    # onces a check box has seen selected
    def select(self, selectedName):
        for checkBox in self.checkBoxes:
            if checkBox.name == selectedName:
                checkBox.setState(True)
            else:
                checkBox.setState(False)
        
        self.selected = selectedName
        self.selectedCallback(selectedName)   
    
        