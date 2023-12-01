import pickle
from .audio_source import AudioSource
from .slice import SliceList

def read_audio_source(path : str) -> AudioSource:
    """Read an audio source object from disk."""

    with open(path, 'rb') as f:
        sl = pickle.load(f)
    return sl

def read_slice_list(path : str) -> SliceList:
    """Read a slice list object from disk."""
    
    with open(path, 'rb') as f:
        sl = pickle.load(f)
    return sl