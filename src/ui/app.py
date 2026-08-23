import customtkinter as ctk

from src.ui.fonts import MyFonts
from src.ui.menu_bar import MenuBar
from src.ui.tabview import TabView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window
        self.title("Xsection Generator")
        self.geometry("600x400")

        self.grid_rowconfigure(0, weight=0)       # for menu bar
        self.grid_rowconfigure(1, weight=1)       # for tab view
        self.grid_columnconfigure(0, weight=1)    # for tab view
        
        # Font
        fonts = MyFonts()

        # Menubar
        self.menu_bar = MenuBar(self)

        # Tab view
        self.tabview = TabView(self, fonts)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        for button in self.tabview._segmented_button._buttons_dict.values():
            button.configure(font=fonts.tab_font, border_spacing=6, width=120)

    def get_all_data(self) -> dict:
        data = {"project": self.tabview.get_project_data(),
                "mask": self.tabview.get_mask_data()}
        
        return data