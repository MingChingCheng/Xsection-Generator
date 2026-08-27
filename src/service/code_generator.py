import os
import time

from src.model.project import ProjectData
from src.model.output import OutputData
from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.process import ProcessDataDict


class CodeGenerator:
    def __init__(
            self, 
            project_data: ProjectData, 
            mask_data_dict: MaskDataDict,
            material_data_dict: MaterialDataDict,
            process_data_dict: ProcessDataDict,
            output_data: OutputData):

        self.project_data = project_data
        self.mask_data_dict = mask_data_dict
        self.material_data_dict = material_data_dict
        self.process_data_dict = process_data_dict
        self.output_data = output_data


        time_now = time.strftime("%Y-%m-%d")
        filename = self.project_data.project_name + "_" + time_now + ".xs"
        path = self.output_data.output_path
        filename_with_path = os.path.join(path, filename)
        with open(filename_with_path, "w") as file:
            self.write_project_data(file)


    def write_project_data(self, file):
        file.write(f"# Project: {self.project_data.project_name}\n")