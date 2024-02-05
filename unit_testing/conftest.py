import pytest
import tkinter as tk
from main import Main
from DataHandler import DataHandler
from GraphTab import GraphTab
import tempfile
import _pytest.monkeypatch
from unittest.mock import MagicMock, patch, create_autospec
from HomeTab import HomeTab
from GraphTab import GraphTab
import os
import pandas as pd
import shutil
from GraphFigure import GraphFigure
from Body import Body
from Ribbon import Ribbon, UpperRibbon, LowerRibbon, ChildFrame
from main import App
from FilterTab import FilterTab
from AnalyticsTab import AnalyticsTab
from PIL import ImageTk, Image
from Templates import OptionsBox
from ThemeColors import *
import LocalDataHandler 


class ThemeMock:
    def __init__(self, upperRibbonBackground):
        self.upperRibbonBackground = upperRibbonBackground
        self.upperRibbonUnselectedBtn = MagicMock()

def create_sample_csv(file_path):
    # Ensure that the parent directory exists
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    data = {
        'Datetime (UTC)': ['2020-01-01T00:00:00Z', '2020-01-01T00:05:00Z'],
        "Timezone (minutes)": [-300, -300],
        'Unix Timestamp (UTC)': [1577836800, 1577837100],
        'Steps count': [1, 2],
        'Temp avg': [3, 4], 
        'On Wrist': [False, True]
    }
    df = pd.DataFrame(data)

    # Save the file to the appropriate location
    df.to_csv(file_path, index=False)

