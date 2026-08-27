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

        # Initialize the CodeGenerator with the provided data
        self.project_data = project_data
        self.mask_data_dict = mask_data_dict
        self.material_data_dict = material_data_dict
        self.process_data_dict = process_data_dict
        self.output_data = output_data

        file_name_with_path = self.initialize_file_name_with_path()
        
        with open(file_name_with_path, "w") as file:
            self.write_project_data(file)

    def initialize_file_name_with_path(self) -> str:
        """return the file name with path"""

        # Initialize the output file name
        project_name = self.project_data.project_name.replace(" ", "_")
        time_now = time.strftime("%Y-%m-%d")
        filename = project_name + "_" + time_now + ".xs"

        # check if the output path exists, if not create it
        path = self.output_data.path
        if not os.path.exists(path):
            os.makedirs(path)

        # check if the file is existing
        if os.path.exists(os.path.join(path, filename)):
            i = 1
            filename_with_number = project_name + "_" + time_now + "_" + str(i) + ".xs"
            while os.path.exists(os.path.join(path, filename_with_number)):
                i += 1
                filename_with_number = project_name + "_" + time_now + "_" + str(i) + ".xs"
            return os.path.join(path, filename_with_number)
        else:
            return os.path.join(path, filename)

    def write_project_data(self, file):
        file.write(f"# Project: {self.project_data.project_name}\n")