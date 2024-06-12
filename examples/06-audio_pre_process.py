import dps
import utils

dest, file_list = utils.get_dest_and_file_list("test-corpora/video")
audio_source = dps.AudioSource(file_list[1])

print(audio_source.source)
audio_source.pre_process_audio()