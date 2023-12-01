"""
01 BASIC SPEECH RECOGNITION

Load an audio file and run a basic speech analysis using vosk
"""
import dps
import utils
import os
import csv

# Set a place to output:
out_dir = os.path.join(os.getcwd(), "output")
if os.path.isdir(out_dir) == False:
    os.makedirs(os.path.join(out_dir, "words-out"))

# Get some audio files:    
file_list = utils.collect_files("test-corpora/en", ["wav"])

# Create an instance of the DSP AudioSource class with one of the files:
audio_source = dps.AudioSource(file_list[0])

# Run the speech recognition method (choose a model according to language: en_small or fr_small):
sr, silences = audio_source.speech_recognition(model = "en_small")

# Returns a pandas dataframe which can be printed or saved to csv:
print(sr)
sr.to_csv(os.path.join(out_dir, "out1.csv"), index = False, quotechar = '"', quoting=csv.QUOTE_NONNUMERIC)



# # Save each word as a seperate audio file:
# for index, row in sr.iterrows():
#     audio_source.split_word(sr, index, os.path.join(out_dir, "words-out"))