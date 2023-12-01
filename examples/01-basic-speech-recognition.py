"""
01 BASIC SPEECH RECOGNITION

Load an audio file and run a basic speech analysis using vosk.
"""
import dps
import utils
import os

# Set a place to output:
out_dir = os.path.join(os.getcwd(), "output")
if os.path.isdir(out_dir) == False:
    os.makedirs(os.path.join(out_dir, "words-out"))

# Get some audio files:    
file_list = utils.collect_files("test-corpora/en", ["wav"])

# Create an instance of the DSP AudioSource class with one of the files:
audio_source = dps.AudioSource(file_list[0])

# Run the speech recognition method (choose a model according to language: en_small or fr_small):
audio_source.speech_recognition(model = "en_small")

# See the results of the analysis:
print(audio_source.slices)