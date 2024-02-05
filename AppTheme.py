from  ThemeColors import *
from tkinter import ttk

_themes = {"Light": LightTheme(),
           "Dark": DarkTheme()}
"""Dict that holds the themes"""

_textSizes = {"Normal": NormalText(),
              "Large": LargeText()}
"""Dict that holds the text sizes"""


class AppTheme():
    """App theme controls the visuals of the app"""
    
    def __init__(self, styleName: str, themeName: str, textSize: str):
        self.name = themeName
    
        self.style = ttk.Style()
        self.style.theme_use(styleName) 
        self.theme = _themes[themeName]
        self.textSize = _textSizes[textSize]
        
        self._loadTheme()
        
    def _loadTheme(self):
        """Applies the new style to the ttk style"""
        
        configureTheme(self.style, self.theme, self.textSize)
        
    def changeTheme(self, themeName: str):
        """Changes the theme of the app"""
        
        self.theme = _themes[themeName]
        self._loadTheme()
    
    def changeTextSize(self, textSize: str):
        """Changes the text size of the app"""
        
        self.textSize = _textSizes[textSize]
        self._loadTheme()


def configureTheme(style, curTheme, textSize):
    """configures the ttk style of the app"""
    
    style.configure("upper_ribbon_unselected.TButton", 
                    padx=1,
                    background=curTheme.upperRibbonBackground,
                    foreground=curTheme.upperRibbonTextColor, 
                    font=(curTheme.fontTypeFace, 
                            textSize.upperRibbonBtnFont, 
                            "bold"),
                    relief='grove')
    
    style.map("upper_ribbon_unselected.TButton", 
                background=[("active", curTheme.upperRibbonBackground)])
    
    style.configure("upper_ribbon_selected.TButton", 
                    background=curTheme.upperRibbonBackground,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                            textSize.upperRibbonBtnFont, 
                            "bold"),
                    relief='grove')
    
    style.map("upper_ribbon_selected.TButton", 
                background=[("active", curTheme.upperRibbonBackground)])
    
    
    style.configure("lower_ribbon_unselected.TButton", 
                    background=curTheme.lowerRibbonUnselectedBtn,
                    foreground=curTheme.lowerRibbonTextColor,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonBtnFont, 
                            "bold"),
                    relief='grove')
    
    style.map("lower_ribbon_unselected.TButton", 
                background=[("active", curTheme.lowerRibbonUnselectedBtn)],
                foreground=[("active", curTheme.ribbonSelectedBtn)])
    
    style.configure("lower_ribbon_selected.TButton", 
                    background=curTheme.lowerRibbonBackground,
                    foreground=curTheme.lowerRibbonTextColor,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonBtnFont, 
                            "bold"),
                    relief='grove')
    
    style.map("lower_ribbon_selected.TButton", 
                background=[("active", curTheme.lowerRibbonBackground)])
    
    style.configure("warning.TButton",
                    background=curTheme.ribbonSelectedBtn,
                    foreground=curTheme.bodyBackground,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonBtnFont, 
                            "bold"),
                    relief="grove")
    
    style.map("warning.TButton",
                    background=[("active", curTheme.upperRibbonBackground)])
    

    style.configure("lower_ribbon_flat.TButton", 
                    background=curTheme.lowerRibbonBackground,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                            textSize.LowerRibbonSectionHeader,
                            "bold"),
                    relief='grove')
    
    style.map("lower_ribbon_flat.TButton", 
                background=[("active", curTheme.lowerRibbonBackground)],
                foreground=[("active", curTheme.lowerRibbonTextColor)])    
    
    style.configure("lower_ribbon_flat_sm.TButton", 
                    background=curTheme.lowerRibbonBackground,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonTextWidget,
                            "normal"),
                    relief='grove')
    
    style.map("lower_ribbon_flat_sm.TButton", 
                background=[("active", curTheme.lowerRibbonBackground)],
                foreground=[("active", curTheme.lowerRibbonTextColor)])  
    
    style.map("recent_files.TButton", 
                    background=[("active", curTheme.lowerRibbonBackground)],
                    foreground=[("active", curTheme.ribbonSelectedBtn)])              
    style.configure("recent_files.TButton", 
                    background=curTheme.lowerRibbonBackground,
                    foreground=curTheme.lowerRibbonTextColor,
                    font=(curTheme.fontTypeFace, textSize.lowerRibbonBtnFont, "bold"),
                    relief='grove')
    
    style.configure("lowerRibbon.TCombobox",
                    font=(curTheme.fontTypeFace, 
                              textSize.dropdown,
                              "normal"),
                    foreground="black")
    
    style.map('lowerRibbon.TCombobox',
        fieldbackground=[('readonly', '#ffffff')],
        background=[('readonly', '#ffffff')],
        focusfill=[('readonly', '#ffffff')])  # Add this line
    
    style.configure("analytics_tab.TButton", 
                    background=curTheme.analyticsTabItemBackground,
                    foreground=curTheme.lowerRibbonTextColor,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonBtnFont,
                              "normal"),
                    relief='grove')
    style.map("analytics_tab.TButton", 
                background=[("active", curTheme.analyticsTabItemBackground),
                            ("disabled", curTheme.analyticsTabDisabledBtnBackground)],
                foreground=[("active", curTheme.ribbonSelectedBtn),
                            ("disabled", curTheme.analyticsTabDisabledBtnTextColor)])

    style.configure("settings_tab_checkbox_button.TButton",
                    background=curTheme.lowerRibbonBackground,
                    foreground=curTheme.lowerRibbonBackground,
                    relief="grove")
    
    style.map("settings_tab_checkbox_button.TButton", 
                background=[("active", curTheme.lowerRibbonBackground)],
                foreground=[("active", curTheme.lowerRibbonBackground)])
        
    style.configure("secondaryButton.TButton", 
                        background=curTheme.bodyBackground,
                        foreground=curTheme.ribbonSelectedBtn,
                        font=(curTheme.fontTypeFace, 
                              textSize.LowerRibbonSectionHeader,
                              "normal"),
                        relief='grove')
    style.map("secondaryButton.TButton", 
                  background=[("active", curTheme.lowerRibbonBackground)])
    
    style.configure("primaryButton.TButton", 
                        background=curTheme.ribbonSelectedBtn,
                        foreground=curTheme.bodyBackground,
                        font=(curTheme.fontTypeFace, 
                              textSize.LowerRibbonSectionHeader,
                              "normal"),
                        relief='grove')
    style.map("primaryButton.TButton", 
                  background=[("active", curTheme.lowerRibbonBackground)])
    
    style.configure("secondaryButtonGray.TButton", 
                        background=curTheme.lowerRibbonUnselectedBtn,
                        foreground=curTheme.upperRibbonTextColor,
                        font=(curTheme.fontTypeFace, 
                              textSize.LowerRibbonSectionHeader,
                              "normal"),
                        relief='grove')
    style.map("secondaryButtonGray.TButton", 
                  background=[("active", curTheme.lowerRibbonBackground)])
    
    style.configure("graph.TButton", 
                    background=curTheme.ribbonSelectedBtn,
                    foreground="white",
                    font=(curTheme.fontTypeFace, 
                    textSize.lowerRibbonTextWidget, 
                    "bold"),
                    relief='grove')
    style.map("graph.TButton", 
                    background=[("active", curTheme.lowerRibbonUnselectedBtn),("disabled", "#C4C4C4")],
                    foreground=[("active", "black"), ("disabled", "#A8A8A8")],
                    relief=[("active", "grove")])
    
    style.configure("graph_unselected.TButton", 
                    background=curTheme.lowerRibbonUnselectedBtn,
                    foreground=curTheme.lowerRibbonTextColor,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonTextWidget, 
                            "bold"),
                    relief='grove')
    
    style.map("graph_unselected.TButton", 
                background=[("active", curTheme.lowerRibbonUnselectedBtn)],
                foreground=[("active", curTheme.ribbonSelectedBtn)])
    
    style.configure("graphDelete.TButton", 
                    background="#EA3333",
                    foreground="white",
                    font=(curTheme.fontTypeFace, 
                    textSize.lowerRibbonBtnFont, 
                    "bold"),
                    relief='grove')
    style.map("graphDelete.TButton", 
                    background=[("active", curTheme.lowerRibbonUnselectedBtn),("disabled", "#C4C4C4")],
                    foreground=[("active", "black"), ("disabled", "#A8A8A8")],
                    relief=[("active", "grove")])
    
    style.configure("graphSelect.TButton",
                    background=curTheme.lowerRibbonUnselectedBtn,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                    textSize.lowerRibbonTextWidget, 
                    "bold"),
                    relief='grove',
                    bordercolor=curTheme.ribbonSelectedBtn,
                    borderwidth=2)
    
    style.configure("select.TButton", 
                    padx=1,
                    background=curTheme.upperRibbonBackground,
                    foreground=curTheme.upperRibbonTextColor, 
                    font=(curTheme.fontTypeFace, 
                    textSize.upperRibbonBtnFont, 
                    "bold"),
                    relief='grove')
    style.map("select.TButton", 
                background=[("active", curTheme.upperRibbonUnselectedBtn)],
                foreground=[("active", curTheme.ribbonSelectedBtn)],
                relief=[("active", "grove")])

    style.configure("addButton.TButton", 
                    background=curTheme.ribbonSelectedBtn,
                    foreground=curTheme.bodyBackground,
                    font=(curTheme.fontTypeFace, 
                            textSize.lowerRibbonBtnFont,
                              "normal"),
                    relief='grove')
    style.map("addButton.TButton", 
                background=[("active", curTheme.lowerRibbonBackground)])
    
    style.configure('Custom.TCombobox', 
                    font=(curTheme.fontTypeFace, 
                          textSize.lowerRibbonNamedCheckboxLabel,
                              "normal"))
    style.map('Custom.TCombobox', 
                fieldbackground=[('readonly', '#ffffff')], 
                background=[('readonly', '#ffffff')], 
                focusfill=[('readonly', '#ffffff')])
    
    style.configure("fliter_chips.TButton", 
                    background=curTheme.bodyBackground,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                          textSize.lowerRibbonTextWidget, "normal"),
                    relief='grove')
    style.map("fliter_chips.TButton", 
                    background=[("active", curTheme.bodyBackground)],
                    foreground=[("active", curTheme.ribbonSelectedBtn)])   
    
    
    style.configure("fliter_chips.TButton", 
                    background=curTheme.bodyBackground,
                    foreground=curTheme.ribbonSelectedBtn,
                    font=(curTheme.fontTypeFace, 
                          textSize.lowerRibbonTextWidget, "normal"),
                    relief='grove')
    style.map("fliter_chips.TButton", 
                    background=[("active", curTheme.bodyBackground)],
                    foreground=[("active", curTheme.ribbonSelectedBtn)])  