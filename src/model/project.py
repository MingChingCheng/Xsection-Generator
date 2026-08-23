from dataclasses import dataclass

from src.model.basic import Data


@dataclass
class ProjectData(Data):
    project_name: str = "New_Project"
    z_scaling: str = "1"
    resolution: str = "0.001"
    height: str = "20"
    depth: str = "10"
    below: str = "10"

    def option_string(self) -> str:
        return f"{self.project_name}"
    