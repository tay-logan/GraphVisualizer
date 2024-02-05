import json
import os

FILE_PATH = {"settings": "/local/settings.json",
             "imports": "/local/imports.json"
             }

DEFAULT_FILE = {"settings": {"theme": "Light", 
                             "text_size": "Normal", 
                             "time": "UTC"
                             },
                "imports": []
                }

        
def _traverseDict(obj, locationPath=[]):
    """
    Traverses the dictionary to desired location
    """
    curLocation = obj
    
    # For each of the keys, it traverses into the dictionary
    for key in locationPath:
        curLocation = curLocation[key]

    # returns the dict after traversal
    return curLocation

def _saveFile(filePath, saveObj):
    """
    Saves the obj to the json file
    """
    with open(os.getcwd() + filePath, "w") as settingsFile:
        json.dump(saveObj, settingsFile)

def readFile(fileName: str , locationPath=[]):
    """
    Gets the desired obj in the file        
    """

    filePath = FILE_PATH[fileName]
    defaultFile = DEFAULT_FILE[fileName]

    try:
        # if the file is found, then it traverses it
        with open(os.getcwd() + filePath, "r") as file:
            obj = json.load(file)

        if fileName == "imports":
            for path in obj:
                open(path.replace("\\", "/"), "r")
        elif fileName == "settings":
            for key in defaultFile.keys():
                _ = obj[key]

            
    except :
        # If file is not found, default one is saved, and traversed
        _saveFile(filePath, defaultFile)
        
        obj = defaultFile

    return _traverseDict(obj, locationPath)

def saveFile(fileName: str, locationPath = [], newObj={}):
    """
    Saves new obj to a json file
    """
    # File path is found by the name
    filePath = FILE_PATH[fileName]
    
    if len(locationPath) > 0:
        # if there is a file path, then it will traverse it
        curObj = readFile(fileName, locationPath[:-1])
        
        # sets the new option to the last dict location
        curObj[locationPath[-1]] = newObj
        _saveFile(filePath, curObj)
        
    else:
        # if there is no file path, then the new settings obj become the new obj       
        _saveFile(filePath, newObj)

def appendFile(fileName: str, locationPath = [], newObj={}):
    """
    Appends a new settings to the settings file
    """
    # File path is found by the name
    filePath = FILE_PATH[fileName]
    
    # Traverses the obj to the location
    obj = readFile(fileName, locationPath)
    
    # Appends the new setting in the last location
    obj.append(newObj)
    
    # New obj is saved to the file path
    _saveFile(filePath, obj)