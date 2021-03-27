"""Define output data and record."""

# Official Libraries


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'OutputsData',
        )


# Main
class OutputsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, str)

    def get_serialized_data(self) -> str:
        return "".join(self.data)
