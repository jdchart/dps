"""
03 VALIDATION

DPS comes with a browser-based validation interface that allows
you to visualise segmentation results, modify them and create new ones.
"""
import dps
import utils

# Perform a speech recognition analysis on an audio file:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")
audio_source = dps.AudioSource(file_list[1])
audio_source.speech_recognition()

# Open the audio source in the validation interface (will open the browser):
audio_source.open_in_validator()

# Execution of the script is suspensed until you kill the server (Ctrl + C)