"""
03 VALIDATION

DPS comes with a browser-based validation interface that allows
you to visualise segmentation results, modify them and create new ones.
"""
import dps
import utils

# Perform a speech recognition analysis on an audio file:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")
audio_source = dps.AudioSource(file_list[0])
audio_source.speech_recognition()

# Open the audio source in the validation interface (will open the browser):
