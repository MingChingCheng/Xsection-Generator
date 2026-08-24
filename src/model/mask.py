from dataclasses import dataclass

from src.model.basic import Data, DataDict


@dataclass
class MaskData(Data):
    name: str
    gdsii_number: str
    datatype: str
    invert: int | str

    def option_string(self) -> str:
        """return the string to be displayed in the listbox"""
        return f"{self.name} {self.gdsii_number}/{self.datatype}"


class MaskDataDict(DataDict[MaskData]):
    def __init__(self):
        super().__init__()

    def _apply_default_value(self, data: MaskData) -> MaskData:
        """apply default value to MaskData if entry is empty"""
        length = self.__len__()

        # name
        if data.name == "":
            data.name = f"Mask_{length + 1}"

        # gdsii_number
        if data.gdsii_number == "":
            # setting a unique gdsii_number
            existing_number = [mask.gdsii_number for mask in self.values()]
            for i in range(1, length+2):
                if f"{i}" not in existing_number:
                    data.gdsii_number = f"{i}"
                    break
            else:
                data.gdsii_number = f"{length + 1}"
        # datatype
        if data.datatype == "":
            data.datatype = "0"

        # invert
        if data.invert == "":
            data.invert = 0

        return data