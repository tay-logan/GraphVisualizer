import tkinter as tk
from tkinter import ttk
from HomeTab import HomeTab
from GraphTab import GraphTab
from FilterTab import FilterTab
from AnalyticsTab import AnalyticsTab
from SettingsTab import SettingsTab
from Templates import UpperRibbonTab, ChildFrame



class UpperRibbon(ChildFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.theme = self.store.get("theme")
        self.configure(background=self.theme.upperRibbonBackground)
        
        self.selectedTab = None
        
        self.upperRibbonBtns = {"Home": None, 
                                "Graph": None, 
                                "Filter": None, 
                                "Analysis": None, 
                                "Settings": None}

        for tabName in self.upperRibbonBtns.keys():
            newTab = UpperRibbonTab(self, tabName)

            self.upperRibbonBtns[tabName] = newTab
            
        self.pack(anchor="nw", fill="both")
        
    def _selectBtn(self, name):
        self.upperRibbonBtns[name].selectTab()
        
             
class LowerRibbon(ChildFrame):
    def __init__(self, parent: ChildFrame):
        super().__init__(parent)
        # self.parent = parent
        self.curTab = None
        
        self.lowerRibbonTabs = {}
        self.lowerRibbonTabs["Home"] = HomeTab(self)
        self.lowerRibbonTabs["Graph"] = GraphTab(self)
        self.lowerRibbonTabs["Filter"] = FilterTab(self)
        self.lowerRibbonTabs["Analysis"] = AnalyticsTab(self)
        self.lowerRibbonTabs["Settings"] = SettingsTab(self)  
        
        self.pack(anchor="nw", fill="both")
                
        self.store.set("updateLowerRibbon", self.update)

    def update(self, newTabName) -> None:
        if self.curTab is not None:
            self.curTab.hide()
            
        self.curTab = self.lowerRibbonTabs[newTabName]
        self.curTab.show()
    
class Ribbon(ChildFrame):
    def __init__(self, parent: ChildFrame):
        super().__init__(parent)
        self.pack(side='top', anchor="nw")
        
        
        self.upperRibbon = UpperRibbon(parent)
        
        self.lowerRibbon = LowerRibbon(parent)
        
        self.upperRibbon._selectBtn("Home")
        
    def update_lower_ribbon(self, newTabName) -> None:
        self.lowerRibbon.update(newTabName)
        

        