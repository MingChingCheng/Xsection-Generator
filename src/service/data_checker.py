from src.model.mask import MaskData, MaskDataDict
from src.model.material import MaterialData, MaterialDataDict
from src.model.output import OutputData
from src.model.process import ProcessData, ProcessDataDict
from src.model.project import ProjectData


class DataChecker:
    def __init__(self):
        self.all_correct = True

    def check_project_data(self, project_data: ProjectData) -> None:
        """Check the project data for errors"""

        # project name
        ## check if project name has invalid characters
        invalid_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

        for char in invalid_chars:
            if char in project_data.project_name:
                raise ValueError(f"Project name contains invalid character '{char}' !")

        # Z scaling
        try:
            z_scaling = float(project_data.z_scaling)
        except ValueError:
            raise ValueError(f"Z scaling '{project_data.z_scaling}' is not a number !")
        if z_scaling <= 0:
            raise ValueError("Z scaling must be greater than 0 !")

        # Resolution
        try:
            resolution = float(project_data.resolution)
        except ValueError:
            raise ValueError(f"Resolution '{project_data.resolution}' is not a number !")
        if resolution <= 0:
            raise ValueError("Resolution must be greater than 0 !")
        if resolution > 1:
            raise ValueError(f"Resolution ({resolution}(um)) is too low !")

        # Height
        try:
            height = float(project_data.height)
        except ValueError:
            raise ValueError(f"Height '{project_data.height}' is not a number !")
        if height <= 0:
            raise ValueError("Height must be greater than 0 !")

        # Depth
        try:
            depth = float(project_data.depth)
        except ValueError:
            raise ValueError(f"Depth '{project_data.depth}' is not a number !")
        if depth <= 0:
            raise ValueError("Depth must be greater than 0 !")

        # Below
        try:
            below = float(project_data.below)
        except ValueError:
            raise ValueError(f"Below '{project_data.below}' is not a number !")
        if below <= 0:
            raise ValueError("Below must be greater than 0 !")

    def check_mask_data_dict(self, mask_data_dict: MaskDataDict) -> None:
        """Check the material data for errors"""
        for mask_data in mask_data_dict.values():
            self.check_mask_data(mask_data)

    def check_mask_data(self, mask_data: MaskData) -> None:
        """Check the mask data for errors"""
        # mask name
        ## first char of name must be a letter
        if ord(mask_data.name[0]) < 65 or ord(mask_data.name[0]) > 122:
            raise ValueError(f"Mask name '{mask_data.name}' must start with a letter !")

        ## check if mask name has a space character
        if " " in mask_data.name:
            raise ValueError(f"Mask name '{mask_data.name}' must not contain space character !")

        # GDSII number
        ## check if GDSII number is an integer
        try:
            gdsii_number = int(mask_data.gdsii_number)
        except ValueError:
            raise ValueError(f"{mask_data.name}'s GDSII number '{mask_data.gdsii_number}' is not an integer !")
        ## check if GDSII number is greater than or equal to 0
        if gdsii_number < 0:
            raise ValueError(f"{mask_data.name}'s GDSII number '{mask_data.gdsii_number}' must be greater than or equal to 0 !")

        # Datatype
        ## check if Datatype is an integer
        try:
            datatype = int(mask_data.datatype)
        except ValueError:
            raise ValueError(f"{mask_data.name}'s Datatype '{mask_data.datatype}' is not an integer !")
        ## check if Datatype is greater than or equal to 0
        if datatype < 0:
            raise ValueError(f"{mask_data.name}'s Datatype '{mask_data.datatype}' must be greater than or equal to 0 !")

    def check_material_data_dict(self, material_data_dict: MaterialDataDict) -> None:
        """Check the material data for errors"""
        for material_data in material_data_dict.values():
            self.check_material_data(material_data)

    def check_material_data(self, material_data: MaterialData) -> None:
        """Check the material data for errors"""
        # material name
        ## first char of name must be a letter
        if ord(material_data.name[0]) < 65 or ord(material_data.name[0]) > 122:
            raise ValueError(f"Material name '{material_data.name}' must start with a letter !")

        ## check if material name has a space character
        if " " in material_data.name:
            raise ValueError(f"Material name '{material_data.name}' must not contain space character !")
        
        # GDSII number
        ## check if GDSII number is an integer
        try:
            gdsii_number = int(material_data.gdsii_number)
        except ValueError:
            raise ValueError(f"{material_data.name}'s GDSII number '{material_data.gdsii_number}' is not an integer !")
        ## check if GDSII number is greater than or equal to 0
        if gdsii_number < 0:
            raise ValueError(f"{material_data.name}'s GDSII number '{material_data.gdsii_number}' must be greater than or equal to 0 !")

    def check_process_data_dict(self, process_data_dict: ProcessDataDict) -> None:
        """Check the process data for errors"""
        for process_data in process_data_dict.values():
            self.check_process_data(process_data)

    def check_process_data(self, process_data: ProcessData) -> None:
        """Check the process data for errors"""
        # process name
        ## first char of name must be a letter
        if ord(process_data.name[0]) < 65 or ord(process_data.name[0]) > 122:
            raise ValueError(f"Process name '{process_data.name}' must start with a letter !")

        ## check if process name has a space character
        if " " in process_data.name:
            raise ValueError(f"Process name '{process_data.name}' must not contain space character !")
        
        # Type
        type = process_data.type
        if type not in ["Deposit", "Grow", "Etch"]:
            raise ValueError(f"{process_data.name}'s type '{type}' is not valid !")

        # Mask
        mask = process_data.mask
        if type in ["Grow", "Etch"] and mask == "No mask":
            raise ValueError(f"{process_data.name}'s type '{type}' requires a mask !")

        # Material
        material = process_data.material
        ignore_material = process_data.ignore_material

        if type == "Grow" or type == "Deposit":
            if len(material) > 1:
                raise ValueError(f"{process_data.name}'s type '{type}' can only have one material !")
            if material == [] or material == "":
                        raise ValueError(f"{process_data.name}'s material is empty !")

        if type == "Etch":
            if material == [] or material == "":
                raise ValueError(f"{process_data.name}'s material is empty ! Select at least one material.")
            for ignored in ignore_material:
                if ignored in material:
                    raise ValueError(f"{process_data.name}'s ignore material '{ignored}' is also in the material list !")
                
        # Vertical
        vertical = process_data.vertical
        try:
            vertical = float(vertical)
        except ValueError:
            raise ValueError(f"{process_data.name}'s vertical '{process_data.vertical}' is not a number !")
        if vertical <= 0:
            raise ValueError(f"{process_data.name}'s vertical '{process_data.vertical}' must be greater than 0 !")

        # Horizontal
        horizontal = process_data.horizontal
        try:
            horizontal = float(horizontal)
        except ValueError:
            raise ValueError(f"{process_data.name}'s horizontal '{process_data.horizontal}' is not a number !")
        
        if (type == "Grow" or type == "Deposit") and (horizontal <= 0):
            raise ValueError(f"{process_data.name}'s horizontal '{process_data.horizontal}' must be greater than 0 !")

        if (type == "Etch") and (horizontal < 0):
            raise ValueError(f"{process_data.name}'s horizontal '{process_data.horizontal}' must be greater than or equal to 0 !")

        # Angle
        angle = process_data.angle
        try:
            angle = float(angle)
        except ValueError:
            raise ValueError(f"{process_data.name}'s angle '{process_data.angle}' is not a number !")
        if angle < 0 or angle > 90:
            raise ValueError(f"{process_data.name}'s angle '{process_data.angle}' must be between 0 and 90 !")

    def check_output_data(self, output_data: OutputData) -> None:
        """Check the output data for errors"""
        # Path
        ## empty
        if output_data.path == "":
            raise ValueError("Output path is empty !")
        
        
