import tkinter as tk
from tkinter import filedialog

class NoneSelected(Exception):
    pass

def cloneWidget(widget: tk.Widget, parent = None):
    """
    Clones a widget to allow for exact copies to be made  
    (with a new parent)  
    """
    # Assigns the same parent if a new one isnt specified
    if parent is None:
        parent = widget.nametowidget(widget.winfo_parent())
    
    # Copies the class type to create a new one
    widget_type = widget.__class__
    
    # Passes in all the configure options to the new widget
    cfg = {keyword: widget.cget(keyword) for keyword in widget.configure()}
    clone = widget_type(parent, **cfg)
    
    return clone


def deleteLines(widget: tk.Widget, rowIndex: int = 1):
    """
    Used to delete lines from a text widget, at a specific row
    """
    # sets the state to normal, to allow for changes
    widget.configure(state="normal")

    # deletes the desired line
    widget.delete(float(rowIndex+1), float(rowIndex+2))
    
    # sets the state to normal, block changes by the user
    widget.configure(state="disabled")

def changeLine(textWidget: tk.Widget, text: str, rowIndex: int = 0):
    """
    Used to change a line in a text widget, at a specified row
    """
    textWidget.configure(state="normal")
        
    # deletes the desired line
    textWidget.delete(float(rowIndex+1), float(rowIndex+2))
    
    # Then inserts the new line where the old line was
    textWidget.insert(round(float(rowIndex+1),1), text)
    
    # sets the state to normal, block changes by the user
    textWidget.configure(state="disabled")
    
    return textWidget

def defocus(event):
    """
    Used to remove focus from the option box
    to preserve the desired behavior
    """
    combobox = event.widget
    combobox.selection_clear()
    combobox.master.focus()
    
def getFolderPath() -> list:
    chosen_path = filedialog.askdirectory()
    
    if chosen_path == "":
        raise NoneSelected

    return chosen_path
                
