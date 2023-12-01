"""
01 BASIC SPEECH RECOGNITION

Load an audio file and run a basic speech analysis using vosk.
"""
import dps
import utils
import os

# Set an output destination and get an audio file:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")

# Create an instance of the DSP AudioSource class with one of the files:
audio_source = dps.AudioSource(file_list[0])

# Run the speech recognition method (choose a model according to language: en_small or fr_small):
audio_source.speech_recognition(model = "en_small")

# See the results of the analysis:
print(audio_source.slices)