@pytest.fixture(scope="session")
def ribbon(session_monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    session_monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    session_monkeypatch.setattr(ImageTk, 'PhotoImage', mock_img_import)
    
    parent = MagicMock(spec=ChildFrame)
    parent.tk = MagicMock()  
    parent._w = '.'
    parent.children = MagicMock()
    parent.store = MagicMock()
    with patch('Ribbon.UpperRibbon', autospec=True) as MockUpperRibbon, \
         patch('Ribbon.LowerRibbon', autospec=True) as MockLowerRibbon:
        
        MockUpperRibbon.return_value._selectBtn = MagicMock()
        ribbon = Ribbon(parent)
        yield ribbon

@pytest.fixture(scope="session")
def body():
    root = MagicMock()  
    body = Body(root)
    yield body

@pytest.fixture(scope="session")
def upper_ribbon():
    parent = MagicMock(spec=ChildFrame)
    theme_mock = ThemeMock('some_color')
    parent.store = MagicMock()
    parent.store.get.return_value = theme_mock
    parent.tk = MagicMock()
    parent._w = '.'
    parent.children = MagicMock()
    upper_ribbon = UpperRibbon(parent)
    yield upper_ribbon

@pytest.fixture(scope="session")
def lower_ribbon(session_monkeypatch):
    parent = MagicMock(spec=ChildFrame)
    parent.tk = MagicMock()
    parent._w = '.'
    parent.children = MagicMock()
    parent.store = MagicMock()

    # Mock the 'tk.call' method
    def mock_tk_call(*args, **kwargs):
        return None

    session_monkeypatch.setattr(parent.tk, 'call', mock_tk_call)

    lower_ribbon = LowerRibbon(parent)

    # Mock the 'show' method for each tab in the lowerRibbonTabs dictionary
    for tab_name, tab_instance in lower_ribbon.lowerRibbonTabs.items():
        tab_instance.show = MagicMock()
        tab_instance.hide = MagicMock()

    return lower_ribbon

@pytest.fixture(scope="session")
def graph_figure(session_monkeypatch):
    
    def mock_img_import(*args, **kwargs):
        return None
    
    session_monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    
    img_mock = MagicMock()
    del_func_mock = MagicMock()
    selected_callback_mock = MagicMock()
    
    graphID = 'G1'
    graph = {
        'data': MagicMock(participantID='Participant 1'),
        'graph_t': 'Line',
        'time_values': [0, 1, 2, 3, 4],
        'feature_values': [10, 15, 20, 25, 30],
        'b_color': 'white',
        'd_color': 'blue',
    }

    instance = GraphFigure(graphID, graph, del_func_mock, selected_callback_mock)
    instance.img = img_mock
    return instance

@pytest.fixture(scope="session")
def data_handler():
    store = MagicMock()
    data_handler = DataHandler(store)  
    
    return data_handler

@pytest.fixture(scope="session")
def session_monkeypatch():
    mpatch = _pytest.monkeypatch.MonkeyPatch()
    yield mpatch
    mpatch.undo()

@pytest.fixture(scope="session")
def mock_response(session_monkeypatch):
    def mock_mainloop(*args, **kwargs):
        return None

    session_monkeypatch.setattr(tk.Tk, "mainloop", mock_mainloop)


@pytest.fixture(scope="session")
def main_instance(mock_response):
    main_instance = Main()
    yield main_instance
    # Any cleanup code can be added here, if necessary

@pytest.fixture(scope="session")
def app_instance(session_monkeypatch):
    parent = MagicMock(spec=Main)
    parent.tk = MagicMock()
    parent._w = '.'
    parent.children = MagicMock()
    parent.store = MagicMock()

    # Mock the 'tk.call' method
    def mock_tk_call(*args, **kwargs):
        return None
    
    def mock_img_import(*args, **kwargs):
        return None

    session_monkeypatch.setattr(parent.tk, 'call', mock_tk_call)
    session_monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    session_monkeypatch.setattr(ImageTk, 'PhotoImage', mock_img_import)

    # Mock the participant_dropdown object in GraphTab
    with patch('GraphTab.ttk.Combobox') as mock_participant_dropdown:
        mock_participant_dropdown.return_value.cget.return_value = 20
        with patch.object(App, 'pack') as mock_pack:
            app = App(parent)
            app.pack = mock_pack

    return app

@pytest.fixture
def temp_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture(scope="session")
def home_tab(session_monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    session_monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    
    home_tab_instance = HomeTab(MockParent())    
    # Create the store object with a DataHandler object within it
    
    store = MagicMock()
    data_handler = DataHandler(store)  # Create an instance of DataHandler
    
    # Set the DataHandler object as an attribute of the store object
    store.dataHandler = data_handler
    store.textSize = NormalText()
    
    # Set the store object as an attribute of the parent object
    home_tab_instance.store = store
    
    yield home_tab_instance

@pytest.fixture(scope="session")
def graph_tab(session_monkeypatch):
    class Mock_Dropdown(dict):
        def __init__(self, **kw) -> None:
            super().__init__(**kw)
            
        def get(self):
            return self["values"]
        
    # session_monkeypatch.setattr("tkinter.ttk.Combobox", MagicMock())
    session_monkeypatch.setattr("tkinter.ttk.Button", MagicMock())
    session_monkeypatch.setattr("tkinter.ttk.Style", MagicMock())
    session_monkeypatch.setattr("tkinter.Label", MagicMock())
    session_monkeypatch.setattr("tkinter.Entry", MagicMock())
    session_monkeypatch.setattr("tkinter.Frame", MagicMock())

    session_monkeypatch.setattr("PIL.ImageTk.PhotoImage", MagicMock())
    session_monkeypatch.setattr("PIL.Image.open", MagicMock())
    session_monkeypatch.setattr("PIL.Image.Image.resize", MagicMock())

    graph_tab = GraphTab(MockParent())

    graph_tab.add_button.state = MagicMock(return_value=["disabled"])
    graph_tab.update_button.state = MagicMock(return_value=["disabled"])
    
    graph_tab.participant_dropdown = Mock_Dropdown()
    graph_tab.feature_dropdown = Mock_Dropdown()

    return graph_tab

class MockParent:
    def __init__(self):
        self.store = MagicMock()
        self.tk = MagicMock()
        self._last_child_ids = MagicMock()
        self._w = '.'
        self.children = MagicMock()

@pytest.fixture(scope="session")
def filter_tab(session_monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    session_monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    # session_monkeypatch.setattr(ImageTk, 'PhotoImage', mock_img_import)

    parent = MockParent()
    filter_tab = FilterTab(parent)

    yield filter_tab

@pytest.fixture(scope="session")
def analytics_tab_instance():
    parent = MockParent()
    analytics_tab = AnalyticsTab(parent)

    return analytics_tab


@pytest.fixture
def sample_data_folder():
    # Create a temporary folder for testing
    temp_folder = tempfile.mkdtemp()

    # Create sample CSV files
    file_path1 = os.path.join(temp_folder, "310", "summary.csv")
    file_path2 = os.path.join(temp_folder, "311", "summary.csv")
    create_sample_csv(file_path1)
    create_sample_csv(file_path2)

    yield temp_folder

    # Clean up the temporary folder after the test session
    shutil.rmtree(temp_folder)
    
@pytest.fixture
def mock_store():
    store = MagicMock()
    store.dataHandler = DataHandler(store)
    store.appTheme
    return store