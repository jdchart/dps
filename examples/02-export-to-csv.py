import dps
import numpy as np

#analysis_file = "/Users/jacob/Documents/Repos/arvest-data-in-context/ml-notebooks/output/fr_male_2_SPEECH_RECOGNITION.json"
analysis_file = "/Users/jacob/Documents/Repos/arvest-data-in-context/ml-notebooks/RENAMED_JSON/0.json"

speech_recognition = dps.SpeechAnalysis(analysis_file, fps = 60)

save_path = "/Users/jacob/Documents/Repos/dps/csv-out.csv"
dps.numpy_to_csv(
    save_path, [
        {"header" : "Raw silence/spoken", "array" : speech_recognition.raw_curve[0]},
        {"header" : "Raw silence/word", "array" : speech_recognition.raw_curve[1]},
        {"header" : "Other dims test", "array" : np.array([0.0, 0.1, 0.5, 0.8])}
    ]
)