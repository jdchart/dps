import dps
from utils import display_curve

analysis_file = "/Users/jacob/Documents/Repos/arvest-data-in-context/ml-notebooks/output/fr_male_2_SPEECH_RECOGNITION.json"

# Load the vosk speech analysis:
speech_recognition = dps.SpeechAnalysis(analysis_file, fps = 64)

# See the raw curves:
speech_recognition.display_raw_curve(0) # (words on/off)
speech_recognition.display_raw_curve(1) # (words on/off + incremental value/word)

# Get the dps as follows:
print(speech_recognition.get_dps())
print(speech_recognition.get_dps(region = {"start_ms" : 0, "end_ms" : 92000}))
print(speech_recognition.get_dps(region = {"start_ms" : 0, "end_ms" : 40000}))
print(speech_recognition.get_dps(region = {"start_ms" : 40000, "end_ms" : 92000}))

# Get DPS as a feature:
dps_curve = speech_recognition.get_dps_feature_curve(128, 4)
display_curve(dps_curve)