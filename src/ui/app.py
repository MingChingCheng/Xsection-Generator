import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from src.model.basic import Data, DataDict
from src.service.code_generator import CodeGenerator
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
        self.tabview = TabView(self, fonts, export_xs_file=self.export_xs_file)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        for button in self.tabview._segmented_button._buttons_dict.values():
            button.configure(font=fonts.tab_font, border_spacing=6, width=120)

    def get_all_data(self) -> dict[str, Data | DataDict]:
        data = {"project": self.tabview.get_project_data(),
                "mask": self.tabview.get_mask_data()}
        
        return data

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
        
    # def export_file_with_data(self) -> None:
        # # export the data to a json file
        # project_data: ProjectData = self.tabview.get_project_data()

        # nested_dict = {}
        # nested_dict["project"] = asdict(project_data)

        # path = data["output"].path[0:-1]
        # file_name_with_path = os.path.join(path, data["project"].project_name + ".json")
        # with open(file_name_with_path, "w", encoding="utf-8") as f:
        #     json.dump(nested_dict, f, indent=4)
