"""
05 WINDOWS

You can create windows within your audio source which is useful for handling certain parts of the data.
"""
import dps
import utils

# Perform a speech recognition analysis on an audio file and get the slice list:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")
audio_source = dps.AudioSource(file_list[1])
audio_source.speech_recognition()

# There is an attribute of the AudioSource() class called windows which is a list of WindowList()s:
print(audio_source.windows)

# To add a new WindowList(), use the add_window_list() method (if you like you can give it a name).
window = audio_source.add_window_list("manual windows")

# You can add slices to this list manually using the add_window() method:
window.add_window(0, audio_source._source_duration * 0.5)
window.add_window(audio_source._source_duration * 0.5, audio_source._source_duration)

# We added two windows, on from the beginning to half of the audio source, the other frorm half to the end:
print(window)