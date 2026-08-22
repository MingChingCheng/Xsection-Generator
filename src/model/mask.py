from dataclasses import dataclass


@dataclass
class MaskData:
    name: str = "Mask"
    gdsii_number: str = "1"
    datatype: str = "0"
    invert: int = 0
    