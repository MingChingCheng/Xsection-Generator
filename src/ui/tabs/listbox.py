import customtkinter as ctk
from CTkListbox import CTkListbox

from src.ui.fonts import MyFonts


class ListBoxFrame(ctk.CTkFrame):
    def __init__(self, master, fonts: MyFonts):
        super().__init__(master)

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


    def move_up(self):
        index = self.listbox.curselection()
        self.listbox.move_up(index)

    def move_down(self):
        index = self.listbox.curselection()
        self.listbox.move_down(index)

    def delete_selected(self):
        index = self.listbox.curselection()
        self.listbox.delete(index)

    def delete_all(self):
        self.listbox.delete("all")
