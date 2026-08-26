import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from src.model.output import OutputData
from src.ui.fonts import MyFonts


class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, fonts: MyFonts):
        super().__init__(master, fg_color="transparent")

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        # entry frame
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.entry_frame.grid(row=0, column=0, rowspan=5, columnspan=4, sticky="nsew", padx=5, pady=5)

        ## output path
        self.path_label = ctk.CTkLabel(
            self.entry_frame, font=fonts.text_font, text="Output Path: "
        )
        self.path_textbox = ctk.CTkTextbox(
            self.entry_frame,
            font=fonts.text_font,
            wrap="none",
            state="disabled",
            height=0,
        )
        self.path_button = ctk.CTkButton(
            self.entry_frame,
            font=fonts.text_font,
            text="Choose Folder",
            command=self.choose_folder,
        )
        self.path_description = ctk.CTkLabel(
            self.entry_frame,
            font=fonts.desc_font,
            text="Set the output path for the generated file. ",
            text_color="dimgray",
        )
        self.path_label.grid(row=0, column=0, padx=5, sticky="w")
        self.path_textbox.grid(row=1, column=0, columnspan=3, padx=5, sticky="ew")
        self.path_button.grid(row=1, column=3, padx=5, sticky="w")
        self.path_description.grid(row=2, column=0, columnspan=3, padx=5, sticky="w")

        ## step checkbox
        self.step_checkbox = ctk.CTkCheckBox(
            self.entry_frame, font=fonts.text_font, text="Display all steps"
        )
        self.step_description = ctk.CTkLabel(
            self.entry_frame,
            font=fonts.desc_font,
            text="Check this option to display all steps in the output. ",
            text_color="dimgray",
        )
        self.step_checkbox.grid(row=3, column=0, columnspan=3, padx=5, sticky="w")
        self.step_description.grid(row=4, column=0, columnspan=3, padx=5, sticky="w")

        # export button
        self.export_button = ctk.CTkButton(self, font=fonts.text_font, text="Export File !", command=self.export)
        self.export_button.grid(row=1, column=1, padx=5, pady=5, sticky="es")

    def choose_folder(self) -> str:
        path = filedialog.askdirectory(title="Select Output Folder")
        self.path_textbox.configure(state="normal")
        self.path_textbox.delete("0.0", "end")
        self.path_textbox.insert("0.0", path)
        self.path_textbox.configure(state="disabled")

        print("Selected Output Path:", path)
        return path

    def export(self) -> None:
        ...
        
    def get_data(self) -> OutputData:
        return OutputData(
            path=self.path_textbox.get("0.0", "end"),
            steps=self.step_checkbox.get()
        )
