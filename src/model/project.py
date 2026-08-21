from dataclasses import dataclass


@dataclass
class ProjectData:
    project_name: str = "New_Project"
    z_scaling: str = "1"
    resolution: str = "0.001"
    height: str = "20"
    depth: str = "10"
    below: str = "10"
    