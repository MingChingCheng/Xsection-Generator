from tkinter import messagebox

from src.model.project import ProjectData


class DataChecker:
    def __init__(self):
        self.all_correct = True

    def check_project_data(self, project_data: ProjectData):
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