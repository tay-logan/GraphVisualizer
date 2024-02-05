from ThemeColors import LightTheme, NormalText, LargeText, DarkTheme
import pandas as pd
import uuid
from unittest.mock import MagicMock
from Store import Store
from main import App
from DataHandler import DataHandler
from Ribbon import Ribbon
from Body import Body
from LocalDataHandler import readFile
import tkinter as tk

def test_main(main_instance):
    result = main_instance
    assert isinstance(main_instance.store, Store)
    assert isinstance(main_instance.store.dataHandler, DataHandler)
    if readFile("settings", ["text_size"]) == "Normal":
        assert result.store.theme == LightTheme()
    else :
        assert result.store.theme == DarkTheme()
    assert result.store.textSize == NormalText() or result.store.textSize == LargeText()
    assert result.cget("background") == "white"
    assert main_instance.title() == "Graph Visualizer"
    # Test geometry (only the position of the window)
    geometry = main_instance.geometry()
    position = geometry.split('+')[1:]
    assert position == ['0', '0']
    # Test if there's an App instance as a child of Main
    app_found = False
    for child in main_instance.winfo_children():
        if isinstance(child, App):
            app_found = True
            break
    assert app_found

def test_app_init(app_instance):
    # Test if the ribbon and body attributes are instances of the Ribbon and Body classes
    assert isinstance(app_instance.ribbon, Ribbon)
    assert isinstance(app_instance.body, Body)

def test_app_pack(app_instance):
    # Test if the pack method was called with the correct arguments
    app_instance.pack.assert_called_once()

def test_import_from_folder(sample_data_folder,data_handler, monkeypatch):
    # Mock the readFile function
    def mock_read_file(file_name, location_path=None):
        if file_name == "imports":
            return []
        return None

    monkeypatch.setattr("LocalDataHandler.readFile", mock_read_file)

    # Mock the saveFile function
    def mock_save_file(file_name, location_path=None, save_obj=None):
        pass

    monkeypatch.setattr("LocalDataHandler.saveFile", mock_save_file)

    # Call the importFromFolder method
    total = data_handler.importFromFolder(str(sample_data_folder))

    # Check the result
    assert total == 2
    assert len(data_handler.featureDataList) == 2

def test_get_participant_data(data_handler):
    # Test the getParticipantData method
    for index, data in enumerate(data_handler.featureDataList):
        id = data.participantID
        data_holder1 = data_handler.getParticipantData(id)
        assert data_holder1 == data_handler.featureDataList[index]

    participant_data_nonexistent = data_handler.getParticipantData(999)
    assert participant_data_nonexistent == None

def test_get_all_data(data_handler):
    
    # Test the getAllData method
    data = data_handler.getAllData()
    assert len(data) == 2

def test_get_ParticipantsList(data_handler):
    
    participantList = data_handler.getParticipantsList()
    id1 = "310"
    id2 = "311"
    exist1 = False
    exist2 = False
    for id in participantList:
        if id == id1:
            exist1 = True
        if id == id2:
            exist2 = True
    assert exist1 and exist2

def test_getFeaturesList(data_handler):
    
    featureList = data_handler.getFeaturesList()
    assert featureList == ['Steps count', 'Temp avg', 'On Wrist']

def test_getColumnsList(data_handler):
    columnList1 = data_handler.getColumnsList()
    expected_columns = ['Datetime (UTC)', 'Steps count', 'Temp avg', 'On Wrist', 'Datetime (Local)']
    
    # Check if the expected columns are present and in the same order
    assert columnList1 == expected_columns

def test_add_graph(data_handler, monkeypatch):
    # Define the test parameters
    participantID = "310"
    graph_t = "Line"
    y_var = "Steps count"
    s_time = pd.to_datetime("2020-01-01T00:00:00Z", utc=True)
    e_time = pd.to_datetime("2020-01-01T00:05:00Z", utc=True)
    inter = 5
    b_color = "red"
    d_color = "blue"

    # Mock uuid.uuid4() to return a predictable value
    mock_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")

    def mock_uuid4():
        return mock_uuid

    monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

    # Create MagicMock objects for the mock methods
    mock_displayGraph = MagicMock()
    mock_updateAllGraphs = MagicMock()

    monkeypatch.setattr(data_handler.store, "displayGraph", mock_displayGraph)
    monkeypatch.setattr(data_handler, "updateAllGraphs", mock_updateAllGraphs)
    
    # Call the add_graph method
    graph_id = data_handler.add_graph(
        participantID, graph_t, y_var, inter, b_color, d_color
    )

    # Verify the returned graph_id
    assert graph_id == "12345678-1234-5678-1234-567812345678"

    # Verify the graph was added to the 'graphs' dictionary
    graph_data = data_handler.graphs[graph_id]

    # Check if the values in the graph_data dictionary are as expected
    assert graph_data["graph_t"] == graph_t
    assert graph_data["y_var"] == y_var
    assert graph_data["inter"] == inter
    assert graph_data["b_color"] == b_color
    assert graph_data["d_color"] == d_color

def test_get_graphID(sample_data_folder, data_handler, monkeypatch):
    test_import_from_folder(sample_data_folder, data_handler, monkeypatch)
    test_add_graph(data_handler, monkeypatch)
    
    # Define the test parameters
    participantID = "310"
    y_var = "Steps count"
    
    non_exist_id = "100"
    non_exist_y_var = "Temperature"
    # Call the get_graphID method
    result_graph_id = data_handler.get_graphID(participantID, y_var)
    failed_graph_id = data_handler.get_graphID(non_exist_id, non_exist_y_var)
    # Verify if the graph_id returned by get_graphID is the same as the one created in add_graph
    assert result_graph_id is not None
    assert failed_graph_id is None

def test_update_graph(data_handler):
    
    # Define the test parameters
    participantID = "310"
    y_var = "Steps count"
    non_exist_id = "100"
    # Call the add_graph method to add a graph
    result_graph_id = data_handler.get_graphID(participantID, y_var)
    # Update the graph parameters
    updated_graph_t = "bar"
    updated_s_time = "2020-01-01T00:00:00Z"
    updated_e_time = "2020-01-01T00:10:00Z"
    updated_inter = 10
    updated_b_color = "green"
    updated_d_color = "purple"

    graph_fig = MagicMock()
    data_handler.graphs[result_graph_id]["graph_fig"] = graph_fig

    result = data_handler.updateGraphVisuals(result_graph_id, updated_graph_t, updated_inter, updated_b_color, updated_d_color)

    failed = data_handler.updateGraphVisuals("12345678-1234-5678-1234-567812345679", updated_graph_t, updated_inter, updated_b_color, updated_d_color)
    # Verify if the graph was updated successfully
    assert result is True
    assert failed is False

    # Verify if the graph parameters were updated
    updated_graph = data_handler.graphs[result_graph_id]
    assert updated_graph["graph_t"] == updated_graph_t
    assert updated_graph["inter"] == updated_inter
    assert updated_graph["b_color"] == updated_b_color
    assert updated_graph["d_color"] == updated_d_color

def test_delete_graph(data_handler):
    
    participantID = "310"
    y_var = "Steps count"
    result_graph_id = data_handler.get_graphID(participantID, y_var)
    data_handler.delete_graph(result_graph_id)
    assert result_graph_id not in data_handler.graphs
