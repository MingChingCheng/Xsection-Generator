import os
import time
from typing import IO

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
            self.write_project_information(file)
            self.write_built_in_functions(file)
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

    def write_project_information(self, file: IO):
        # project information
        file.write(f"# Project: {self.project_data.project_name}\n")
        file.write(f"# Date: {time.strftime('%Y-%m-%d')}\n")
        file.write("\n")
        file.write("\n")

    def write_built_in_functions(self, file: IO):
        file.write("def vertical(input_thickness)\n")
        file.write("    # multiple thickness by a scaling factor\n")
        file.write("    out = Z_SCALE * input_thickness\n")
        file.write("    return out\n")
        file.write("end\n")
        file.write("\n")
        file.write("def angle(input_angle)\n")
        file.write("    # change angle into radius\n")
        file.write("    input_angle = Math::PI * input_angle / 180\n")
        file.write("    # get new angle after scaling in radius\n")
        file.write("    out = Math.atan( Math.tan(input_angle) / Z_SCALE )\n")
        file.write("    # change new angle into degree\n")
        file.write("    out = out / Math::PI * 180\n")
        file.write("    return out\n")
        file.write("end\n")
        file.write("\n")
        file.write("\n")

    def write_project_data(self, file: IO):
        # z scaling factor
        file.write("# only the scale of Z direction will be changed\n")
        file.write(f"Z_SCALE = {self.project_data.z_scaling}\n")

        # resolution, height, depth, below
        file.write("Setting resolution (um)\n")
        file.write(f"dbu({self.project_data.resolution})\n")
        file.write("# setting view of height, above surface substrate\n")
        file.write(f"height(vertical({self.project_data.height}))\n")
        file.write("# setting view of depth, below surface of substrate\n")
        file.write(f"depth(vertical({self.project_data.depth}))\n")
        file.write("# setting view of below, below backside surface of substrate\n")
        file.write(f"below(vertical({self.project_data.below}))\n")
        file.write("\n")

    def write_mask_data(self, file: IO):
        