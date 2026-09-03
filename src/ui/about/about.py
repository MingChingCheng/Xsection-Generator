import customtkinter as ctk

from src.ui.fonts import MyFonts
from src.version import __version__


class AboutWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        fonts = MyFonts()

        self.title_label = ctk.CTkLabel(self, text="Xsection Generator", font=fonts.tab_font)
        self.version_label = ctk.CTkLabel(self, text=f"Version: {__version__}", font=fonts.text_font)
        
        