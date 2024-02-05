import tkinter as tk
from tkinter import ttk, colorchooser
from LocalDataHandler import readFile
import pandas as pd
from Templates import LowerRibbonTab, OptionsBox, LowerRibbonGrid, ChildFrame
from PIL import Image, ImageTk
from AnalyticsTab import TitledWidget

class GraphTab(LowerRibbonTab):
    def __init__(self, parent):
        super().__init__(parent)
        theme = self.store.theme
        self.textSize = self.store.textSize
        
        # loads in data handler from the store
        self.dataHandler = self.store.dataHandler
        
        # Register the updateDataHandler callback
        self.store.set("updateGraphTabFields", self.update_fields)
        
        self.store.dataHandler.register_data_update_callback(self.clear_fields)
        self.store.dataHandler.register_data_update_callback(self.update_participant_dropdown)
        self.store.dataHandler.register_data_update_callback(self.update_feature_dropdown)
        
        self.graph_id = None
        self.local_set = False
        self.time_values = []

        # Define column widths and titles
        columns = ["Display", "Type", "Coloring", "Time Range", ""]
        title_font = (theme.fontTypeFace, self.textSize.lowerRibbonBtnFont, "bold")
        small_font = (theme.fontTypeFace, self.textSize.LowerRibbonSectionHeader, "bold")
        dropdown_font = (theme.fontTypeFace, self.textSize.graphTab)
        
        # Makes grid to have divisions
        self.grid = LowerRibbonGrid(self)
        
        # Enables divisions for parent class
        self.grid.enableDivisions(padx=10)
        
        # Creates the new frame that holds all the things related to display section
        self.displayFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.displayFrame)
        
        # Creates the title label for the display section
        displayTitleLabel = tk.Label(self.displayFrame, 
                                        text="Display", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        displayTitleLabel.pack(pady=(10, 2), padx=9, anchor="w")

        # Creates a new frame for the display options (comboboxes)
        displayOptionsFrame = ChildFrame(self.displayFrame, 
                                            background=self.theme.lowerRibbonBackground)
        displayOptionsFrame.pack(pady=15)

        # Add dropdowns
        self.participant_dropdown = OptionsBox(displayOptionsFrame, 
                                               "Choose Participant", 
                                               self.attempFillFields, 
                                               style='lowerRibbon.TCombobox', 
                                               state='normal')
        self.participant_dropdown.grid(row=0, column=0, padx=12, pady=9)
        
        
        self.feature_dropdown = OptionsBox(displayOptionsFrame, 
                                               "Choose Feature", 
                                               self.attempFillFields, 
                                               style='lowerRibbon.TCombobox', 
                                               state='normal')
        self.feature_dropdown.grid(row=1, column=0, padx=12, pady=9)

        
        # Creates the new frame that holds all the things related to types section
        self.typesFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.typesFrame)
        
        # Creates the title label for the types section
        typesTitleLabel = tk.Label(self.typesFrame, 
                                        text="Types", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        typesTitleLabel.pack(pady=5, padx=9, anchor="w")
        
        # Creates the new frame that holds all types options
        self.typesOptions = ChildFrame(self.typesFrame, background=self.theme.lowerRibbonBackground)
        self.typesOptions.pack(pady=5, padx=9, anchor="w")

        # Add buttons to the Type column
        button_images = {
            "Line": 'assets/images/buttons/VP_Graphs-01.png',
            "Bar": 'assets/images/buttons/VP_Graphs-02.png',
            "Area": 'assets/images/buttons/VP_Graphs-05.png',
            "Scatter": 'assets/images/buttons/VP_Graphs-07.png'
        }

        self.type_buttons = {}

        for name, img_path in button_images.items():
        # Load the image with PIL
            img = Image.open(img_path)

            # Scale down the image to the desired size
            img = img.resize((50, 50), Image.ANTIALIAS)

            # Convert the image to a Tkinter PhotoImage
            img = ImageTk.PhotoImage(img)

            button = ttk.Button(
                self.typesOptions,
                image=img,
                takefocus=False,
                command=lambda typeName=name: self.setSelectedType(typeName),
                style="graph_unselected.TButton",
                compound='top',
                text=name,
                width=(self.textSize.lowerRibbonBtnFont-9)
            )
            
            button.img = img  # Store a reference to the image to prevent garbage collection
            button.grid(row=0, column=len(self.type_buttons.values()), padx=4, pady=5)
            
            button.bind("<ButtonPress>", self.attemptEnableButtons)
                        
            self.type_buttons[name] = button
            
        # Creates the new frame that holds all the things related to coloring section
        self.coloringFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.coloringFrame)
        
        # Creates the title label for the coloring section
        coloringTitleLabel = tk.Label(self.coloringFrame, 
                                        text="Coloring", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        coloringTitleLabel.pack(pady=(5, 9), padx=9, anchor="w")
        
        # Creates the new frame that holds all coloring options
        self.coloringOptions = ChildFrame(self.coloringFrame, background=self.theme.lowerRibbonBackground)
        self.coloringOptions.pack(pady=5, padx=9, anchor="w")

        # Add color options
        self.background_label = tk.Label(self.coloringOptions, text="Background Color", font=(theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), background=self.theme.lowerRibbonBackground, foreground="#505050")
        self.background_label.grid(row=0, column=0, padx=5, pady=12, sticky="w")

        self.background_color_label = tk.Label(self.coloringOptions, text=" ", font=(theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), background="#FFFFFF", borderwidth=1, relief="solid", width=2, height=1)
        self.background_color_label.grid(row=0, column=1, padx=5, pady=12, sticky="w")

        self.background_color_button = ttk.Button(
            self.coloringOptions,
            text="Select",
            style="lower_ribbon_flat_sm.TButton",
            command=self.select_background_color,
            padding=(-16, 0, -16, 0),
            takefocus=0
        )
        self.background_color_button.bind("<KeyRelease>", self.attemptEnableButtons)
        self.background_color_button.grid(row=0, column=2, padx=5, pady=12, sticky="w")

        self.data_label = tk.Label(self.coloringOptions, text="Data Color", font=(theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), background=self.theme.lowerRibbonBackground, foreground="#505050")
        self.data_label.grid(row=1, column=0, padx=5, pady=12, sticky="w")

        self.data_color_label = tk.Label(self.coloringOptions, text=" ", font=(theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), background="#FFFFFF", borderwidth=1, relief="solid", width=2, height=1)
        self.data_color_label.grid(row=1, column=1, padx=5, pady=12, sticky="w")
        self.data_color_label.config(bg='#0080FF')

        self.data_color_button = ttk.Button(
            self.coloringOptions,
            text="Select",
            style="lower_ribbon_flat_sm.TButton",
            command=self.select_data_color,
            padding=(-16, 0, -16, 0),
            takefocus=0
        )
        self.data_color_button.grid(row=1, column=2, padx=5, pady=12, sticky="w")
        self.data_color_button.bind("<KeyRelease>", self.attemptEnableButtons)
        
        
        # Creates the new frame that holds all the things related to time range section
        self.timeRangeFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.timeRangeFrame)
        
        # Creates the title label for the time range section
        timeRangeTitleLabel = tk.Label(self.timeRangeFrame, 
                                        text="Time Range", 
                                        font=(self.theme.fontTypeFace, 
                                              self.textSize.LowerRibbonSectionHeader, 
                                              "bold"), 
                                        background=self.theme.lowerRibbonBackground)
        # timeRangeTitleLabel.pack(pady=5, padx=9, anchor="w")
        timeRangeTitleLabel.grid(row=0, column=0, sticky="W", padx=5, pady=(5, 14))
        
        
        # Add comboboxes to the Time Range column

        # Creates a titled widget for Start Time
        startTimeTitledWidget = TitledWidget(self.timeRangeFrame, "Start Time")
        # startTimeTitledWidget.outerFrame.pack(pady=5, padx=9, anchor="w")
        startTimeTitledWidget.outerFrame.grid(row=1, column=0, sticky="W", padx=5)

        self.x_axis_from_dropdown = OptionsBox(parent=self.timeRangeFrame, 
                                               defaultTxt=" ", 
                                               selectedCommand=self.filterTimeValues,  
                                               style='lowerRibbon.TCombobox', 
                                               state='normal')
        # self.x_axis_from_dropdown.config(width=int(self.x_axis_from_dropdown.cget('width') * 1.15))
        self.x_axis_from_dropdown.bind("<KeyRelease>", self.attemptEnableButtons)
        # self.x_axis_from_dropdown.pack(padx=9, anchor="w")
        self.x_axis_from_dropdown.grid(row=2, column=0, sticky="W", padx=5, pady=(0, 8))

        # Creates a titled widget for End Time
        endTimeTitledWidget = TitledWidget(self.timeRangeFrame, "End Time")
        # endTimeTitledWidget.outerFrame.pack(pady=5, padx=9, anchor="w")
        endTimeTitledWidget.outerFrame.grid(row=3, column=0, sticky="W", padx=5)

        self.x_axis_to_dropdown = OptionsBox(parent=self.timeRangeFrame,
                                             defaultTxt=" ", 
                                             selectedCommand=self.filterTimeValues,  
                                             style='lowerRibbon.TCombobox', 
                                             state='normal')
        # self.x_axis_to_dropdown.config(width=int(self.x_axis_to_dropdown.cget('width') * 1.15))
        self.x_axis_to_dropdown.bind("<KeyRelease>", self.attemptEnableButtons)
        # self.x_axis_to_dropdown.pack(padx=9, anchor="w")
        self.x_axis_to_dropdown.grid(row=4, column=0, sticky="W", padx=5, pady=(0,14))


        # Creates a titled widget for Interval
        participant1TitledWidget = TitledWidget(self.timeRangeFrame, "Interval")
        # participant1TitledWidget.outerFrame.pack(pady=5, padx=9, anchor="w")
        participant1TitledWidget.outerFrame.grid(row=1, column=1, sticky="W", padx=10)
        

        self.interval_entry = tk.Entry(self.timeRangeFrame, font=(self.theme.fontTypeFace, self.textSize.lowerRibbonTextWidget, "normal"), width=8)
        self.interval_entry.bind("<KeyRelease>", self.attemptEnableButtons)
        self.interval_entry.bind("<FocusOut>", self.attemptEnableButtons)
        # self.interval_entry.pack(padx=9, anchor="w")
        self.interval_entry.grid(row=2, column=1, sticky="W", padx=10, pady=(0,14))

        # Creates the new frame that holds the buttons
        self.actionsFrame = ChildFrame(self.grid, background=self.theme.lowerRibbonBackground)
        self.grid.addSection(self.actionsFrame)

        # Add "Add" and "Update" buttons in the "Action" column
        self.add_button = ttk.Button(
            self.actionsFrame,
            text="Add",
            style="graph.TButton",
            command=self.add_action,
            state="disabled",
            padding=(-8, 3, -8, 3),
            takefocus=0
        )
        self.add_button.pack(pady=5, padx=9, anchor="w")
        
        self.update_button = ttk.Button(
            self.actionsFrame,
            text="Update",
            style="graph.TButton",
            command=self.update_action,
            state="disabled",
            padding=(-8, 3, -8, 3),
            takefocus=0
        )
        self.update_button.pack(pady=5, padx=9, anchor="w")

    def on_focus_in(self, event):
        combobox = event.widget
        combobox.selection_clear()
        combobox.master.focus_set()

    def update_participant_dropdown(self):
        # Get unique participant IDs
        unique_participant_ids = self.store.dataHandler.getParticipantsList()

        # Update the participant dropdown
        self.participant_dropdown['values'] = unique_participant_ids
        
    def update_feature_dropdown(self):
        # Get unique feature names
        unique_feature_names = self.store.dataHandler.getFeaturesList()
        # Update the feature dropdown
        self.feature_dropdown['values'] = unique_feature_names

    def filterTimeValues(self, event=None):
        selected_from_value = self.x_axis_from_dropdown.get()
        selected_to_value = self.x_axis_to_dropdown.get()
        
        # Convert the selected values to a pandas.Timestamp
        selected_from_time = pd.to_datetime(selected_from_value)
        selected_to_time = pd.to_datetime(selected_to_value)
        
        # Find the index of the selected values in the time_values list
        selected_from_index = self.time_values.index(selected_from_time)
        selected_to_index = self.time_values.index(selected_to_time)
        
        # Get the updated "To" values based on the selected "From" value
        updated_from_values = self.time_values[:selected_to_index]
        updated_to_values = self.time_values[selected_from_index+1:]
        
        # Update the "x-axis to" dropdown values
        self.x_axis_from_dropdown['values'] = updated_from_values
        self.x_axis_to_dropdown['values'] = updated_to_values

    def setTimeRange(self):
        timeSeries = self.store.dataHandler.getTimeValues()
        
        self.time_values = timeSeries
            
        # Update the "x-axis from" and "x-axis to" dropdowns
        self.x_axis_from_dropdown['values'] = self.time_values
        self.x_axis_to_dropdown['values'] = self.time_values
   
    def setDefaultTime(self):
        # updates the min/max drop downs
        self.x_axis_from_dropdown.set(min(self.time_values))
        self.x_axis_to_dropdown.set(max(self.time_values))
    
    def clear_fields(self):
        # Reset all fields
        self.participant_dropdown.set("Choose a Participant")
        self.feature_dropdown.set("Choose a Feature")
        
        self.setSelectedType(None)
        
        # Clear the options list of x_axis_from_dropdown and x_axis_to_dropdown
        self.x_axis_from_dropdown['values'] = []
        self.x_axis_to_dropdown['values'] = []
        
        self.x_axis_from_dropdown.set("")
        self.x_axis_to_dropdown.set("")
        self.interval_entry.delete(0, 'end')
        self.background_color_label.config(bg="#FFFFFF")
        self.data_color_label.config(bg="#0080FF")
        self.add_button.state(["disabled"])
        self.update_button.state(["disabled"])

    def setSelectedType(self, selected_type):
        oldSelectedType = self.getSelectedType()
        
        if oldSelectedType is not None:
            oldSelectedBtn = self.type_buttons[oldSelectedType]
            oldSelectedBtn.state(["!selected"])
            oldSelectedBtn.config(style="graph_unselected.TButton")
        
        if selected_type is not None:
            selectedBtn = self.type_buttons[selected_type]
            selectedBtn.state(["selected"])
            selectedBtn.config(style="graphSelect.TButton")

    def add_action(self):
        # Get the selected values from each field
        participant_id = self.participant_dropdown.get()
        feature = self.feature_dropdown.get()
        
        graph_type = self.getSelectedType()

        background_color = self.background_color_label.cget("bg")
        data_color = self.data_color_label.cget("bg")
        start_time = self.x_axis_from_dropdown.get()
        end_time = self.x_axis_to_dropdown.get()

        # Convert the interval to an integer
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            print("Invalid interval value")
            return

        # Add a graph dict to the dataHandler and return its Id
        newGraphID = self.store.dataHandler.add_graph(
            participant_id, 
            graph_type, 
            feature, 
            interval, 
            background_color, 
            data_color)
        
        self.store.dataHandler.setTimeRanges(start_time, end_time)
        
        # Disable Add button
        self.clear_fields()
    
    def graphExists(self) -> bool:
        participant_id = self.participant_dropdown.get()
        feature = self.feature_dropdown.get()
        graphID = self.store.dataHandler.get_graphID(participant_id, feature)
        return graphID is not None
    
    def attempFillFields(self, event=None):
        participant_id = self.participant_dropdown.get()
        feature = self.feature_dropdown.get()
        
        if participant_id == "Choose a Participant":
            self.update_participant_dropdown()
            self.participant_dropdown.set(self.participant_dropdown['values'][0])
            participant_id = self.participant_dropdown.get()
            
        if feature == "Choose a Feature":
            self.feature_dropdown.set(self.feature_dropdown['values'][0])
            feature = self.feature_dropdown.get()
        
        if self.graphExists():
            graphID = self.store.dataHandler.get_graphID(participant_id, feature)
            self.update_fields(graphID)
            return
            
        if self.getSelectedType() is None:
            self.setSelectedType("Line")
            
        self.setTimeRange()
        self.setDefaultTime()
        self.filterTimeValues()

        # Check if interval entry is empty
        intervalValue = self.interval_entry.get()

        if not (intervalValue.isdigit() and int(intervalValue) > 0):
            self.interval_entry.delete(0, 'end')
            self.interval_entry.insert(0, "1")

        self.attemptEnableButtons()
                
    def attemptEnableButtons(self, event=None):
        
        if self.allFieldsValid():
                # Enable or disable the update_button based on whether 
                # a graph with the selected participant ID and feature exists
                alreadyExists = self.graphExists()
                
                if alreadyExists:
                    self.add_button.state(["disabled"])
                    self.update_button.state(["!disabled"])
                else:
                    self.add_button.state(["!disabled"])
                    self.update_button.state(["disabled"])
        else:
            self.add_button.state(["disabled"])
            self.update_button.state(["disabled"])
                
                
    def allFieldsValid(self):
        participant_id = self.participant_dropdown.get()
        feature = self.feature_dropdown.get()
        bgColor = self.background_color_label.cget("bg")
        dataColor = self.data_color_label.cget("bg")
        fromTime = self.x_axis_from_dropdown.get()
        toTime = self.x_axis_to_dropdown.get()
        intervalValue = self.interval_entry.get()
        graphType = self.getSelectedType()
        
        return (participant_id and feature and
                participant_id != "Choose a Participant" and feature != "Choose a Feature" and
                graphType is not None and
                bgColor and dataColor and fromTime and
                toTime and intervalValue.isdigit() and
                (int(intervalValue) > 0))


    def update_action(self):
        self.update_button.state(["disabled"])

        # Get the selected values from each field
        participant_id = self.participant_dropdown.get()
        feature = self.feature_dropdown.get()
        graph_type = self.getSelectedType()
                
        background_color = self.background_color_label.cget("bg")
        data_color = self.data_color_label.cget("bg")
        start_time = self.x_axis_from_dropdown.get()
        end_time = self.x_axis_to_dropdown.get()
        interval = int(self.interval_entry.get())

        g_id = self.store.dataHandler.get_graphID(participant_id, feature)

        # Update the graph
        self.store.dataHandler.updateGraphVisuals(g_id, 
                                                  graph_type, 
                                                  interval, 
                                                  background_color, 
                                                  data_color)
        self.store.dataHandler.setTimeRanges(start_time, end_time)


        self.clear_fields()

    def select_background_color(self):
        color = tk.colorchooser.askcolor()
        if color:
            self.background_color_label.config(bg=color[1])
            self.background_color = color[1]

    def update_fields(self, graphID: str):    
        graph = self.store.dataHandler.getGraph(graphID)    
        
        participant_id = graph["data"].participantID
        feature = graph["y_var"]
        
        self.participant_dropdown.set(participant_id)
        self.feature_dropdown.set(feature)
                            
        self.setSelectedType(graph["graph_t"])
                
        self.background_color_label.config(bg=graph["b_color"])
        self.data_color_label.config(bg=graph["d_color"])
        
        lowerRange, upperRange = self.store.dataHandler.getTimeRanges()
        
        self.x_axis_from_dropdown.set(lowerRange)
        self.x_axis_to_dropdown.set(upperRange)
        self.setTimeRange()
        
        self.interval_entry.delete(0, 'end')
        self.interval_entry.insert(0, str(graph["inter"]))
        
        self.graph_id = graphID
        self.attemptEnableButtons()
        
        
    def getSelectedType(self) -> str:
        selected = None
        for button in self.type_buttons.values():
            if button.instate(["selected"]):
                selected = button["text"]
                
        return selected

    def select_data_color(self):
        color = tk.colorchooser.askcolor()
        if color:
            self.data_color_label.config(bg=color[1])

    def show(self) -> None:
        self.pack(side='top', anchor="nw", fill="both", expand=1)       

    def hide(self) -> None:
        self.pack_forget()
