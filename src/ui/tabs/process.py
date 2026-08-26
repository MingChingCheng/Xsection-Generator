import tkinter as tk

import customtkinter as ctk

from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.process import ProcessData, ProcessDataDict
from src.ui.fonts import MyFonts
from src.ui.tabs.listbox import ListBoxFrame


class ProcessFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        fonts: MyFonts,
        mask_data_dict: MaskDataDict,
        material_data_dict: MaterialDataDict,
    ):
        super().__init__(master, fg_color="transparent")

        # process data dict
        self.mask_data_dict = mask_data_dict
        self.material_data_dict = material_data_dict
        self.process_data_dict = ProcessDataDict()
        self.selected_index: int | None = None

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # listbox frame
        self.listbox_frame = ListBoxFrame(self, fonts, self.process_data_dict)
        self.listbox_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # entry frame
        self.entry_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.name_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Process Name: ")
        self.name_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: Process_1, Deposit PE oxide, ...",)
        self.name_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the name of process. ", text_color="dimgray",)
        self.name_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="e")
        self.name_entry.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="we")
        self.name_description.grid(row=1, column=0, columnspan=2, padx=5, sticky="e")

        self.type_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Type: ")
        self.type_optionmenu = ctk.CTkOptionMenu(self.entry_frame, font=fonts.text_font, values=["", "Deposit", "Grow", "Etch"])
        self.type_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Select the type of process. ", text_color="dimgray",)
        self.type_label.grid(row=2, column=0, padx=5, sticky="e")
        self.type_optionmenu.grid(row=2, column=1, padx=5, sticky="we")
        self.type_description.grid(row=3, column=0, columnspan=2, padx=5, sticky="e")

        self.mask_options = [
            mask_data.option_string() for mask_data in self.mask_data_dict.values()
        ] or ["No mask"]
        self.mask_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Mask: ")
        self.mask_optionmenu = ctk.CTkOptionMenu(
            self.entry_frame, 
            font=fonts.text_font, 
            values=self.mask_options
            )
        self.mask_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Select the mask for the process. Only valid for 'Grow' and 'Etch' ", text_color="dimgray",)
        self.mask_label.grid(row=4, column=0, padx=5, sticky="e")
        self.mask_optionmenu.grid(row=4, column=1, padx=5, sticky="we")
        self.mask_description.grid(row=5, column=0, columnspan=2, padx=5, sticky="e")

        self.material_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Material: ")
        self.material_scrollable_frame = CheckList(self.entry_frame, fonts, self.material_data_dict)
        self.material_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Select the material to be deposited/grown or etched. ", text_color="dimgray",)
        self.material_label.grid(row=6, column=0, padx=5, sticky="ne")
        self.material_scrollable_frame.grid(row=6, column=1, padx=5, sticky="we")
        self.material_description.grid(row=7, column=0, columnspan=2, padx=5, sticky="e")

        self.ignore_material_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Ignored Material: ")
        self.ignore_material_scrollable_frame = CheckList(self.entry_frame, fonts, self.material_data_dict)
        self.ignore_material_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Select the material to be ignored for deposition/grown or etched. ", text_color="dimgray",)
        self.ignore_material_label.grid(row=8, column=0, padx=5, sticky="ne")
        self.ignore_material_scrollable_frame.grid(row=8, column=1, padx=5, sticky="we")
        self.ignore_material_description.grid(row=9, column=0, columnspan=2, padx=5, sticky="e")

        self.vertical_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Vertical (um): ")
        self.vertical_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 1")
        self.vertical_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the vertical thickness of process. Default = 1. ", text_color="dimgray",)
        self.vertical_label.grid(row=10, column=0, padx=5, sticky="e")
        self.vertical_entry.grid(row=10, column=1, padx=5, sticky="we")
        self.vertical_description.grid(row=11, column=0, columnspan=2, padx=5, sticky="e")

        self.horizontal_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Horizontal (um): ")
        self.horizontal_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 0")
        self.horizontal_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the horizontal thickness of process. Default = 0. ", text_color="dimgray",)
        self.horizontal_label.grid(row=12, column=0, padx=5, sticky="e")
        self.horizontal_entry.grid(row=12, column=1, padx=5, sticky="we")
        self.horizontal_description.grid(row=13, column=0, columnspan=2, padx=5, sticky="e")

        self.angle_label = ctk.CTkLabel(self.entry_frame, font=fonts.text_font, text="Angle (deg): ")
        self.angle_entry = ctk.CTkEntry(self.entry_frame, font=fonts.text_font, placeholder_text="e.g.: 0")
        self.angle_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Set the angle of process. Measured respect to the vertical line. Default = 0. ", text_color="dimgray",)
        self.angle_label.grid(row=14, column=0, padx=5, sticky="e")
        self.angle_entry.grid(row=14, column=1, padx=5, sticky="we")
        self.angle_description.grid(row=15, column=0, columnspan=2, padx=5, sticky="e")

        self.backside_checkbox = ctk.CTkCheckBox(self.entry_frame, font=fonts.text_font, text="Backside")
        self.backside_description = ctk.CTkLabel(self.entry_frame, font=fonts.desc_font, text="Check to apply the backside process. ", text_color="dimgray",)
        self.backside_checkbox.grid(row=16, column=1, padx=5, sticky="w")
        self.backside_description.grid(row=17, column=0, columnspan=2, padx=5, sticky="e")

        # buttons
        self.modify_button = ctk.CTkButton(self, text="Modify", font=fonts.text_font, command=self.modify)
        self.remove_button = ctk.CTkButton(self, text="Remove", font=fonts.text_font, command=self.remove)
        self.add_button = ctk.CTkButton(self, text="Add", font=fonts.text_font, command=self.add)
        self.clear_button = ctk.CTkButton(self, text="Clear", font=fonts.text_font, command=self.clear_all_entries)
        self.modify_button.grid(row=2, column=0, padx=5)
        self.remove_button.grid(row=2, column=1, padx=5)
        self.add_button.grid(row=2, column=2, padx=5)
        self.clear_button.grid(row=2, column=3, padx=5)

    def modify(self): ...
    def remove(self): ...

    # def modify(self) -> None:
    #     """modify the selected mask data"""
    #     # entry fields
    #     mask = self._get_selected_data()
    #     if mask is not None:
    #         self.clear_all_entries()
    #         self.name_entry.insert(0, mask.name)
    #         self.gdsii_number_entry.insert(0, mask.gdsii_number)
    #         self.datatype_entry.insert(0, mask.datatype)
    #         if mask.invert == 0:
    #             self.invert_checkbox.deselect()
    #         else:
    #             self.invert_checkbox.select()

    #     # set buttons to modify mode
    #     self.add_button.configure(text="Update", command=self.update)
    #     self.clear_button.configure(text="Cancel", command=self.cancel_modify)

    # def update(self) -> None:
    #     """In update mode, update the selected mask data"""
    #     mask = self._get_entry_data()
    #     if self.selected_index is not None:
    #         self.mask_data_dict.insert_data(self.selected_index, mask)
    #         self.listbox_frame.refresh_listbox()

    #     # set buttons back to add mode
    #     self.clear_all_entries()
    #     self.add_button.configure(text="Add", command=self.add)
    #     self.clear_button.configure(text="Clear", command=self.clear_all_entries)

    # def cancel_modify(self) -> None:
    #     """In modify mode, back to add mode"""
    #     # clear entry fields
    #     self.clear_all_entries()

    #     # set buttons back to add mode
    #     self.add_button.configure(text="Add", command=self.add)
    #     self.clear_button.configure(text="Clear", command=self.clear_all_entries)

    # def remove(self) -> None:
    #     """remove selected mask data from listbox"""
    #     index = self.listbox_frame._selected_index()
    #     if index is not None:
    #         self.mask_data_dict.remove_data(index)
    #         self.listbox_frame.refresh_listbox()

    def add(self) -> None:
        """add a new process to listbox"""
        # create a new ProcessData
        process_data = self._get_entry_data()

        # append the new mask data
        self.process_data_dict.append_data(process_data)
        self.listbox_frame.refresh_listbox()

        # clear the entry fields
        self.clear_all_entries()

    def clear_all_entries(self) -> None:
        """clear all entries"""
        self.name_entry.delete(0, tk.END)
        self.type_optionmenu.set("")
        self.mask_optionmenu.set("No mask")
        self.material_scrollable_frame.clear_selection()
        self.ignore_material_scrollable_frame.clear_selection()
        self.vertical_entry.delete(0, tk.END)
        self.horizontal_entry.delete(0, tk.END)
        self.angle_entry.delete(0, tk.END)
        self.backside_checkbox.deselect()

    def _get_entry_data(self) -> ProcessData:
        """return ProcessData from entries"""
        return ProcessData(
            name=self.name_entry.get(),
            type=self.type_optionmenu.get(),
            mask=self.mask_optionmenu.get(),
            material=self.material_scrollable_frame.get_selected_items(),
            ignore_material=self.ignore_material_scrollable_frame.get_selected_items(),
            vertical=self.vertical_entry.get(),
            horizontal=self.horizontal_entry.get(),
            angle=self.angle_entry.get(),
            backside=self.backside_checkbox.get(),
        )

    # def _get_selected_data(self) -> MaskData | None:
    #     """return selected MaskData from listbox"""
    #     self.selected_index = self.listbox_frame._selected_index()
    #     if self.selected_index is not None:
    #         mask = self.mask_data_dict[f"{self.selected_index}"]
    #         return mask

    def get_data(self) -> ProcessDataDict:
        """return the mask data dict"""
        return self.process_data_dict

    def update_mask_data(self, mask_data_dict: MaskDataDict) -> None:
        """update the mask data dict"""
        self.mask_data_dict = mask_data_dict
        mask_options = []
        for mask in self.mask_data_dict.values():
            mask_options.append(mask.option_string())

        self.mask_optionmenu.configure(values=mask_options)

    def update_material_data(self, material_data_dict: MaterialDataDict) -> None:
        """update the material data dict"""
        self.material_data_dict = material_data_dict
        self.material_scrollable_frame.update_items(material_data_dict)
        self.ignore_material_scrollable_frame.update_items(material_data_dict)

    

