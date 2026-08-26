import tkinter as tk
from collections.abc import Callable

import customtkinter as ctk

from src.model.material import MaterialData, MaterialDataDict
from src.ui.fonts import MyFonts
from src.ui.tabs.listbox import ListBoxFrame


class MaterialFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        fonts: MyFonts,
        on_change: Callable[[MaterialDataDict], None] | None = None,
    ):
        super().__init__(master, fg_color="transparent")

        # material data dict
        self.material_data_dict = MaterialDataDict()
        self.on_change = on_change
        self.selected_index: int | None = None

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # listbox frame
        self.listbox_frame = ListBoxFrame(self, fonts, self.material_data_dict)
        self.listbox_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.listbox_frame.refresh_listbox()

        # entry frame
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.name_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Material Name: ")
        self.name_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: Oxide, PZT, ...",)
        self.name_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the name of material. ", text_color="dimgray",)
        self.name_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="e")
        self.name_entry.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="we")
        self.name_description.grid(row=1, column=0, columnspan=2, padx=5, sticky="e")

        self.gdsii_number_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="GDSII Number: ")
        self.gdsii_number_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 1, 20, ...")
        self.gdsii_number_description = ctk.CTkLabel(
            self.entry_frame,
            font=fonts.desc_font,
            text="Set the GDSII number of material. \n Affect to the color displayed by KLayout. ",
            text_color="dimgray",
            justify="right",
        )
        self.gdsii_number_label.grid(row=2, column=0, padx=5, sticky="e")
        self.gdsii_number_entry.grid(row=2, column=1, padx=5, sticky="we")
        self.gdsii_number_description.grid(row=3, column=0, columnspan=2, padx=5, sticky="e")

        # buttons
        self.modify_button = ctk.CTkButton(self, text="Modify", font=fonts.text_font, command=self.modify)
        self.remove_button = ctk.CTkButton(self, text="Remove", font=fonts.text_font, command=self.remove)
        self.add_button = ctk.CTkButton(self, text="Add", font=fonts.text_font, command=self.add)
        self.clear_button = ctk.CTkButton(self, text="Clear", font=fonts.text_font, command=self.clear_all_entries)
        self.modify_button.grid(row=2, column=0, padx=5)
        self.remove_button.grid(row=2, column=1, padx=5)
        self.add_button.grid(row=2, column=2, padx=5)
        self.clear_button.grid(row=2, column=3, padx=5)

    def modify(self) -> None:
        """modify the selected material data"""
        # entry fields
        material = self._get_selected_data()
        if material is not None:
            self.clear_all_entries()
            self.name_entry.insert(0, material.name)
            self.gdsii_number_entry.insert(0, material.gdsii_number)

        # set buttons to modify mode
        self.add_button.configure(text="Update", command=self.update)
        self.clear_button.configure(text="Cancel", command=self.cancel_modify)

    def update(self) -> None:
        """In update mode, update the selected data"""
        material = self._get_entry_data()
        if self.selected_index is not None:
            self.material_data_dict.insert_data(self.selected_index, material)
            self.listbox_frame.refresh_listbox()
            self._notify_change()

        # set buttons back to add mode
        self.clear_all_entries()
        self.add_button.configure(text="Add", command=self.add)
        self.clear_button.configure(text="Clear", command=self.clear_all_entries)

    def cancel_modify(self) -> None:
        """In modify mode, back to add mode"""
        # clear entry fields
        self.clear_all_entries()

        # set buttons back to add mode
        self.add_button.configure(text="Add", command=self.add)
        self.clear_button.configure(text="Clear", command=self.clear_all_entries)

    def remove(self) -> None:
        """remove selected data from listbox"""
        index = self.listbox_frame._selected_index()
        if index is not None:
            self.material_data_dict.remove_data(index)
            self.listbox_frame.refresh_listbox()
            self._notify_change()

    def add(self) -> None:
        """add a new to listbox"""
        # create a new MaterialData
        material_data = self._get_entry_data()

        # append the new material data
        self.material_data_dict.append_data(material_data)
        self.listbox_frame.refresh_listbox()
        self._notify_change()

        # clear the entry fields
        self.clear_all_entries()

    def clear_all_entries(self) -> None:
        """clear all entries"""
        self.name_entry.delete(0, tk.END)
        self.gdsii_number_entry.delete(0, tk.END)

    def _get_entry_data(self) -> MaterialData:
        """return MaterialData from entries"""
        return MaterialData(
            name=self.name_entry.get(),
            gdsii_number=self.gdsii_number_entry.get(),
        )

    def _get_selected_data(self) -> MaterialData | None:
        """return selected MaterialData from listbox"""
        self.selected_index = self.listbox_frame._selected_index()
        if self.selected_index is not None:
            material = self.material_data_dict[f"{self.selected_index}"]
            return material

    def get_data(self) -> MaterialDataDict:
        """return the material data dict"""
        return self.material_data_dict

    def _notify_change(self) -> None:
        if self.on_change is not None:
            self.on_change(self.material_data_dict)
