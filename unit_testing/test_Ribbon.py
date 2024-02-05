import pytest
import tkinter as tk
from unittest.mock import MagicMock
from GraphTab import GraphTab
from SettingsTab import SettingsTab
from Ribbon import UpperRibbon, LowerRibbon

def test_ribbon(ribbon):
    ribbon.lowerRibbon.update = MagicMock()
    ribbon.update_lower_ribbon("Graphs")
    ribbon.upperRibbon._selectBtn.assert_called_once_with("Home")
    ribbon.lowerRibbon.update.assert_called_once_with("Graphs")
    assert isinstance(ribbon.upperRibbon, UpperRibbon)
    assert isinstance(ribbon.lowerRibbon, LowerRibbon)

def test_upper_ribbon_init(upper_ribbon):
    # Test if the upperRibbonBtns dictionary is initialized correctly
    expected_keys = ["Home", "Graph", "Filter", "Analysis", "Settings"]
    assert list(upper_ribbon.upperRibbonBtns.keys()) == expected_keys

def test_lower_ribbon_init(lower_ribbon):
    lowerRib = lower_ribbon
    # Test if the lowerRibbonTabs dictionary is initialized correctly
    expected_keys = ["Home", "Graph", "Filter", "Analysis", "Settings"]
    assert list(lower_ribbon.lowerRibbonTabs.keys()) == expected_keys

    # Test if the initial value of curTab is None
    assert lower_ribbon.curTab is None

def test_lower_ribbon_update(lower_ribbon):
    # Test updating the current tab
    lower_ribbon.update("Graph")

    # Test if the current tab is updated to the GraphTab
    assert isinstance(lower_ribbon.curTab, GraphTab)

    # Test if the show method is called on the current tab
    lower_ribbon.curTab.show.assert_called_once()

    # Test updating the current tab again
    lower_ribbon.update("Settings")

    # Test if the current tab is updated to the SettingsTab
    assert isinstance(lower_ribbon.curTab, SettingsTab)

    # Test if the hide method is called on the previous tab (GraphTab)
    lower_ribbon.lowerRibbonTabs["Graph"].hide.assert_called_once()

    # Test if the show method is called on the current tab (SettingsTab)
    lower_ribbon.curTab.show.assert_called_once()