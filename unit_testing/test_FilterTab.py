from Templates import LowerRibbonGrid, CheckBoxController
from FilterTab import ChildFrame, FilterChip
from tkinter import ttk
from unittest import mock
from unittest.mock import MagicMock

def test_filter_tab_initialization(filter_tab):
    assert filter_tab.dataHandler == filter_tab.store.dataHandler
    assert filter_tab.filters == []
    assert isinstance(filter_tab.grid, LowerRibbonGrid)
    assert isinstance(filter_tab.timezoneSettingsFrame, ChildFrame)
    assert isinstance(filter_tab.timezoneController, CheckBoxController)
    assert isinstance(filter_tab.filtersFrame, ChildFrame)
    assert isinstance(filter_tab.filtersList, ChildFrame)
    assert isinstance(filter_tab.clearBtn, ttk.Button)
    assert isinstance(filter_tab.addBtn, ttk.Button)

class FakeFilter:
    def __init__(self, chip_display):
        self.chipDisplay = chip_display

def test_update_filter_list(filter_tab, monkeypatch):
    # Create a mock_destroy function
    def mock_destroy():
        mock_destroy.called = True
    mock_destroy.called = False

    # Mock getAllFilters method
    monkeypatch.setattr(
        filter_tab.dataHandler,
        "getAllFilters",
        lambda: [
            FakeFilter(chip_display=None),
            FakeFilter(chip_display=MagicMock(outerFrame=MagicMock(destroy=mock_destroy))),
        ],
    )

    # Patch FilterChip constructor
    mock_filter_chip_constructor = MagicMock()
    monkeypatch.setattr("FilterTab.FilterChip", lambda *args, **kwargs: mock_filter_chip_constructor(*args, **kwargs))

    # Call the method
    filter_tab.updateFilterList()

    # Check if the outerFrame.destroy() method is called for the second filter
    assert mock_destroy.called

    # Check if FilterChip instances were created for both filters
    assert mock_filter_chip_constructor.call_count == 2

def test_clear_filters(filter_tab, monkeypatch):
    # Mock the deleteAllFilters method
    def mock_delete_all_filters():
        mock_delete_all_filters.called = True
    mock_delete_all_filters.called = False
    monkeypatch.setattr(filter_tab.dataHandler, "deleteAllFilters", mock_delete_all_filters)

    # Call the method
    filter_tab.clearFilters()

    # Check if the deleteAllFilters method is called
    assert mock_delete_all_filters.called


def test_add_filters(filter_tab, monkeypatch):
    # Mock the FilterPopup constructor
    def mock_filter_popup_constructor(*args, **kwargs):
        mock_filter_popup_constructor.called = True
    mock_filter_popup_constructor.called = False
    monkeypatch.setattr("FilterTab.FilterPopup", mock_filter_popup_constructor)

    # Call the method
    filter_tab.addFilters()

    # Check if the FilterPopup constructor is called
    assert mock_filter_popup_constructor.called




