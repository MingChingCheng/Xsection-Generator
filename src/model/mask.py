from dataclasses import dataclass


@dataclass
class MaskData:
    name: str
    gdsii_number: str
    datatype: str
    invert: int | str

    def option_string(self):
        return f"{self.name} {self.gdsii_number}/{self.datatype}"


class MaskDataDict(dict):
    def __init__(self):
        super().__init__()

    def append_mask_data(self, mask_data: MaskData):
        length = self.__len__()
        self[f"{length}"] = self._apply_default_value(mask_data)

    def remove_mask_data(self, index: int):
        if str(index) in self:
            del self[str(index)]
            self.refresh_mask_data()

    def refresh_mask_data(self):
        for index, key in enumerate(self.keys()):
            mask_data = self[key]
            self[f"{index}"] = mask_data

    def _apply_default_value(self, mask_data: MaskData) -> MaskData:
        length = self.__len__()

        # name
        if mask_data.name == "":
            mask_data.name = f"Mask_{length + 1}"

        # gdsii_number
        if mask_data.gdsii_number == "":
            # setting a unique gdsii_number
            existing_number = [mask.gdsii_number for mask in self.values()]
            for i in range(1, length+2):
                if f"{i}" not in existing_number:
                    mask_data.gdsii_number = f"{i}"
                    break
            else:
                mask_data.gdsii_number = f"{length + 1}"
        # datatype
        if mask_data.datatype == "":
            mask_data.datatype = "0"

        # invert
        if mask_data.invert == "":
            mask_data.invert = 0

        return mask_data