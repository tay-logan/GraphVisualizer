from Templates import LowerRibbonGrid, ChildFrame, OptionsBox
from tkinter import ttk
from unittest.mock import MagicMock, patch, ANY
import pandas as pd


def test_analytics_tab_initialization(analytics_tab_instance):
    analytics_tab = analytics_tab_instance
    # Test if dataHandler is initialized correctly
    assert analytics_tab.dataHandler is not None

    # Test if grid is an instance of LowerRibbonGrid
    assert isinstance(analytics_tab.grid, LowerRibbonGrid)

    # Test if statisticsAnalyticsNames and advancedAnalyticsNames are initialized correctly
    assert analytics_tab.statisticsAnalyticsNames == ["Mean", "Median", "Mode", "Standard Deviation", "Max", "Min"]
    assert analytics_tab.advancedAnalyticsNames == ["Covariance", "Correlation"]

    # Test if statisticTexts and advancedTexts are dictionaries
    assert isinstance(analytics_tab.statisticTexts, dict)
    assert isinstance(analytics_tab.advancedTexts, dict)

    # Test if the statistics participant and feature variables are initialized to None
    assert analytics_tab.statisticsParticipant is None
    assert analytics_tab.statisticsFeature is None

    # Test if the advanced participant and feature variables are initialized to None
    assert analytics_tab.advancedParticipant1 is None
    assert analytics_tab.advancedParticipant2 is None
    assert analytics_tab.advancedFeature1 is None
    assert analytics_tab.advancedFeature2 is None

    # Test if statisticsFrame and advancedFrame are instances of ChildFrame
    assert isinstance(analytics_tab.statisticsFrame, ChildFrame)
    assert isinstance(analytics_tab.advancedFrame, ChildFrame)

    # Test if statisticsParticipantCombobox and statisticsFeatureCombobox are instances of OptionsBox
    assert isinstance(analytics_tab.statisticsParticipantCombobox, OptionsBox)
    assert isinstance(analytics_tab.statisticsFeatureCombobox, OptionsBox)

    # Test if advancedParticipant1Combobox, advancedParticipant2Combobox, advancedFeature1Combobox, and advancedFeature2Combobox are instances of OptionsBox
    assert isinstance(analytics_tab.advancedParticipant1Combobox, OptionsBox)
    assert isinstance(analytics_tab.advancedParticipant2Combobox, OptionsBox)
    assert isinstance(analytics_tab.advancedFeature1Combobox, OptionsBox)
    assert isinstance(analytics_tab.advancedFeature2Combobox, OptionsBox)

    # Test if clearBtn is an instance of ttk.Button
    assert isinstance(analytics_tab.clearBtn, ttk.Button)

