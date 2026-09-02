import tkinter as tk
from collections.abc import Callable

import customtkinter as ctk

from src.model.mask import MaskData, MaskDataDict
from src.ui.fonts import MyFonts
from src.ui.tabs.listbox import ListBoxFrame


class MaskFrame(ctk.CTkFrame):
    def __init__(
            self, 
            master, 
            fonts: MyFonts, 
            on_change: Callable[[MaskDataDict], None] | None = None,
        ):
        super().__init__(master, fg_color="transparent")

        # mask data dict
        self.mask_data_dict = MaskDataDict()
        self.on_change = on_change
        self.selected_index: int | None = None

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
        self.clear_button = ctk.CTkButton(self, text="Clear", font=fonts.text_font, command=self.clear_all_entries)
        self.modify_button.grid(row=2, column=0, padx=5)
        self.remove_button.grid(row=2, column=1, padx=5)
        self.add_button.grid(row=2, column=2, padx=5)
        self.clear_button.grid(row=2, column=3, padx=5)

    def modify(self) -> None:
        """modify the selected mask data"""
        # entry fields
        mask = self._get_selected_data()
        if mask is not None:
            self.clear_all_entries()
            self.name_entry.insert(0, mask.name)
            self.gdsii_number_entry.insert(0, mask.gdsii_number)
            self.datatype_entry.insert(0, mask.datatype)
            if mask.invert == 0:
                self.invert_checkbox.deselect()
            else:
                self.invert_checkbox.select()

        # set buttons to modify mode
        self.add_button.configure(text="Update", command=self.update)
        self.clear_button.configure(text="Cancel", command=self.cancel_modify)

    def update(self) -> None:
        """In update mode, update the selected mask data"""
        mask = self._get_entry_data()
        if self.selected_index is not None:
            self.mask_data_dict.insert_data(self.selected_index, mask)
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
        """remove selected mask data from listbox"""
        index = self.listbox_frame._selected_index()
        if index is not None:
            self.mask_data_dict.remove_data(index)
            self.listbox_frame.refresh_listbox()
            self._notify_change()

    def add(self) -> None:
        """add a new mask to listbox"""
        # create a new MaskData
        mask_data = self._get_entry_data()
        
        # append the new mask data
        self.mask_data_dict.append_data(mask_data)
        self.listbox_frame.refresh_listbox()
        self._notify_change()

        # clear the entry fields
        self.clear_all_entries()

    def clear_all_entries(self) -> None:
        """clear all entries"""
        self.name_entry.delete(0, tk.END)
        self.gdsii_number_entry.delete(0, tk.END)
        self.datatype_entry.delete(0, tk.END)
        self.invert_checkbox.deselect()

    def _get_entry_data(self) -> MaskData:
        """return MaskData from entries"""
        return MaskData(name=self.name_entry.get(),
                        gdsii_number=self.gdsii_number_entry.get(),
                        datatype=self.datatype_entry.get(),
                        invert=self.invert_checkbox.get())
    
    def _get_selected_data(self) -> MaskData | None:
        """return selected MaskData from listbox"""
        self.selected_index = self.listbox_frame._selected_index()
        if self.selected_index is not None:
            mask = self.mask_data_dict[f"{self.selected_index}"]
            return mask

    def get_data(self) -> MaskDataDict:
        """return the mask data dict"""
        return self.mask_data_dict

    def _notify_change(self) -> None:
        if self.on_change is not None:
            self.on_change(self.mask_data_dict)

    def set_data(self, mask_data_dict: MaskDataDict) -> None:
        """set the mask data dict"""
        for mask_data in mask_data_dict.values():
            self.mask_data_dict.append_data(mask_data)
            
        self.listbox_frame.refresh_listbox()