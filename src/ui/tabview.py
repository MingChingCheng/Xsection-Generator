from collections.abc import Callable

import customtkinter as ctk

from service.project_saver import ProjectSaver
from src.model.basic import Data, DataDict
from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.output import OutputData
from src.model.process import ProcessDataDict
from src.model.project import ProjectData
from src.ui.tabs.mask import MaskFrame
from src.ui.tabs.material import MaterialFrame
from src.ui.tabs.output import OutputFrame
from src.ui.tabs.process import ProcessFrame
from src.ui.tabs.project import ProjectFrame


class TabView(ctk.CTkTabview):
    def __init__(self, master, fonts, export_xs_file: Callable):
        super().__init__(master)
        self.export_xs_file = export_xs_file

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

        self.mask_frame = MaskFrame(
            self.tabs[1], 
            fonts,
            on_change=self._update_mask_process_data,
        )
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

        self.output_frame = OutputFrame(
            self.tabs[4], fonts, on_export=self._export_xs_file
        )
        self.output_frame.grid(row=0, column=0, sticky="nsew")

    def get_project_data(self) -> ProjectData:
        return self.project_frame.get_data()

    def set_project_data(self, project_data: ProjectData) -> None:
        self.project_frame.set_data(project_data)

    def get_mask_data(self) -> MaskDataDict:
        return self.mask_frame.get_data()

    def set_mask_data(self, mask_data_dict: MaskDataDict) -> None:
        self.mask_frame.set_data(mask_data_dict)
        self.process_frame.update_mask_data(mask_data_dict)

    def get_material_data(self) -> MaterialDataDict:
        return self.material_frame.get_data()

    def set_material_data(self, material_data_dict: MaterialDataDict) -> None:
        self.material_frame.set_data(material_data_dict)
        self.process_frame.update_material_data(material_data_dict)

    def get_process_data(self) -> ProcessDataDict:
        return self.process_frame.get_data()

    def set_process_data(self, process_data_dict: ProcessDataDict) -> None:
        self.process_frame.set_data(process_data_dict)

    def get_output_data(self) -> OutputData:
        return self.output_frame.get_data()

    def set_output_data(self, output_data: OutputData) -> None:
        self.output_frame.set_data(output_data)
    
    def get_all_data(self) -> dict[str, Data | DataDict]:
        return {
            "project": self.get_project_data(),
            "mask": self.get_mask_data(),
            "material": self.get_material_data(),
            "process": self.get_process_data(),
            "output": self.get_output_data()
        }

    def set_all_data(self, project_saver: ProjectSaver) -> None:
        """Set all data in the tabview using a ProjectSaver instance."""
        # project frame
        if isinstance(project_saver.project_data, ProjectData):
            self.set_project_data(project_saver.project_data)
        # mask frame
        if isinstance(project_saver.mask_data_dict, MaskDataDict):
            self.set_mask_data(project_saver.mask_data_dict)
        # material frame
        if isinstance(project_saver.material_data_dict, MaterialDataDict):
            self.set_material_data(project_saver.material_data_dict)
        # process frame
        if isinstance(project_saver.process_data_dict, ProcessDataDict):
            self.set_process_data(project_saver.process_data_dict)
        # output frame
        if isinstance(project_saver.output_data, OutputData):
            self.set_output_data(project_saver.output_data)

    def _update_mask_process_data(self, mask_data_dict: MaskDataDict) -> None:
        self.process_frame.update_mask_data(mask_data_dict)

    def _update_process_material_data(self, material_data_dict: MaterialDataDict) -> None:
        self.process_frame.update_material_data(material_data_dict)

    def _export_xs_file(self) -> None:
        self.export_xs_file()