import torch
import torchaudio
import os
import shutil
import librosa
import soundfile
import audiofile
import json
import subprocess
import webbrowser
import pyloudnorm as pyln
from scipy.io import wavfile
import noisereduce as nr

def normalize_audio(path_in : str, path_out : str) -> str:
    """
    Boost the gain and normalize an audio file.
    
    https://medium.com/@poudelnipriyanka/audio-normalization-9dbcedfefcc0
    """
    data, rate = soundfile.read(path_in) # load audio
    
    # peak normalize audio to -1 dB
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    
    # measure the loudness first 
    meter = pyln.Meter(rate) # create BS.1770 meter
    loudness = meter.integrated_loudness(data)

    # loudness normalize audio to -12 dB LUFS
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -12.0)

    soundfile.write(path_out, loudness_normalized_audio, rate)
    return path_out

def reduce_noise_audio(path_in : str, path_out : str) -> str:
    # load data
    rate, data = wavfile.read(path_in)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(path_out, rate, reduced_noise)
    return path_out


def open_validator() -> None:
    """
    Run a local server running the validation interface.
    
    Will pause execution of python until the user kills the server.
    """
    os.chdir("validation-interface")
    webbrowser.open('http://localhost:5173/', new = 0, autoraise = True)
    subprocess.run(["npm", "run", "dev"])

def create_temp_folder() -> str:
    """Create a temporary folder at os.path.join(os.getcwd(), "dps_temp") and return absolute path."""
    path = os.path.join(os.getcwd(), "dps_temp")
    if os.path.isdir(path) == False:
        os.makedirs(path)
    return path

def cleanup() -> None:
    """Remove the folder at os.path.join(os.getcwd(), "dps_temp") and all it's contents."""
    path = os.path.join(os.getcwd(), "dps_temp")
    if os.path.isdir(path):
        shutil.rmtree(path)

def get_audiofile_length(path):
    return audiofile.duration(path)

def convert_to_mono(source_path : str, out_path : str) -> None:
    """Convert a multichannel audio file to mono."""
    waveform, sr = torchaudio.load(source_path)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    torchaudio.save(out_path, waveform, sr)
    return out_path

def resample(source_path : str, out_path : str, sample_rate = 16000) -> None:
    """Resample an ausio file to given sample rate."""
    y, sr_original = librosa.load(source_path, sr = None)
    y_resampled = librosa.resample(y, orig_sr = sr_original, target_sr = sample_rate)
    soundfile.write(out_path, y_resampled, 16000, 'PCM_16')
    return out_path

def write_json(path : str, content : dict, indent : int = 4) -> None:
    """
    Donner un chemin de destination et du contenu et enregistrer au format json.
    
    Si le dossier n'existe pas, cette fonction créera le dossier de manière récursive.
    """
    if os.path.splitext(path)[1] == ".json":
        check_dir_exists(path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii = False, indent = indent)
    else:
        print("Erreur ! Il faut donner un fichier avec une extension \"json\" !")

def check_dir_exists(filepath):
    """Check if folder exists, if not, create it."""
    if os.path.isdir(os.path.dirname(filepath)) == False:
        os.makedirs(os.path.dirname(filepath))