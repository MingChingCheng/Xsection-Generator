import customtkinter as ctk

from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.process import ProcessDataDict
from src.model.project import ProjectData
from src.ui.tabs.mask import MaskFrame
from src.ui.tabs.material import MaterialFrame
from src.ui.tabs.process import ProcessFrame
from src.ui.tabs.project import ProjectFrame


class TabView(ctk.CTkTabview):
    def __init__(self, master, fonts):
        super().__init__(master)

        # create tabs
        self.tab_names = [
            "Project",
            "Mask",
            "Material",
            "Process",
            "Output",
        ]
        self.tabs = []

        for name in self.tab_names:
            new_tab = self.add(name)
            new_tab.grid_rowconfigure(0, weight=1)
            new_tab.grid_columnconfigure(0, weight=1)
            self.tabs.append(new_tab)

        # insert frames to each tab
        self.project_frame = ProjectFrame(self.tabs[0], fonts)
        self.project_frame.grid(row=0, column=0, sticky="nsew")

        self.mask_frame = MaskFrame(self.tabs[1], fonts)
        self.mask_frame.grid(row=0, column=0, sticky="nsew")

        self.material_frame = MaterialFrame(
            self.tabs[2],
            fonts,
            on_change=self._update_process_material_data,
        )
        self.material_frame.grid(row=0, column=0, sticky="nsew")

        self.process_frame = ProcessFrame(
            self.tabs[3],
            fonts,
            mask_data_dict=self.mask_frame.get_data(),
            material_data_dict=self.material_frame.get_data(),
        )
        self.process_frame.grid(row=0, column=0, sticky="nsew")

        # self.output_frame = OutputFrame(self.tabs[3], fonts)
        # self.output_frame.grid(row=0, column=0, sticky="nsew")

    def get_project_data(self) -> ProjectData:
        return self.project_frame.get_data()

    def get_mask_data(self) -> MaskDataDict:
        return self.mask_frame.get_data()

    def get_material_data(self) -> MaterialDataDict:
        return self.material_frame.get_data()

    def get_process_data(self) -> ProcessDataDict:
        return self.process_frame.get_data()

    def _update_process_material_data(self, material_data_dict: MaterialDataDict) -> None:
        self.process_frame.update_material_data(material_data_dict)