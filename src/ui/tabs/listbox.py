import customtkinter as ctk
from CTkListbox import CTkListbox

from src.model.basic import DataDict
from src.ui.fonts import MyFonts


class ListBoxFrame(ctk.CTkFrame):
    def __init__(self, master, fonts: MyFonts, data_dict: DataDict):
        super().__init__(master)

        # Dict data
        self.data_dict = data_dict

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        # listbox
        self.listbox = CTkListbox(self)
        self.listbox.configure(font=fonts.text_font)
        self.listbox.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # buttons
        self.up_button = ctk.CTkButton(self, text="Up", font=fonts.text_font, command=self.move_up)
        self.down_button = ctk.CTkButton(self, text="Down", font=fonts.text_font, command=self.move_down)
        self.up_button.grid(row=1, column=0, padx=(0, 5))
        self.down_button.grid(row=1, column=1, padx=(5, 0))

    def _selected_index(self) -> int | None:
        index = self.listbox.curselection()
        if index is None:
            return None
        if isinstance(index, tuple):
            return index[0]
        if isinstance(index, int):
            return index

    def move_up(self):
        index = self._selected_index()
        if index is not None and index > 0:
            self.listbox.move_up(index)
            self.data_dict.swap_data(index, index-1)
        
    def move_down(self):
        index = self._selected_index()
        if index is not None and index < self.listbox.size() - 1:
            self.listbox.move_down(index)
            self.data_dict.swap_data(index, index+1)

    def refresh_listbox(self):
        self.listbox.delete("all")
        for index, data in self.data_dict.items():
            self.listbox.insert(f"{index}", data.option_string())
