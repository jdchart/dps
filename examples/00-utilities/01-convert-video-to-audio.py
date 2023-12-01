"""
Convert a folder of mp4 files to wav.
"""
import os
import utils

src_folder = "/Users/jacob/Documents/Repos/dps/test-corpora/video"

file_list = utils.collect_files(src_folder, ["mp4"])

for item in file_list:
    utils.video_to_wav(item, f"{os.path.splitext(item)[0]}.wav")