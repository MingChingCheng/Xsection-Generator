import json
from dataclasses import asdict

from src.model.basic import Data, DataDict


class ProjectSaver:
    def __init__(
            self,
            all_data: dict[str, Data | DataDict]
    ):
        self.project_data = all_data["project"]
        self.mask_data_dict = all_data["mask"]
        self.material_data_dict = all_data["material"]
        self.process_data_dict = all_data["process"]
        self.output_data = all_data["output"]

    def data_to_dict(self, data: Data | DataDict) -> dict:
        """transform Data or DataDict to a dictionary"""
        if isinstance(data, Data):
            return asdict(data)
        
        if isinstance(data, DataDict):
            return {key: asdict(value) for key, value in data.items()}

    def merge_dicts(self) -> dict:
        project_dict = self.data_to_dict(self.project_data)
        mask_dict = self.data_to_dict(self.mask_data_dict)
        material_dict = self.data_to_dict(self.material_data_dict)
        process_dict = self.data_to_dict(self.process_data_dict)
        output_dict = self.data_to_dict(self.output_data)

        return {"project": project_dict,
                "mask": mask_dict,
                "material": material_dict,
                "process": process_dict,
                "output": output_dict}

    def save_project_as_json(self, file_path: str):
        merged_dict = self.merge_dicts()
        json_data = json.dumps(merged_dict, indent=4)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_data)
