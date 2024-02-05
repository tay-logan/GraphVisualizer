from unittest.mock import MagicMock, call, patch
import pytest

def test_body_initialization(body):
    assert body.theme is not None
    assert body.graphRegion is not None
    assert body.store.get.called_once_with("theme")

def test_display_graph(body):
    body.graphRegion.addRow = MagicMock()
    body.store.dataHandler.getGraph = MagicMock(return_value={
        'graph_fig': None
    })

    with patch('Body.GraphFigure', autospec=True) as MockedGraphFigure:
        graph_fig_instance = MockedGraphFigure.return_value
        graph_fig_instance.graph_fig = None

        body.display(0)

        # Get the created graph dictionary
        created_graph = body.store.dataHandler.getGraph.return_value

        MockedGraphFigure.assert_called_once_with(
            0, created_graph,
            body.store.dataHandler.delete_graph,
            body.store.updateGraphTabFields
        )
        graph_fig_instance.createGraph.assert_called_once()
        graph_fig_instance.enableScroll.assert_called_once_with(body.graphRegion.container)
        graph_fig_instance.show.assert_called_once()

        # Check that the graph_fig attribute was set correctly
        assert created_graph["graph_fig"] == graph_fig_instance
        body.store.dataHandler.getGraph.assert_called_once_with(0)

def test_delete_graph(body):
    body.graphRegion.deleteRow = MagicMock()

    body.delete_graph(0)

    body.graphRegion.deleteRow.assert_called_once_with(0)

def test_delete_all_graphs(body):
    body.graphRegion.deleteRow = MagicMock()

    body.deleteAllGraphs(5)

    body.graphRegion.deleteRow.assert_has_calls([call(0)] * 5)


