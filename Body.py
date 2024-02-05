import tkinter as tk
from tkinter import ttk
from Templates import ChildFrame, ScrollableRegion
from GraphFigure import GraphFigure       
        
class Body(ChildFrame):
    """
    Main body class with all neccesary functionality
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.theme = self.store.get("theme")
      
        self.configure(background=self.theme.bodyBackground)        
        self.pack(fill="both", expand=1)
        
        # Gives the store, a way to delete graphs and display them
        self.store.set("deleteAllGraphs", self.deleteAllGraphs)
        self.store.set("delete_graph", self.delete_graph)
        self.store.set("displayGraph", self.display)

        self.graphRegion = ScrollableRegion(self)
        self.graphRegion.setBackground("white")

    def display(self, graphId):
        dataHandler = self.store.dataHandler
        
        graph = dataHandler.getGraph(graphId)

        # Create the graph
        newFrame = self.graphRegion.addRow()
        
        graphFig = GraphFigure(graphId, graph, self.store.dataHandler.delete_graph,
                                self.store.updateGraphTabFields)
        
        graphFig.createGraph(parent=newFrame)
        graphFig.enableScroll(self.graphRegion.container)
        graphFig.show()

        # Add the graph figure to the list
        graph["graph_fig"] = graphFig

    def delete_graph(self, rowIndex: int):
        """Update the scrollable region using the deleteRow function"""
        self.graphRegion.deleteRow(rowIndex)
        
        
    def deleteAllGraphs(self, graphCount):    
        """Delete all from the scrollable region using the deleteRow function"""
            
        for _ in range(graphCount):
            self.graphRegion.deleteRow(0)

 




    