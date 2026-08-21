import customtkinter as ctk


class MyFonts:
    def __init__(self):
        # Default font
        self.default_font = ctk.CTkFont(family="Roboto", size=13)

        # Tab
        self.tab_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")

        # Text
        self.text_font = ctk.CTkFont(family="Roboto", size=14)

        # Description
        self.desc_font = ctk.CTkFont(family="Roboto", size=12, slant="italic")