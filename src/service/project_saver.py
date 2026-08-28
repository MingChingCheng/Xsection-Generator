import json
from dataclasses import asdict

from src.model.basic import Data, DataDict
from src.model.mask import MaskDataDict
from src.model.material import MaterialDataDict
from src.model.output import OutputData
from src.model.process import ProcessDataDict
from src.model.project import ProjectData


class ProjectSaver:
    def __init__(
            self,
            project_data: ProjectData,
            mask_data_dict: MaskDataDict,
            material_data_dict: MaterialDataDict,
            process_data_dict: ProcessDataDict,
            output_data: OutputData
    ):
        self.project_data = project_data
        self.mask_data_dict = mask_data_dict
        self.material_data_dict = material_data_dict
        self.process_data_dict = process_data_dict
        self.output_data = output_data

    def data_to_dict(self, data: Data) -> dict:
        return asdict(data)

    def data_dict_to_dict(self, data_dict: DataDict) -> dict:
        return {key: asdict(value) for key, value in data_dict.items()}

    def merge_dicts(self) -> dict:
        project_dict = self.data_to_dict(self.project_data)
        mask_dict = self.data_dict_to_dict(self.mask_data_dict)
        material_dict = self.data_dict_to_dict(self.material_data_dict)
        process_dict = self.data_dict_to_dict(self.process_data_dict)
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
