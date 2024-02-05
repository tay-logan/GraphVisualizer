from unittest.mock import MagicMock, call
from LocalDataHandler import readFile
from unittest.mock import patch
import tkinter as tk
import pandas as pd

def test_graph_figure_attributes(graph_figure):
    assert graph_figure.selectedCallback is not None
    assert graph_figure.delete is not None
    assert graph_figure.graphObj is not None
    assert graph_figure.graph_id == 'G1'
    assert graph_figure.image_path == "assets/images/icons/delete.png"
    assert graph_figure.img is not None

def test_create_graph(graph_figure, monkeypatch):
    # Create a mock function for plot_graph
    mock_plot_graph = MagicMock()

    # Use the patch context manager to replace the plot_graph method with the mock function
    with patch.object(graph_figure, "plot_graph", mock_plot_graph):
        # Call the createGraph method with a mock for tk.Button
        with patch('tkinter.Button') as mocked_button:
            graph_figure.createGraph()

        # Assert that the created attributes exist and have the correct values
        assert graph_figure.fig is not None
        assert graph_figure.plot is not None
        assert graph_figure.container_frame is not None
        assert graph_figure.canvas is not None
        assert graph_figure.delete_button is not None

        # Test if the plot_graph method was called
        mock_plot_graph.assert_called_once()

        # Assert that the delete button's command is set to the delete_graph method
        mocked_button.assert_called_with(graph_figure.container_frame, image=graph_figure.img, command=graph_figure.delete_graph, bg="white", padx=8, pady=8, relief=tk.FLAT)


def test_plot_graph(graph_figure, monkeypatch):
    test_create_graph(graph_figure, monkeypatch)
    # Set up mock values for the graph_figure attributes
    graph_figure.canvas = MagicMock()
    graph_figure.graphObj = {
        "data": MagicMock(participantID="Participant 1"),
        "graph_t": "Line",
        "time_values": pd.Series([0, 1, 2, 3, 4], name="Time"),
        "feature_values": pd.Series([10, 15, 20, 25, 30], name="Feature"),
        "b_color": "white",
        "d_color": "blue",
    }

    # Mock the plot object using patch
    with patch.object(graph_figure, "plot", MagicMock()) as mock_plot:
        # Call the plot_graph method
        graph_figure.plot_graph()

        # Assert the correct methods were called with the expected arguments
        mock_plot.set_facecolor.assert_called_once_with("white")
        mock_plot.margins.assert_called_once_with(x=0.01)
        mock_plot.plot.assert_called_once_with(
            graph_figure.graphObj["time_values"],
            graph_figure.graphObj["feature_values"],
            color="blue",
        )
        mock_plot.set_title.assert_called_once()
    
    graph_figure.canvas.draw.assert_called_once()

def test_update_graph(graph_figure):
    # Mock the plot object and the plot_graph method
    graph_figure.plot = MagicMock()
    graph_figure.plot_graph = MagicMock()

    # Call the updateGraph method
    graph_figure.updateGraph()

    # Assert that the plot object's clear method is called
    graph_figure.plot.clear.assert_called_once()

    # Assert that the plot_graph method is called
    graph_figure.plot_graph.assert_called_once()

def test_delete_graph(graph_figure):
    # Mock the delete method and the delete_button's destroy method
    graph_figure.delete = MagicMock()
    graph_figure.delete_button = MagicMock(destroy=MagicMock())

    # Set a mock value for graph_id attribute
    graph_figure.graph_id = 1

    # Call the delete_graph method
    graph_figure.delete_graph()

    # Assert that the delete method is called with the correct graph_id
    graph_figure.delete.assert_called_once_with(1)

    # Assert that the delete_button's destroy method is called
    graph_figure.delete_button.destroy.assert_called_once()
