from dataclasses import dataclass

def rgbShades(rgbStr, alpha):
    """Gets a new rbg val after applying alpha transparency"""
    r, g, b = [255 - round((255 - int(rgbStr[i:i+2], 16)) * alpha) 
         for i in range(1, 7, 2)]
    
    return f"#{r:X}{g:X}{b:X}"
    
    
@dataclass
class LightTheme():
    fontTypeFace = "Inter"
    ribbonSelectedBtn = "#3387EA"
    
    upperRibbonBackground = rgbShades("#D9D9D9", 0.8)
    upperRibbonTextColor = "#828282"
    upperRibbonUnselectedBtn = "#c4c4c4"
    
    lowerRibbonBackground = rgbShades("#D9D9D9", 0.5)
    lowerRibbonTextColor = "#505050"
    lowerRibbonUnselectedBtn = "#D9D9D9"
    
    analyticsTabItemBackground = "#ffffff"
    analyticsTabDisabledBtnBackground = "#C9C9C9"
    analyticsTabDisabledBtnTextColor = "#BCBCBC"
    
    
    bodyBackground = "white"
    
@dataclass
class DarkTheme():
    fontTypeFace = "Inter"
    ribbonSelectedBtn = "#3387EA"
    
    upperRibbonBackground = rgbShades("#000000", 0.8)
    upperRibbonTextColor = "#000000"
    upperRibbonUnselectedBtn = "#000000"
    
    lowerRibbonBackground = rgbShades("#D9D9D9", 0.5)
    lowerRibbonTextColor = "#505050"
    lowerRibbonUnselectedBtn = "#D9D9D9"
    
    analyticsTabItemBackground = "#ffffff"
    analyticsTabDisabledBtnBackground = "#C9C9C9"
    analyticsTabDisabledBtnTextColor = "#BCBCBC"
    
    bodyBackground = "white"
    
@dataclass
class NormalText():
    name = "Normal"
    upperRibbonBtnFont = 11
    LowerRibbonSectionHeader = 10
    titledWidgetTitle = 7
    lowerRibbonTextWidget = 9
    lowerRibbonBtnFont = 12
    lowerRibbonNamedCheckboxLabel = 10
    popUpWarningHeader = 14
    dropdown = 14
    graphTab = 13
    
@dataclass
class LargeText():
    name = "Large"
    upperRibbonBtnFont = 15
    LowerRibbonSectionHeader = 14
    titledWidgetTitle = 11
    lowerRibbonTextWidget = 13
    lowerRibbonBtnFont = 16
    lowerRibbonNamedCheckboxLabel = 14
    popUpWarningHeader = 18
    dropdown = 18
    graphTab = 17