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
        z_scaling = float(project_data.z_scaling)
        if z_scaling <= 0:
            raise ValueError("Z scaling must be greater than 0 !")

        # Resolution
        resolution = float(project_data.resolution)
        if resolution <= 0:
            raise ValueError("Resolution must be greater than 0 !")

        # Height
        height = float(project_data.height)
        if height <= 0:
            raise ValueError("Height must be greater than 0 !")

        # Depth
        depth = float(project_data.depth)
        if depth <= 0:
            raise ValueError("Depth must be greater than 0 !")

        # Below
        below = float(project_data.below)
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

        # GDSII number
        ## check if GDSII number is an integer
        try:
            gdsii_number = int(material_data.gdsii_number)
        except ValueError:
            raise ValueError(f"{material_data.name}'s GDSII number '{material_data.gdsii_number}' is not an integer !")
        ## check if GDSII number is greater than or equal to 0
        if gdsii_number < 0:
            raise ValueError(f"{material_data.name}'s GDSII number '{material_data.gdsii_number}' must be greater than or equal to 0 !")
