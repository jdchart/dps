import numpy as np
import pickle

class Slice:
    def __init__(self, start, end, **kwargs) -> None:
        """Generic Slice class."""

        self.start = start
        self.end = end
        self.duration = end - start
        self.type = kwargs.get("type", None)
        self.props = kwargs.get("props", {})

    def to_dict(self) -> dict:
        """Return the contents of the slice as a dictionary."""
        return {
            "start" : self.start,
            "end" : self.end,
            "duration" : self.duration,
            "type" : self.type,
            "props" : self.props
        }

class SliceList:
    def __init__(self) -> None:
        """Main slice list object class."""

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
    
    def write(self, path : str) -> None:
        """Write the slice array to disk. The file name must use the extension ".pickle"."""

        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def to_dict(self) -> dict:
        """Return the contents of the slice list as a dictionary."""

        ret = {"slices" : []}
        for item in self.array:
            ret["slices"].append(item.to_dict())
        return ret
    
    def get_total_type(self, slice_type : str = "word") -> int:
        """Return the total number of a given type of slice in the slice list."""
        tot = 0
        for slice in self.array:
            if slice.type == slice_type:
                tot = tot + 1
        return tot
    
    def get_total_duration(self, slice_type : str = "word") -> float:
        """Return the total time of all of a given slice in the slice list."""
        tot = 0
        for slice in self.array:
            if slice.type == slice_type:
                tot = tot + slice.duration
        return tot
    
    def get_duration_ratio(self, slice_type_1 : str, slice_type_2 : str) -> float:
        """Return the ratio of duration of slices of given types."""
        tot_1 = 0
        tot_2 = 0
        for slice in self.array:
            if slice.type == slice_type_1:
                tot_1 = tot_1 + slice.duration
            elif slice.type == slice_type_2:
                tot_2 = tot_2 + slice.duration
        return tot_1/tot_2
    
    def get_dps(self, slice_type : str = "word") -> float:
        """Return the quantity of given slice type / duration of given slice type."""
        return self.get_total_type(slice_type) / self.get_total_duration(slice_type)

    def append_slice(self, slice : Slice) -> None:
        """Add a new slice to the slice array."""

        if self.array_empty:
            self.array = np.array([slice])
            self.array_empty = False
        else:
            self.array = np.append(self.array, slice)

    def clear(self) -> None:
        """Clear the array and reset the object."""

        self.array = None
        self.array_empty = True

    def get_sub_array(self, attribute : str, value, **kwargs) -> np.array:
        """
        Return a numpy array with a subselection of the main array.
        
        Define an attribute (for example "type") and value to match (for example "word").
        You can also query by props by giving the attribute "props" and the kwarg key = "word" for example.
        Finally, you can provide and operator with the op kwarg (by default op = "==").
        """

        op = kwargs.get("op", "==")
        if op == "==":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) == value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] == value])
        elif op == ">=":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) >= value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] >= value])
        elif op == "<=":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) <= value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] <= value])
        elif op == ">":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) > value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] > value])
        elif op == "<":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) < value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] < value])
        elif op == "!=":
            if attribute != "props":
                return np.array([item for item in self.array if getattr(item, attribute) != value])
            else:
                return np.array([item for item in self.array if getattr(item, attribute)[kwargs.get("key")] != value])