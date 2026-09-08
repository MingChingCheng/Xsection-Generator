from dataclasses import dataclass

from src.model.basic import Data, DataDict


@dataclass
class ProcessData(Data):
    name: str
    type: str
    mask: str
    material: str | list[str]
    ignore_material: str | list[str]
    vertical: str
    horizontal: str
    angle: str
    backside: int | str

    def option_string(self) -> str:
        """return the string to be displayed in the listbox"""
        return f"{self.name}: {self.type}"


class ProcessDataDict(DataDict[ProcessData]):
    def __init__(self):
        super().__init__()

    def _apply_default_value(self, data: ProcessData) -> ProcessData:
        """apply default value to ProcessData if entry is empty"""
        length = self.__len__()

        # name
        if data.name == "":
            data.name = f"Process_{length + 1}"
        # replace space in name with underscore
        data.name = data.name.replace(" ", "_")

        # type
        if data.type == "-":
            data.type = "-"

        # vertical
        if data.vertical == "":
            data.vertical = "1"

        # horizontal
        if data.horizontal == "":
            data.horizontal = "1"

        # angle
        if data.angle == "":
            data.angle = "0"

        return data
