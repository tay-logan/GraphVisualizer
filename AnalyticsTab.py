import tkinter as tk
from tkinter import ttk
from Templates import ChildFrame, OptionsBox, LowerRibbonTab, LowerRibbonGrid
from Utils import changeLine
import pandas as pd


class AnalyticsTab(LowerRibbonTab):
    """
    Main analytics tab class with all neccesary functionality
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.textSize = self.store.textSize

        # loads in data handler from the store
        self.dataHandler = self.store.dataHandler
        
        self.dataHandler.register_data_update_callback(self.updateOptions)
        
        # Makes grid to have divisions
        self.grid = LowerRibbonGrid(self)
        
        # Enables divisions for parent class
        self.grid.enableDivisions(padx=10)
        
        # Save textfields as a dict of names for basic analytics
        self.statisticsAnalyticsNames = ["Mean", "Median", "Mode", "Standard Deviation", "Max", "Min"]
        self.statisticTexts={}
        
        # Save textfields as a dict of names for advanced analytics
        self.advancedAnalyticsNames = ["Covariance", "Correlation"]
        self.advancedTexts={}
        
        # Creates varblaes to hold chose combobox options for basic analytics
        self.statisticsParticipant = None
        self.statisticsFeature = None
        
        # Creates varblaes to hold chose combobox options for advanced analytics
        self.advancedParticipant1 = None
        self.advancedParticipant2 = None
        self.advancedFeature1 = None
        self.advancedFeature2 = None
        
        
        # Creates the new frame that holds all the things related to statistics section
        self.statisticsFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.statisticsFrame)
        
        # Creates the title label for the statistics section
        statisticsTitleLabel = tk.Label(self.statisticsFrame, 
                                        text="Basic Statistical Analytics", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        statisticsTitleLabel.pack(pady=5, padx=9, anchor="w")
               
        # Creates a new frame for the statistics options (comboboxes and text fields)
        statisticsOptionsFrame = ChildFrame(self.statisticsFrame, 
                                            background=self.theme.lowerRibbonBackground)
        statisticsOptionsFrame.pack(pady=8)
                
        # Creates first combobox to select the participant for statistics analytics
        self.statisticsParticipantCombobox = OptionsBox(statisticsOptionsFrame, 
                                                        defaultTxt="Choose Participant", 
                                                        selectedCommand=self.setStatisticsParticipant,
                                                        style="lowerRibbon.TCombobox", 
                                                        state="readonly")
        self.statisticsParticipantCombobox.grid(row=0, column=0, padx=12, pady=1)

        # Creates second combobox to select the feature for statistics analytics
        self.statisticsFeatureCombobox = OptionsBox(statisticsOptionsFrame,
                                                    defaultTxt="Choose Feature",
                                                    selectedCommand=self.setStatisticsFeature,
                                                    style="lowerRibbon.TCombobox", 
                                                    state="readonly")
        self.statisticsFeatureCombobox.grid(row=1, column=0, padx=12, pady=10)
        
        # Sets row order and column order for the text fields of the statistic results    
        rowOrder = [0, 1, 0, 1, 0, 1]
        colOrder = [2, 2, 3, 3, 4, 4]
        
        # loops through the basic analytics names and creates a titled widget
        # with a text field (to display analytics) result for each
        for name, row, col in zip(self.statisticsAnalyticsNames, rowOrder, colOrder):
            titledWidget = TitledWidget(statisticsOptionsFrame, name)
            titledWidget.outerFrame.grid(row=row, column=col, padx=12)
            self.statisticTexts[name] = tk.Text(titledWidget.outerFrame, 
                    height=1, 
                    state="disabled", 
                    width=11, 
                    font=(self.theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), 
                    background=self.theme.analyticsTabItemBackground, 
                    relief="raised", 
                    border=2)
            
            titledWidget.widget = self.statisticTexts[name]
            titledWidget.widget.pack()
        
        
        # Creates the new frame that holds all the things related to advanced section
        self.advancedFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.advancedFrame)
        
        # Creates the title label for the advanced section
        advancedTitleLabel = tk.Label(self.advancedFrame, 
                                      text="Advanced Statistical Analytics", 
                                      font=(self.theme.fontTypeFace, 
                                            self.textSize.LowerRibbonSectionHeader, 
                                            "bold"), 
                            background=self.theme.lowerRibbonBackground)
        advancedTitleLabel.pack(pady=5, padx=9, anchor="w")
        
        # Creates a new frame for the advanced options (comboboxes and text fields)
        advancedOptionsFrame = ChildFrame(self.advancedFrame, background=self.theme.lowerRibbonBackground)
        advancedOptionsFrame.pack(pady=8)
        
        # Creates a titled widget for participant 1
        participant1TitledWidget = TitledWidget(advancedOptionsFrame, "Feature 1")
        participant1TitledWidget.outerFrame.grid(row=0, column=0, padx=12, pady=1)
        
        # Creates first combobox to select the participant 1
        self.advancedParticipant1Combobox = OptionsBox(participant1TitledWidget.outerFrame,
                                                         defaultTxt="Choose Participant",
                                                         selectedCommand=self.setAdvancedParticipant1,
                                                         style="lowerRibbon.TCombobox", 
                                                         state="readonly")

        self.advancedParticipant1Combobox.pack()
        
        # Adds the first combobox to the titled widget of participant 1
        participant1TitledWidget.widget = self.advancedParticipant1Combobox
        participant1TitledWidget.widget.pack()
        
        # Creates a second combobox to select feature 1
        self.advancedFeature1Combobox = OptionsBox(advancedOptionsFrame,
                                                         defaultTxt="Choose Feature",
                                                         selectedCommand=self.setAdvancedFeature1,
                                                         style="lowerRibbon.TCombobox", 
                                                         state="readonly")
        self.advancedFeature1Combobox.grid(row=1, column=0, padx=12, pady=10)
        
        # Creates a titled widget for participant 2
        participant1TitledWidget = TitledWidget(advancedOptionsFrame, "Feature 2")
        participant1TitledWidget.outerFrame.grid(row=0, column=1, padx=12, pady=1)
        
        # Creates third combobox to select the participant 2
        self.advancedParticipant2Combobox = OptionsBox(participant1TitledWidget.outerFrame,
                                                         defaultTxt="Choose Participant",
                                                         selectedCommand=self.setAdvancedParticipant2,
                                                         style="lowerRibbon.TCombobox", 
                                                         state="readonly")

        self.advancedParticipant2Combobox.pack()
        
        # Adds the third combobox to the titled widget of participant 2
        participant1TitledWidget.widget = self.advancedParticipant2Combobox
        participant1TitledWidget.widget.pack()
        
        # Creates a fourth combobox to select feature 2
        self.advancedFeature2Combobox = OptionsBox(advancedOptionsFrame,
                                                         defaultTxt="Choose Feature",
                                                         selectedCommand=self.setAdvancedFeature2,
                                                         style="lowerRibbon.TCombobox", 
                                                         state="readonly")
        self.advancedFeature2Combobox.grid(row=1, column=1, padx=12, pady=10)
        
        # Sets row order and column order for the text fields of the advanced results    
        rowOrder = [0, 0]
        colOrder = [2, 3]
        
        # loops through the advanced analytics names and creates a titled widget
        # with a text field (to display analytics) result for each
        for analyticsName, row, col in zip(self.advancedAnalyticsNames, rowOrder, colOrder):
            titledWidget = TitledWidget(advancedOptionsFrame, analyticsName)
            titledWidget.outerFrame.grid(row=row, column=col, padx=12, rowspan=2)
            
            self.advancedTexts[analyticsName] = tk.Text(titledWidget.outerFrame, 
                        height=1, 
                        state="disabled", 
                        width=11, 
                        font=(self.theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), 
                        background=self.theme.analyticsTabItemBackground, 
                        relief="raised", 
                        border=2)
            
            titledWidget.widget = self.advancedTexts[analyticsName]
            titledWidget.widget.pack()
            
            
        # Adds the clear button to clear the statistic's comboboxes
        self.clearBtn = ttk.Button(self.grid,
                                   takefocus=False,
                                   style="lower_ribbon_flat.TButton",
                                   command=self.clearTexts,
                                   text="Clear")
        self.grid.addSection(self.clearBtn)
        
    def setStatisticsParticipant(self, _):
        """Callback to set statistics participant"""
        
        self.statisticsParticipant = self.statisticsParticipantCombobox.get()
        self.updateStatisticsResults()
        
    def setStatisticsFeature(self, _):
        """Callback to set statistics feature"""
        self.statisticsFeature = self.statisticsFeatureCombobox.get()
        self.updateStatisticsResults()
        
    def setAdvancedParticipant1(self, _):
        """Callback to set advanced analytics participant 1"""
        self.advancedParticipant1 = self.advancedParticipant1Combobox.get()
        self.updateAdvancedResults()
        
    def setAdvancedParticipant2(self, _):
        """Callback to set advanced analytics participant 2"""
        self.advancedParticipant2 = self.advancedParticipant2Combobox.get()
        self.updateAdvancedResults()
        
    def setAdvancedFeature1(self, _):
        """Callback to set advanced analytics feature 1"""
        self.advancedFeature1 = self.advancedFeature1Combobox.get()
        self.updateAdvancedResults()
    
    def setAdvancedFeature2(self, _):
        """Callback to set advanced analytics feature 2"""
        self.advancedFeature2 = self.advancedFeature2Combobox.get()
        self.updateAdvancedResults()
        
    def updateStatisticsResults(self):
        """Calculates and updates the basic analytics results"""
        if self.statisticsParticipant is None or self.statisticsFeature is None:
            return
        
        data = self.dataHandler.getParticipantData(self.statisticsParticipant).df[self.statisticsFeature]
 
        for statisticName in self.statisticsAnalyticsNames:
            widget = self.statisticTexts[statisticName]
            if statisticName == "Mean":
                changeLine(widget, str(data.mean())[:10])
            if statisticName == "Median":
                changeLine(widget, str(data.median())[:10])
            if statisticName == "Mode":
                changeLine(widget, str(data.mode().to_list()[0])[:11])
            if statisticName == "Standard Deviation":
                changeLine(widget, str(data.std())[:10])
            if statisticName == "Max":
                changeLine(widget, str(data.max())[:10])
            if statisticName == "Min":
                changeLine(widget, str(data.min())[:10])
            else:
                Exception("ahhhhhhhhhh")
        
    def updateAdvancedResults(self):
        """Calculates and updates the advanced analytics results"""
        if (self.advancedParticipant1 is None or self.advancedParticipant2 is None or 
            self.advancedFeature1 is None or self.advancedFeature2 is None):
            return
        
        data1 = self.dataHandler.getParticipantData(self.advancedParticipant1).df[self.advancedFeature1]
        data2 = self.dataHandler.getParticipantData(self.advancedParticipant2).df[self.advancedFeature2]
        
        # Checks both feature data, to convert datetimes into seconds
        if data1.dtype == "datetime64[ns]":
            data1 = data1.apply(lambda x: x.timestamp())
            
        if data2.dtype == "datetime64[ns]":
            data2 = data2.apply(lambda x: x.timestamp())
            
        # Combines both series into one dataframe to calculate results
        d = {self.advancedFeature1: data1, self.advancedFeature2: data2}
        data = pd.DataFrame(data=d)
                
        for advancedName in self.advancedAnalyticsNames:
            widget = self.advancedTexts[advancedName]
            if advancedName == "Covariance":
                changeLine(widget, str(data.cov().loc[self.advancedFeature1, self.advancedFeature2])[:11])
            if advancedName == "Correlation":
                changeLine(widget, str(data.corr().loc[self.advancedFeature1, self.advancedFeature2])[:11])
                       
    def clearTexts(self):
        """Sets callback method when the clear button is pressed  """
        for statisticName in self.statisticsAnalyticsNames:
            changeLine(self.statisticTexts[statisticName], "")
            
        for advancedName in self.advancedAnalyticsNames:
            changeLine(self.advancedTexts[advancedName], "")   

    def updateOptions(self):
        """
        Update participant and feature options in the comboxes
        when they are imported in the home tab, they will be added to the comboboxes
        """
        self.statisticsParticipantCombobox["values"] = self.dataHandler.getParticipantsList()
        self.statisticsFeatureCombobox["values"] = self.dataHandler.getColumnsList()
        
        self.advancedParticipant1Combobox["values"] = self.dataHandler.getParticipantsList()
        self.advancedFeature1Combobox["values"] = self.dataHandler.getColumnsList()
        self.advancedParticipant2Combobox["values"] = self.dataHandler.getParticipantsList()
        self.advancedFeature2Combobox["values"] = self.dataHandler.getColumnsList()
               
       
class TitledWidget(ChildFrame):
    """Used to add a title to a widget"""
    def __init__(self, parent, defaultTxt: str):
        super().__init__(parent)
        self.theme = self.store.theme
        self.textSize = self.store.textSize
        
        # Creates an outer frame to hold the label and the widget
        self.outerFrame = ChildFrame(parent, background=self.theme.lowerRibbonBackground)
        
        # Label that holds the title of the widget
        self.label = tk.Label(self.outerFrame, 
                              text=defaultTxt, 
                              font=(self.theme.fontTypeFace, 
                                    self.textSize.titledWidgetTitle,
                                    "normal"), 
                              background=self.theme.lowerRibbonBackground, 
                              borderwidth=0)
        self.label.pack(anchor="w")
        
        # widget is initially set to None, and is updated before the outerFrame is displayed
        self.widget = None

    