class CheckList(ctk.CTkScrollableFrame):
    def __init__(self, master, fonts: MyFonts, material_data_dict: MaterialDataDict):
        super().__init__(master, fg_color="Silver", height=100)
        self.fonts = fonts
        self.material_data_dict = material_data_dict
        self._scrollbar.configure(height=0)

        self.checkboxes = []
        for i, item in enumerate(self.get_material_data_names()):
            checkbox = ctk.CTkCheckBox(self, font=fonts.text_font, text=item)
            checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.checkboxes.append(checkbox)

    def get_material_data_names(self) -> list[str]:
        names = []
        for material in self.material_data_dict.values():
            names.append(material.name)
        return names

    def get_selected_items(self) -> list[str]:
        """return the selected items"""
        selected_items = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                selected_items.append(checkbox.cget("text"))
        return selected_items

    def update_items(self, material_data_dict: MaterialDataDict) -> None:
        """Refresh the checklist while keeping selections for existing items."""
        self.material_data_dict = material_data_dict
        selected_items = set(self.get_selected_items())
        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.checkboxes = []
        for i, item in enumerate(self.get_material_data_names()):
            checkbox = ctk.CTkCheckBox(self, font=self.fonts.text_font, text=item)
            checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            if item in selected_items:
                checkbox.select()
            self.checkboxes.append(checkbox)

    def clear_selection(self) -> None:
        """Clear all selections in the checklist."""
        for checkbox in self.checkboxes:
            checkbox.deselect()