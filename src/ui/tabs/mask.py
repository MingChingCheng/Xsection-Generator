import tkinter as tk

import customtkinter as ctk

from src.model.mask import MaskData, MaskDataDict
from src.ui.fonts import MyFonts
from src.ui.tabs.listbox import ListBoxFrame


class MaskFrame(ctk.CTkFrame):
    def __init__(self, master, fonts: MyFonts):
        super().__init__(master, fg_color="transparent")

        # mask data dict
        self.mask_data_dict = MaskDataDict()

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # listbox frame
        self.listbox_frame = ListBoxFrame(self, fonts, self.mask_data_dict)
        self.listbox_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # entry frame
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.name_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Mask Name: ")
        self.name_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: Mask_1, oxide, ...")
        self.name_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the name of mask. ", text_color="dimgray")
        self.name_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="e")
        self.name_entry.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="we")
        self.name_description.grid(row=1, column=0, columnspan=2, padx=5, sticky="e")

        self.gdsii_number_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="GDSII Number: ")
        self.gdsii_number_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 1, 20, ...")
        self.gdsii_number_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the GDSII number of mask. ", text_color="dimgray")
        self.gdsii_number_label.grid(row=2, column=0, padx=5, sticky="e")
        self.gdsii_number_entry.grid(row=2, column=1, padx=5, sticky="we")
        self.gdsii_number_description.grid(row=3, column=0, columnspan=2, padx=5, sticky="e")

        self.datatype_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Datatype: ")
        self.datatype_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 0, 1, ...")
        self.datatype_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set datatype of mask, default = 0. ", text_color="dimgray")
        self.datatype_label.grid(row=4, column=0, padx=5, sticky="e")
        self.datatype_entry.grid(row=4, column=1, padx=5, sticky="we")
        self.datatype_description.grid(row=5, column=0, columnspan=2, padx=5, sticky="e")

        self.invert_checkbox = ctk.CTkCheckBox(self.entry_frame, font=fonts.text_font, text="Invert")
        self.invert_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Check to invert the tone of mask. ", text_color="dimgray")
        self.invert_checkbox.grid(row=6, column=1, padx=5, sticky="w")
        self.invert_description.grid(row=7, column=0, columnspan=2, padx=5, sticky="e")

        # buttons
        self.modify_button = ctk.CTkButton(self, text="Modify", font=fonts.text_font, command=self.modify)
        self.remove_button = ctk.CTkButton(self, text="Remove", font=fonts.text_font, command=self.remove)
        self.add_button = ctk.CTkButton(self, text="Add", font=fonts.text_font, command=self.add)
        self.clear_button = ctk.CTkButton(self, text="Clear", font=fonts.text_font, command=self.clear)
        self.modify_button.grid(row=2, column=0, padx=5)
        self.remove_button.grid(row=2, column=1, padx=5)
        self.add_button.grid(row=2, column=2, padx=5)
        self.clear_button.grid(row=2, column=3, padx=5)

    def modify(self):
        ...

    def remove(self):
        """print dict data temporarily"""
        index = self.listbox_frame._selected_index()
        if index is not None:
            self.mask_data_dict.remove_data(index)
            self.listbox_frame.refresh_listbox()

    def add(self):
        """add a new mask to listbox"""

        # create a new MaskData
        mask_data = self._get_entry_data()
        
        # append the new mask data
        self.mask_data_dict.append_data(mask_data)
        self.listbox_frame.refresh_listbox()

        # clear the entry fields
        self.clear()

    def clear(self):
        """clear all entries"""
        self.name_entry.delete(0, tk.END)
        self.gdsii_number_entry.delete(0, tk.END)
        self.datatype_entry.delete(0, tk.END)
        self.invert_checkbox.deselect()

    def _get_entry_data(self) -> MaskData:
        return MaskData(name=self.name_entry.get(),
                        gdsii_number=self.gdsii_number_entry.get(),
                        datatype=self.datatype_entry.get(),
                        invert=self.invert_checkbox.get())
    
    def _get_selected_data(self) -> MaskData:
        ...

    def _print_mask_data_dict(self):
        print("Current mask data dict:")
        for _ in self.mask_data_dict:
            print(f"{_}: {self.mask_data_dict[_]}")
        print("-------------------------------")

    def get_data(self) -> MaskDataDict:
        return self.mask_data_dict