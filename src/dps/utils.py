import torch
import torchaudio
import os
import shutil
import librosa
import soundfile

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