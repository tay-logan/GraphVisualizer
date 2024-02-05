import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as CanvasFigure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk  as NavigationTool
from matplotlib.figure import Figure


class GraphFigure():
    """Generates a graph onto provided frame"""
    def __init__(self, graphID, graph, del_func, selectedCallback=None):
        self.selectedCallback = selectedCallback
        self.delete = del_func
        self.graphObj = graph
        self.graph_id = graphID
        self.image_path = "assets/images/icons/delete.png"
        self.img = tk.PhotoImage(file=self.image_path)

    def show(self):   
        """Shows the graph"""    
        self.canvas.get_tk_widget().pack(anchor="nw", fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hides the graph"""
        self.canvas.get_tk_widget().pack_forget()
    
    # Enales scrolling of parent frame
    def enableScroll(self, outerContainer):
        self.bigCanvas = outerContainer
        self.canvas.get_tk_widget().bind_all("<MouseWheel>", self.onScroll)
            
    def onScroll(self, event):
        """Sets scroll speed"""
        self.bigCanvas.yview_scroll(int(-1* (event.delta/5)), "pixels")
    
    def addNav(self, parent):
        """Adds a navigation tool (Deprecated)"""
        self.navBar = NavigationTool(self.canvas, parent, pack_toolbar=False)
        self.navBar.pack(side="top")

    def removeNav(self):
        """Hides the graph and Navigivation tool (Deprecated)"""
        self.navBar.pack_forget()

    def plot_graph(self):
        """Creates the graph and draws the graph"""
        participant_id = self.graphObj["data"].participantID
        graph_type = self.graphObj["graph_t"]
        time_values = self.graphObj["time_values"]
        feature_values = self.graphObj["feature_values"]

        back_color = self.graphObj["b_color"]
        data_color = self.graphObj["d_color"]

        self.plot.set_facecolor(back_color)
        
        self.plot.margins(x=0.01)
        
        # Defines the X and Y axis
        x_column = time_values
        y_column = feature_values
        
        # Sets the plot type
        if graph_type == 'Line':
            self.plot.plot(x_column, y_column, color=data_color)
        elif graph_type == 'Scatter':
            self.plot.scatter(x_column, y_column, color=data_color, s=5)
        elif graph_type == 'Bar':
            self.plot.bar(x_column, y_column, color=data_color)
        elif graph_type == 'Area':
            self.plot.fill_between(x_column, y_column, color=data_color)
        else:
            raise ValueError('Invalid graph_type provided. Supported types are: line, scatter, bar, area.')

        self.plot.set_title(f"{y_column.name} vs. {x_column.name} for {participant_id}", loc="left", color='Black')
        
        self.canvas.draw()
        
    def createGraph(self, parent=None):    
        """Creates the figure with parameters"""    
        self.fig = Figure(figsize=(18.6, 3), dpi=100, tight_layout=True)
        self.plot = self.fig.add_subplot(111)
        self.fig.set_facecolor('white')  # Set the outer color of the graph
        self.plot.tick_params(axis='x', labelcolor='black')
        self.plot.tick_params(axis='y', labelcolor='black')

        # Frame that holds the figure and the delete button
        self.container_frame = tk.Frame(parent, bg="white")
        self.container_frame.pack(side="top", fill="both", expand=True)

        # Canvas holds the figure
        self.canvas = CanvasFigure(self.fig, self.container_frame)
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        
        # Delete button used to remove the graph from the body
        self.delete_button = tk.Button(self.container_frame, image=self.img, command=self.delete_graph, bg="white", padx=8, pady=8, relief=tk.FLAT)
        self.delete_button.pack(side="right", padx=(0, 5))

        self.canvas.get_tk_widget().bind("<Button-1>", self.on_click)

        # Update the canvas with the new graph
        self.plot_graph()
        
    def updateGraph(self):  
        """Update the canvas with the new graph"""      
        self.plot.clear()
        self.plot_graph()

    def delete_graph(self):
        """Delete graph by calling callback function"""
        self.delete(self.graph_id)
        self.delete_button.destroy()

    def on_click(self, event):
        """Callback for when the graph is clicked"""
        self.show_graph_info()

    def show_graph_info(self):
        """When graph is clicked, the selected graph is updated"""
        if not self.plot:
            print(f"Participant ID {self.participant_id} not found.")
            return

        # Call the callback function with the relevant graph information
        self.selectedCallback(self.graph_id)





        