import pytest
from unittest.mock import MagicMock, call, patch, create_autospec
from SettingsTab import SettingsTab
from PopupWarning import PopupWarning
import tkinter as tk
from LocalDataHandler import readFile
import os

def test_selectTheme(mock_store, monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    
    settings_tab = SettingsTab(mock_store)
    settings_tab.store.appTheme = MagicMock()
    
    # Test light theme
    settings_tab.selectTheme("Light Mode")
    settings_tab.store.appTheme.changeTheme.assert_called_with("Light")
    assert readFile("settings", ["theme"]) == "Light"
    
    # Test dark theme
    settings_tab.selectTheme("Dark Mode")
    assert readFile("settings", ["theme"]) == "Dark"
    
    settings_tab.selectTheme("Light Mode")    

def test_selectTextSize(mock_store, monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    
    settings_tab = SettingsTab(mock_store)
    settings_tab.store.appTheme = MagicMock()
    
    # Test normal size
    settings_tab.selectTextSize("Normal Size")
    settings_tab.store.appTheme.changeTextSize.assert_called_with("Normal")
    assert readFile("settings", ["text_size"]) == "Normal"
    
    # Test large size
    settings_tab.selectTextSize("Large Size")
    settings_tab.store.appTheme.changeTextSize.assert_called_with("Large")
    assert readFile("settings", ["text_size"]) == "Large"
    
    settings_tab.selectTextSize("Normal Size")
    
    
    

def test_openUserGuide(mock_store, monkeypatch):
    def mock_img_import(*args, **kwargs):
        return None
    
    monkeypatch.setattr(tk, 'PhotoImage', mock_img_import)
    
    dirname = os.path.dirname(__file__)
    
    
    # Mock os.startfile to assert it is called correctly
    mock_startfile = MagicMock()
    monkeypatch.setattr("os.startfile", mock_startfile)
    
    # Test user guide exists
    settings_tab = SettingsTab(MagicMock())
    settings_tab.openUserGuide()
    assert mock_startfile.assert_called_once
    
