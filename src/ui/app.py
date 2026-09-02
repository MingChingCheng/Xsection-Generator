from tkinter import messagebox

import customtkinter as ctk

from src.service.code_generator import CodeGenerator
from src.service.project_saver import ProjectSaver
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
        self.menu_bar = MenuBar(self,
                                open_command=self.open_project, 
                                save_as_command=self.save_project_as)

        # Tab view
        self.tabview = TabView(self, fonts, export_xs_file=self.export_xs_file)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        for button in self.tabview._segmented_button._buttons_dict.values():
            button.configure(font=fonts.tab_font, border_spacing=6, width=120)

    def export_xs_file(self) -> None:
        _ = CodeGenerator(
            project_data=self.tabview.get_project_data(),
            mask_data_dict=self.tabview.get_mask_data(),
            material_data_dict=self.tabview.get_material_data(),
            process_data_dict=self.tabview.get_process_data(),
            output_data=self.tabview.get_output_data()
        )

        # show a message box to inform file has been exported
        messagebox.showinfo("Export", "File has been exported successfully.")
        
    def save_project_as(self) -> None:
        # export the data to a json file
        project_saver = ProjectSaver(all_data=self.tabview.get_all_data())
        
        file_name_with_path = ctk.filedialog.asksaveasfilename(title="Save Project ...", 
                                                               defaultextension=".json", 
                                                               filetypes=[("JSON files", "*.json")])

        project_saver.save_project_as_json(file_name_with_path)

    def open_project(self) -> None:
        # read the data from a json file
        file_name_with_path = ctk.filedialog.askopenfilename(
            title="Open Project ...",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )

        if file_name_with_path:
            project_saver = ProjectSaver()
            project_saver.read_project_from_json(file_name_with_path)
            print("Project data read from JSON:")
            print("Project Data:", project_saver.project_data)
            print("Mask Data Dict:", project_saver.mask_data_dict)
            print("Material Data Dict:", project_saver.material_data_dict)
            print("Process Data Dict:", project_saver.process_data_dict)
            print("Output Data:", project_saver.output_data)
