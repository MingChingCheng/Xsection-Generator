import customtkinter as ctk

from src.ui.fonts import MyFonts
from src.version import __version__


class AboutWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window
        self.geometry("300x200")
        fonts = MyFonts()

        self.grid_columnconfigure(0, weight=1)

        # labels
        self.title_label = ctk.CTkLabel(self, text=f"Xsection Generator {__version__}", font=fonts.tab_font)
        self.author_label = ctk.CTkLabel(self, text="Author: Ming-Ching, Cheng", font=fonts.desc_font)
        self.description_label = ctk.CTkLabel(self, text="A tool for generating cross-section code.", font=fonts.desc_font)

        self.title_label.grid(row=0, column=0, pady=(20, 10))
        self.author_label.grid(row=2, column=0, padx=10)
        self.description_label.grid(row=3, column=0, pady=(0, 10))
            