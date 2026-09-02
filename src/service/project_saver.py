import json
from dataclasses import asdict

from src.model.basic import Data, DataDict
from src.model.mask import MaskData, MaskDataDict
from src.model.material import MaterialData, MaterialDataDict
from src.model.output import OutputData
from src.model.process import ProcessData, ProcessDataDict
from src.model.project import ProjectData


class ProjectSaver:
    def __init__(
            self,
            all_data: dict[str, Data | DataDict] | None = None
    ):
        if all_data is None:
            self.project_data = None
            self.mask_data_dict = None
            self.material_data_dict = None
            self.process_data_dict = None
            self.output_data = None
        else:
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
        if (
            self.project_data is not None
            and self.mask_data_dict is not None
            and self.material_data_dict is not None
            and self.process_data_dict is not None
            and self.output_data is not None
        ):
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
        else:
            raise ValueError("Data is not set. Please provide all data before merging.")

    def save_project_as_json(self, file_path: str):
        merged_dict = self.merge_dicts()
        json_data = json.dumps(merged_dict, indent=4)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_data)

    def read_project_from_json(self, file_name_with_path: str):
        with open(file_name_with_path, "r", encoding="utf-8") as f:
            json_data = f.read()
            data_dict = json.loads(json_data)

            self.project_data = self.dict_to_data("project", data_dict["project"])
            self.mask_data_dict = self.dict_to_data("mask", data_dict["mask"])
            self.material_data_dict = self.dict_to_data("material", data_dict["material"])
            self.process_data_dict = self.dict_to_data("process", data_dict["process"])
            self.output_data = self.dict_to_data("output", data_dict["output"])

    def dict_to_data(self, key: str, data_dict: dict) -> ProjectData | MaskDataDict | MaterialDataDict | ProcessDataDict | OutputData:
        """transform a dictionary to Data or DataDict"""
        if key == "project":
            return ProjectData(**data_dict)
        
        if key == "mask":
            mask_data_dict = MaskDataDict()
            for mask_data in data_dict.values():
                mask_data_dict.append_data(MaskData(**mask_data))
            return mask_data_dict
        
        if key == "material":
            material_data_dict = MaterialDataDict()
            # clear the material_data_dict before appending new data
            material_data_dict.clear()
            for material_data in data_dict.values():
                material_data_dict.append_data(MaterialData(**material_data))
            return material_data_dict
        
        if key == "process":
            process_data_dict = ProcessDataDict()
            for process_data in data_dict.values():
                process_data_dict.append_data(ProcessData(**process_data))
            return process_data_dict
        
        if key == "output":
            return OutputData(**data_dict)
        
        raise ValueError("Unknown data type. Cannot convert dictionary to Data or DataDict.")