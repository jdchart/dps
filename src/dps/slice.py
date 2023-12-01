# slice is an object
# slice array - numpy array of slices
# on each query of slice array, construct pd using only requied values.


import numpy as np

class Slice:
    def __init__(self, start, end, **kwargs) -> None:
        self.start = start
        self.end = end
        self.duration = end - start
        self.type = kwargs.get("type", None)
        self.props = kwargs.get("props", {})

class SliceList:
    def __init__(self) -> None:
        self.array = None
        self.array_empty = True

    def __str__(self) -> str:
        ret = ""
        for i, slice in enumerate(self.array):
            ret = ret + f"{str(i)}: {str(slice.start)} - {str(slice.end)}"
            if slice.type != None:
                ret = ret + f" ({slice.type})"
            ret = ret + "\n"
        ret = ret + f"Number of slices: {str(len(self.array))}"
        return ret

    def append_slice(self, slice):
        if self.array_empty:
            self.array = np.array([slice])
            self.array_empty = False
        else:
            self.array = np.append(self.array, slice)

    def clear(self):
        self.array = None
        self.array_empty = True