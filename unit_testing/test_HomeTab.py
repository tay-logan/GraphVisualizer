import pytest
import tkinter as tk
from tkinter import ttk
import _pytest.monkeypatch
import uuid
from unittest.mock import MagicMock
from HomeTab import ImportPopup
import pandas as pd
from LocalDataHandler import readFile
from unittest.mock import patch

def test_import_folder(sample_data_folder, home_tab):
    # Call the importBtnCallback method with the sample_data_folder
    import_popup = ImportPopup(home_tab)
    import_popup.folderPathList = [sample_data_folder]
    import_popup.importBtnCallback()

    # Check if data was imported correctly
    assert home_tab.store.dataHandler.featureDataList is not None
    assert len(home_tab.store.dataHandler.featureDataList) > 0
    assert len(home_tab.store.dataHandler.featureDataList) == 2   
    
# def test_open_prev_file(home_tab, monkeypatch):
#     # Mock the "readFile" function to return a specific list of files
#     def mock_read_file(file_type):
#         return [os.path.abspath("file1"), os.path.abspath("file2"), os.path.abspath("file3")]

#     # Mock the "importFromFile" function so that it doesn't actually import any files
#     mock_import_from_file = MagicMock()
#     monkeypatch.setattr(DataHandler, "importFromFile", mock_import_from_file)

#     # Use a context manager to temporarily replace the readFile function with the mock during the openPrevFile call
#     with monkeypatch.context() as m:
#         m.setattr("LocalDataHandler.readFile", mock_read_file)

#     # Instantiate the HomeTab object with a mock store and call the "openPrevFile" method
#     result = home_tab.openPrevFile(0)

#     # Check if the "importFromFile" function was called the expected number of times
#     assert mock_import_from_file.call_count == 1

#     # Check if the "importFromFile" function was called with the correct arguments
#     mock_import_from_file.assert_any_call(mock_read_file("imports")[0])

#     # Check if the "openPrevFile" method returns the expected value
#     assert result == None


def test_hide_graphs(sample_data_folder, home_tab):
    graph_id1 = str(uuid.uuid4())
    graph_id2 = str(uuid.uuid4())
    graph_t = "Line"
    y_var = "Steps count"

    home_tab.store.dataHandler.graphs = {
        graph_id1: {"graph_type": graph_t, "y_var": y_var},
        graph_id2: {"graph_type": graph_t, "y_var": y_var},
    }

    # Ensure that graphs exist before hiding
    assert len(home_tab.store.dataHandler.graphs) == 2

    # Mock the tkinter messagebox.askyesno function to return True
    _pytest.monkeypatch.MonkeyPatch().setattr(tk.messagebox, "askyesno", lambda *args, **kwargs: True)

    # Call the hideGraphs method
    home_tab.hideGraps()

    # Check if graphs are removed
    assert len(home_tab.store.dataHandler.graphs) == 0

    # Check if data is cleared
    assert home_tab.store.dataHandler.featureDataList is None or len(home_tab.store.dataHandler.featureDataList) == 0

