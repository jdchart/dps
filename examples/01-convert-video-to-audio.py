import utils
import os

 
file_list = utils.collect_files("/Users/jacob/Documents/Repos/dps/test-corpora/video", ["mp4"])

for item in file_list:
    utils.video_to_wav(item, f"{os.path.splitext(item)[0]}.wav")