"""
04 STATS

The core of DPS revolves around deriving a certain set of statistics about slice lists.
"""
import dps
import utils

# Perform a speech recognition analysis on an audio file and get the slice list:
dest, file_list = utils.get_dest_and_file_list("test-corpora/en")
audio_source = dps.AudioSource(file_list[1])
audio_source.speech_recognition()
slice_list = audio_source.slices

# Get the quantity of a type of slice:
print("Words:", slice_list.get_total_type())
print("Silences:", slice_list.get_total_type("silence"))

# Get the duration of a type of slice:
print("Words (duration):", slice_list.get_total_duration())
print("Silences (duration):", slice_list.get_total_duration("silence"))

# Get the ratio of durations of two slice types:
print("Words/silences ratio:", slice_list.get_duration_ratio("word", "silence"))
print("Silences/words ratio:", slice_list.get_duration_ratio("silence", "word"))

# Get the "DPS" (quantity of slice type / duration of slice type)
print("DPS (words):", slice_list.get_dps())
print("DPS (silences):", slice_list.get_dps("silence"))