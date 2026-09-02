import os
import time
from typing import IO

from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.output import OutputData
from src.model.process import ProcessDataDict
from src.model.project import ProjectData
from src.service.data_checker import DataChecker


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

        # record used materials
        self.used_materials = ["Substrate"]

        # create a data checker
        self.data_checker = DataChecker()

    def generate_code(self) -> bool | str:
        """Generate the code and write it to a file"""
        try:
            # make a unique file name with path
            file_name_with_path = self.initialize_file_name_with_path()

            # check data for errors
            self.data_checker.check_project_data(self.project_data)
            self.data_checker.check_mask_data_dict(self.mask_data_dict)

            with open(file_name_with_path, "w") as file:
                self.write_project_information(file)
                self.write_built_in_functions(file)
                self.write_project_data(file)
                self.write_mask_data(file)
                self.write_process_data(file)
                self.write_output(file)
            return True
        
        except Exception as e:  # noqa: BLE001
            return f"{e}"

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

    def write_project_information(self, file: IO) -> None:
        # project information
        file.write(f"# Project: {self.project_data.project_name}\n")
        file.write(f"# Date: {time.strftime('%Y-%m-%d')}\n")

        # end of project information
        file.write("\n")
        file.write("\n")

    def write_built_in_functions(self, file: IO) -> None:
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

        # end of built-in functions
        file.write("\n")
        file.write("\n")

    def write_project_data(self, file: IO) -> None:
        # z scaling factor
        file.write("# only the scale of Z direction will be changed\n")
        file.write(f"Z_SCALE = {self.project_data.z_scaling}\n")

        # resolution, height, depth, below
        file.write("# Setting resolution (um)\n")
        file.write(f"dbu({self.project_data.resolution})\n")
        file.write("# setting view of height, above surface substrate\n")
        file.write(f"height(vertical({self.project_data.height}))\n")
        file.write("# setting view of depth, below surface of substrate\n")
        file.write(f"depth(vertical({self.project_data.depth}))\n")
        file.write("# setting view of below, below backside surface of substrate\n")
        file.write(f"below(vertical({self.project_data.below}))\n")

        # end of project data
        file.write("\n")
        file.write("\n")

    def write_mask_data(self, file: IO) -> None:
        # write mask data
        for mask_data in self.mask_data_dict.values():
            name = f"{mask_data.name}_layer"
            number = f"\"{mask_data.gdsii_number}/{mask_data.datatype}\""
            if mask_data.invert == "0" or mask_data.invert == 0:
                file.write(f"{name} = layer({number})\n")
            else:
                file.write(f"{name} = layer({number}).inverted\n")

        # write substrate data
        file.write("Substrate = bulk\n")

        # end of mask data
        file.write("\n")
        file.write("\n")

    def write_process_data(self, file: IO) -> None:
        # write process data
        for index, process_data in self.process_data_dict.items():

            # note the process name
            file.write(f"# Process {index}: {process_data.name}\n")

            # flip for backside processing
            if process_data.backside == 1 or process_data.backside == "1":
                file.write("flip\n")

            if process_data.type == "-":
                pass

            elif process_data.type == "Deposit":

                # material
                material = process_data.material[0]
                self.used_materials.append(material)
                file.write(f"{material} = deposit(")

                # dimensions
                v = process_data.vertical
                h = process_data.horizontal
                file.write(f"vertical({v}), {h},")

                # options
                file.write(" :mode => :round)")

                # end
                file.write("\n")

            elif process_data.type == "Grow":

                # material
                material = process_data.material[0]
                self.used_materials.append(material)
                file.write(f"{material} = ")

                # mask
                mask = process_data.mask.split(" ")[0]
                mask = f"{mask}_layer"
                file.write(f"mask({mask}).grow(")

                # dimensions
                v = process_data.vertical
                h = process_data.horizontal
                file.write(f"vertical({v}), {h}, ")

                # options
                ignored_material = self._material_string(process_data.ignore_material)
                file.write(f":mode => :round, :through => {ignored_material})")

                # end
                file.write("\n")

            elif process_data.type == "Etch":

                # mask
                mask = process_data.mask.split(" ")[0]
                mask = f"{mask}_layer"
                file.write(f"mask({mask}).etch(")

                # dimensions
                v = process_data.vertical
                h = process_data.horizontal
                a = process_data.angle
                file.write(f"vertical({v}), {h}, :taper => angle({a}), ")

                # options
                material = self._material_string(process_data.material)
                ignored_material = self._material_string(process_data.ignore_material)
                file.write(f":into => {material}, :through => {ignored_material})")

                # end
                file.write("\n")

            # flip back to front side after backside processing
            if process_data.backside == 1 or process_data.backside == "1":
                file.write("flip\n")

            self.write_snapshot(file, process_data.name)
            file.write("\n")

        # end of process data
        file.write("\n")
        file.write("\n")

    def _material_string(self, lst) -> str:
        if lst == []:
            return "[]"
        else:
            string = ""
            for material in lst:
                string += f"{material}, "
            return "[" + string[:-2] + "]"

    def write_output(self, file: IO) -> None:
        for material in self.material_data_dict.values():
            file.write(f"output(\"{material.option_string()}\",")
            file.write(f" {material.name})\n")

        # end of output data
        file.write("\n")

    def write_snapshot(self, file: IO, process_name: str) -> None:
        if self.output_data.steps == "1" or self.output_data.steps == 1:
 
            for material in self.material_data_dict.values():
                if material.name in self.used_materials:
                    file.write(f"output(\"{material.option_string()}\",")
                    file.write(f" {material.name})\n")

            file.write(f"snapshot(\"{process_name}\")\n")