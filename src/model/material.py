from dataclasses import dataclass

from src.model.basic import Data, DataDict


@dataclass
class MaterialData(Data):
    name: str
    gdsii_number: str
    datatype: str = "0"

    def option_string(self) -> str:
        """return the string to be displayed in the listbox"""
        return f"{self.name} ({self.gdsii_number}/{self.datatype})"


class MaterialDataDict(DataDict[MaterialData]):
    def __init__(self):
        super().__init__()

        # initialize the substrate
        substrate = MaterialData(name="Substrate", gdsii_number="0", datatype="0")
        new_dict = {"0": substrate}
        self.update(new_dict)

    def _apply_default_value(self, data: MaterialData) -> MaterialData:
        """apply default value to MaskData if entry is empty"""
        length = self.__len__()

        # name
        if data.name == "":
            data.name = f"Material_{length + 1}"

        # gdsii_number
        if data.gdsii_number == "":
            data.gdsii_number = f"{length + 1}"

        # datatype
        same_gdsii_numbers = 0
        for material in self.values():
            if material.gdsii_number == data.gdsii_number:
                same_gdsii_numbers += 1

        data.datatype = f"{same_gdsii_numbers}"
            

        return data
