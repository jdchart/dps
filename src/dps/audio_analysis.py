import os
import uuid
import json
import vosk
import wave
from pydub import AudioSegment
import pandas as pd
from .utils import *

vosk.SetLogLevel(-1) # Supress vosk console output.

class AudioSource:
    def __init__(self, path, **kwargs) -> None:
        self.source = path
        self.model_paths = kwargs.get("model_paths", os.path.join(os.getcwd(), "models"))
        
        self._file_name = os.path.splitext(os.path.basename(self.source))[0]

    def split_word(self, data_frame, index, out_folder) -> str:
        """Pass the index of a word in the speech recognition result and save as an audio file."""
        df_row = data_frame.iloc[index]
        start_ms = df_row['start'] * 1000
        end_ms = df_row['end'] * 1000
        word_name = df_row['word']
        audio_load = AudioSegment.from_wav(self.source)
        audio_load = audio_load[start_ms:end_ms]
        audio_load.export(os.path.join(out_folder, f"{index}_{word_name}_{str(start_ms)}_{str(end_ms)}.wav"), format="wav")

    def speech_recognition(self, **kwargs) -> dict:
        """
        Perform speech recognition on the audio source using vosk.

        model = the model used by vosk (en_small, fr_small)
        """

        audio = self._preprocess_audio()
        model = vosk.Model(self._get_sr_model(kwargs.get('model', "en_small")))
        
        with wave.open(audio, 'rb') as wf:
            sample_rate = wf.getframerate()
            audio_data = wf.readframes(wf.getnframes())

        recognizer = vosk.KaldiRecognizer(model, sample_rate)
        recognizer.SetWords(True)

        if recognizer.AcceptWaveform(audio_data):
            res = json.loads(recognizer.Result())
        else:
            print("Recognition failed.")

        cleanup()

        sr_df = self._speech_recognition_to_pandas(res)
        silence_df = self._get_silences(sr_df)
        return sr_df, silence_df

    def _speech_recognition_to_pandas(self, sr_results):
        """Convert the results of a vosk speech recognition analysis to pandas."""
        df = pd.DataFrame()
        df['word'] = None
        df['start'] = None
        df['end'] = None
        df['duration'] = None
        df['conf'] = None
        for i, word in enumerate(sr_results["result"]):
            to_append = {
                'word' : word['word'],
                'start' : word['start'],
                'end' : word['end'],
                'duration' : word['end'] - word['start'],
                'conf' : word['conf']
            }
            df.loc[len(df)] = to_append
        return df
    
    def _get_silences(self, sr_df):
        """Derive a pandas dataframe of silences from the results of a speech recognition analysis."""
        df = pd.DataFrame()
        df['start'] = None
        df['end'] = None
        df['duration'] = None

        if sr_df.iloc[0]["start"] == 0:
            pass

        current_start = 0
        audio_length = 1000

        for index, row in sr_df.iterrows():
            if row['start'] - current_start > 0:
                print(current_start, row['start'])
            current_start = row['end']
            if index == len(sr_df) - 1:
                if audio_length - row['end'] > 0:
                    print(row['end'], audio_length)
            # if index != len(sr_df) - 1:
            #     print(current_start, row['start'])
            #     current_start = row["end"]
            # else:
            #     print(f"Last: {str(index)}")

        return df

    def _get_sr_model(self, model_name):
        if model_name == "en_small":
            return os.path.join(self.model_paths, "vosk-model-small-en-us-0.15")
        elif model_name == "fr_small":
            return os.path.join(self.model_paths, "vosk-model-small-fr-0.22")

    def _preprocess_audio(self) -> str:
        """Convert the source to a mono wav file and 16000 sampling rate."""
        temp_path = create_temp_folder()
        new_path = os.path.join(temp_path, f"{str(uuid.uuid4())}_{self._file_name}_mono.wav")
        convert_to_mono(self.source, new_path)
        resample(new_path, new_path, 16000)
        return new_path