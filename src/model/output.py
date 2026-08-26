from dataclasses import dataclass

from src.model.basic import Data


@dataclass
class OutputData(Data):
    path: str
    steps: int | str