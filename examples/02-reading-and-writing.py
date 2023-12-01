"""
02 READING AND WRITING

DPS is designed so that you only need to analyse an audio source once.
This is how to write and read back your analyses properly.
"""
import dps
import utils
import os

# Perform a speech recognition analysis on an audio file:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")
audio_source = dps.AudioSource(file_list[0])
audio_source.speech_recognition()

# Write the audio source to disk:
audio_source.write(os.path.join(dest, "dps_save.pickle"))

# Read the audio source back:
loaded = dps.read_audio_source(os.path.join(dest, "dps_save.pickle"))

print(loaded.slices)
print(loaded.source)

# If you wish, you can save a SliceList object individually:
audio_source.slices.write(os.path.join(dest, "dps_slice_list_save.pickle"))
loaded_slice_list = dps.read_slice_list(os.path.join(dest, "dps_slice_list_save.pickle"))
print(loaded_slice_list)