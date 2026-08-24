from dataclasses import dataclass
from typing import Generic, TypeVar

# Define type variable for value type.
DataT = TypeVar("DataT", bound="Data")


@dataclass
class Data:
    
    def option_string(self) -> str:
        """This method should be overridden in subclasses."""
        return "This is a base class for data objects."


class DataDict(dict[str, DataT], Generic[DataT]):
    def __init__(self):
        super().__init__()

    def append_data(self, data: DataT) -> None:
        length = self.__len__()
        self[f"{length}"] = self._apply_default_value(data)

    def insert_data(self, index: int, data: DataT):
        self[f"{index}"] = self._apply_default_value(data)
        
    def remove_data(self, index: int) -> None:
        if str(index) in self:
            del self[str(index)]
            self._reorder_data()

    def swap_data(self, index1: int, index2: int) -> None:
        if str(index1) in self and str(index2) in self:
            self[str(index1)], self[str(index2)] = self[str(index2)], self[str(index1)]

    def _reorder_data(self) -> None:
        new_dict: dict[str, DataT] = {}
        for index, key in enumerate(self.keys()):
            data = self[key]
            new_dict[f"{index}"] = data
        self.clear()
        self.update(new_dict)

    def _apply_default_value(self, data: DataT) -> DataT:
        """This method should be overridden in subclasses."""
        return data
