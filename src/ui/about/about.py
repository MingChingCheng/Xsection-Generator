import customtkinter as ctk

from src.ui.fonts import MyFonts
from src.version import __version__


class AboutWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window
        self.geometry("300x150")
        fonts = MyFonts()

        self.grid_columnconfigure(0, weight=1)

        # labels
        self.title_label = ctk.CTkLabel(self, text=f"Xsection Generator {__version__}", font=fonts.tab_font)

        info = "Copyright (c) 2026 Ming-Ching Cheng \n" \
               "This software is released under the MIT License. "

        self.author_label = ctk.CTkLabel(
            self, text=info, font=fonts.desc_font, text_color="gray"
        )

        self.title_label.grid(row=0, column=0, pady=(20, 10))
        self.author_label.grid(row=2, column=0, padx=10)

        # button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=4, column=0, pady=(20, 10))

