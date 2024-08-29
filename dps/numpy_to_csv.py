from .utils import write_csv

def numpy_to_csv(path, columns):
    """Give a path to write to, and a list of dicts like this: {"header":"header_name", "array":np.array}"""
    out = []
    for item in columns:
        to_append = item["array"].tolist()
        to_append.insert(0, item["header"])
        out.append(to_append)
    
    write_csv(path, out)