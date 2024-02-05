
import tkinter as tk
from tkinter import ttk
from Store import Store
from Templates import ChildFrame
from AppTheme import AppTheme
from PopupWarning import PopupWarning

class FilterPopup(tk.Toplevel):
    def __init__(self, store):
        super().__init__()
        self.root = self
        self.root.iconbitmap("assets/images/icons/warning.ico")
        self.geometry('600x150+500+300')
        self.configure(background ="white")

        # Creates a store, with the old store copied over
        self.store = store

        app = App(self)

    def resizeWindow(self, x, y):
        self.geometry(f'{x}x{y}+500+300')

class App(ChildFrame):
    def __init__(self, parent: FilterPopup):
        super().__init__(parent)
        self.configure(background="white")
        self.pack(fill=tk.BOTH, ipadx=10, expand=1)
        
        theme = self.store.theme
        textSize = self.store.textSize

        self.filterList = []

        titleLabel = tk.Label(self, text="Add Filters", 
                              foreground="#3387EA", 
                              background="white",
                              font=(theme.fontTypeFace, textSize.popUpWarningHeader, "bold"))
        titleLabel.grid(row=0, column=0, sticky='W', padx=10, pady=10)

        self.feature_dropdown = []
        self.comparator_dropdown = []
        self.value_entries = []

        self.comparatorValues = ["==", "!=" , ">", "<", ">=", "<="]
        self.featureValues = ['Acc magnitude avg', 
                              'Eda avg', 'Temp avg', 
                              'Movement intensity', 
                              'Steps count', 
                              'Rest', 
                              'On Wrist']

        self.addBtn = ttk.Button(self, 
                                 text="+", 
                                 takefocus=False, 
                                 style="addButton.TButton", 
                                 command=self.addRow, width=3)
        self.addBtn.grid(row=2, column=0, sticky='W', padx=10, pady=10)
        
        self.cancelBtn = ttk.Button(self, 
                            text="Cancel", 
                            takefocus=False, 
                            style="secondaryButton.TButton", 
                            width=7, 
                            command=self.close)
        self.cancelBtn.grid(row=4, column=2, sticky='W', padx=10)

        self.applyBtn = ttk.Button(self, 
                                   text="Apply", 
                                   takefocus=False, 
                                   style="primaryButton.TButton", 
                                   command=self.applyFilters, 
                                   width=7)
        self.applyBtn.grid(row=4, column=3, sticky='W', padx=10)

        self.addRow()


    def close(self):
        self.master.destroy()

    def addRow(self):
        textSize = self.store.textSize
        if len(self.feature_dropdown) == 20:
            self.addBtn.configure(state="disabled")
            return
        
        theme = self.store.theme
        index = len(self.feature_dropdown) + 1
        
        self.feature_dropdown.append(ttk.Combobox(self, 
                                                  font=(theme.fontTypeFace, textSize.upperRibbonBtnFont, "normal"), 
                                                  style='Custom.TCombobox', 
                                                  state='readonly', 
                                                  values=self.featureValues))
        self.feature_dropdown[-1].config(width=20)
        self.feature_dropdown[-1].set("Choose a Feature")
        self.feature_dropdown[-1].grid(row=index, column=0, sticky='W', padx=10, pady=10)

        self.comparator_dropdown.append(ttk.Combobox(self, 
                                                     font=(theme.fontTypeFace, textSize.upperRibbonBtnFont, "normal"), 
                                                     style='Custom.TCombobox', 
                                                     state='readonly', 
                                                     values=self.comparatorValues))
        self.comparator_dropdown[-1].config(width=20)
        self.comparator_dropdown[-1].set("Choose a Comparator")
        self.comparator_dropdown[-1].grid(row=index, column=1, sticky='W', padx=10, pady=10)

        self.value_entries.append(tk.Entry(self, font=(theme.fontTypeFace, textSize.upperRibbonBtnFont, "normal"), bd=3))
        self.value_entries[-1].config(width=20)
        self.value_entries[-1].grid(row=index, column=2, columnspan=2, sticky='W', padx=10, pady=10)

        self.addBtn.grid(row=index+1, column=0, sticky='W', padx=10, pady=10)
        self.cancelBtn.grid(row=index+3, column=2, sticky='W', padx=10)
        self.applyBtn.grid(row=index+3, column=3, sticky='W', padx=10)
        
        if self.store.textSize.name == "Normal":
            self.master.resizeWindow(600, 150+45*(index))
        else:
            self.master.resizeWindow(775, 175+50*(index))


    def applyFilters(self):
        truthy_input = ["t", "true", "truth"]
        falsey_input = ["f", "false", "fake"]

        filter_features = []
        comparator_values = []
        filter_values = []
        for i in range(len(self.feature_dropdown)):
            curFeature = self.feature_dropdown[i]
            curComparator = self.comparator_dropdown[i]
            curValue = self.value_entries[i]
            
            filter_features.append(curFeature.get())
            
            if filter_features[-1] == 'Choose a Feature':
                PopupWarning(bodyTxt="One or more of your filter values are not in the correct format.")
                return
            
            comparator_values.append(curComparator.get())
            
            if filter_features[-1] == "On Wrist":
                if comparator_values[-1] not in ["==", "!="]:
                    PopupWarning(bodyTxt="One or more of your filter values are not in the correct format.")
                    return
                
                if curValue.get().lower() in truthy_input:
                    filter_values.append(True)
                elif curValue.get().lower() in falsey_input:
                    filter_values.append(False)
                else:
                    PopupWarning(bodyTxt="One or more of your filter values are not in the correct format.")
                    return
                
            elif curValue.get().replace(".", "", 1).isdigit():
                filter_values.append(float(curValue.get()))
            else:
                PopupWarning(bodyTxt="One or more of your filter values are not in the correct format.")
                return
                
        for feature, comparator, value in zip(filter_features, comparator_values, filter_values):
            self.store.dataHandler.addFilter(feature, comparator, value)
            
        self.store.dataHandler.updateAllGraphs()

        self.close()
