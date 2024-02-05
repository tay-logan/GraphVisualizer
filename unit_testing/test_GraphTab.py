from unittest.mock import MagicMock, call
from LocalDataHandler import readFile
from unittest.mock import patch
from GraphTab import GraphTab
from DataHandler import DataHandler

def test_graph_tab_creation(graph_tab):
    assert isinstance(graph_tab, GraphTab)


def test_graph_tab_has_expected_widgets(graph_tab):
    assert hasattr(graph_tab, "participant_dropdown")
    assert hasattr(graph_tab, "feature_dropdown")
    assert hasattr(graph_tab, "type_buttons")
    assert hasattr(graph_tab, "background_color_button")
    assert hasattr(graph_tab, "data_color_button")
    assert hasattr(graph_tab, "x_axis_from_dropdown")
    assert hasattr(graph_tab, "x_axis_to_dropdown")
    assert hasattr(graph_tab, "interval_entry")
    assert hasattr(graph_tab, "add_button")
    assert hasattr(graph_tab, "update_button")


def test_graph_tab_buttons_initially_disabled(graph_tab):
    assert "disabled" in graph_tab.add_button.state()
    assert "disabled" in graph_tab.update_button.state()

def test_update_participant_dropdown(graph_tab, monkeypatch):
    # Mock the return value of getParticipantsList
    graph_tab.store.dataHandler.getParticipantsList.return_value = ['P1', 'P2', 'P3']

    # Call the update_participant_dropdown method
    graph_tab.update_participant_dropdown()

    # Assert the participant dropdown values are updated correctly
    assert graph_tab.participant_dropdown['values'] == ['P1', 'P2', 'P3']

def test_update_feature_dropdown(graph_tab):
    # Reset the mock

    # Mock the return value of getFeaturesList
    graph_tab.store.dataHandler.getFeaturesList.return_value = ['F1', 'F2', 'F3']

    # Call the update_feature_dropdown method
    graph_tab.update_feature_dropdown()

    # Assert the feature dropdown values are updated correctly
    assert graph_tab.feature_dropdown['values'] == ['F1', 'F2', 'F3']

def test_add_action(graph_tab):
    # Set up mock return values
    graph_tab.getSelectedType = MagicMock(return_value='Line')
    graph_tab.data_color_label.cget.return_value = 'data_color'
    graph_tab.interval_entry.get.return_value = '10'

    # Call the add_action method
    with patch.object(graph_tab, 'participant_dropdown') as mock_participant_dropdown, \
         patch.object(graph_tab, 'feature_dropdown') as mock_feature_dropdown, \
         patch.object(graph_tab, 'clear_fields') as mock_clear_fields, \
         patch.object(graph_tab, 'background_color_label') as mock_bg_color_label:
             
        mock_participant_dropdown.get.return_value = 'P1'
        mock_feature_dropdown.get.return_value = 'F1'
        mock_bg_color_label.cget.return_value = 'bg_color'
        
        graph_tab.add_action()

        # Assert the add_graph method is called with the correct arguments
        graph_tab.store.dataHandler.add_graph.assert_called_with(
            'P1', 'Line', 'F1', 10, 'bg_color', 'data_color'
        )

        # Assert that the clear_fields function was called
        mock_clear_fields.assert_called_once()  # Add this line

def test_update_action(graph_tab):    
    graph_tab.store.dataHandler.get_graphID.return_value = 'G1'
    with patch.object(graph_tab, 'x_axis_from_dropdown') as mock_x_axis_from, \
        patch.object(graph_tab, 'x_axis_to_dropdown') as mock_x_axis_to, \
        patch.object(graph_tab, 'clear_fields') as mock_clear_fields, \
        patch.object(graph_tab, 'background_color_label') as mock_bg_color_label:
        mock_bg_color_label.cget.return_value = 'bg_color'
        # Call the update_action method
        graph_tab.update_action()

    # Assert the update_graph method is called with the correct arguments
    graph_tab.store.dataHandler.updateGraphVisuals.assert_called_with(
        'G1',
        'Line',
        10,
        'bg_color',
        'data_color'
    )

    # Assert the update_button and delete_button are disabled
    graph_tab.update_button.state.assert_called_with(["disabled"])
    mock_clear_fields.assert_called_once()  # Add this line
