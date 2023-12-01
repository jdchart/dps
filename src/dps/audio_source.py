import os
import uuid
import json
import vosk
import wave
from pydub import AudioSegment
import pandas as pd
from .utils import *
from .slice import Slice, SliceList

vosk.SetLogLevel(-1) # Supress vosk console output.

class AudioSource:
    def __init__(self, path, **kwargs) -> None:
        self.source = path
        self.model_paths = kwargs.get("model_paths", os.path.join(os.getcwd(), "models"))
        
        self._file_name = os.path.splitext(os.path.basename(self.source))[0]
        self._source_duration = get_audiofile_length(path)

        self.slices = SliceList()

    # def split_word(self, data_frame, index, out_folder) -> str:
    #     """Pass the index of a word in the speech recognition result and save as an audio file."""
    #     df_row = data_frame.iloc[index]
    #     start_ms = df_row['start'] * 1000
    #     end_ms = df_row['end'] * 1000
    #     word_name = df_row['word']
    #     audio_load = AudioSegment.from_wav(self.source)
    #     audio_load = audio_load[start_ms:end_ms]
    #     audio_load.export(os.path.join(out_folder, f"{index}_{word_name}_{str(start_ms)}_{str(end_ms)}.wav"), format="wav")

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

        self._speech_recognition_parse(res)

    def _speech_recognition_parse(self, sr_results):
        self.slices.clear()
        
        if sr_results["result"][0]['start'] == 0:
            pass
        
        current_start = 0

        for i, word in enumerate(sr_results["result"]):
            # Add silence first:
            if word['start'] - current_start > 0:
                self.slices.append_slice(Slice(
                    current_start,
                    word['start'],
                    type = 'silence'
                ))
            current_start = word['end']

            # Add word slice:
            self.slices.append_slice(Slice(
                word['start'],
                word['end'],
                type = 'word',
                props = {'word' : word['word'], 'conf' : word['conf']}
            ))

            # If last occurance, add a final silence:
            if i == len(sr_results["result"]) - 1:
                if self._source_duration - word['end'] > 0:
                    self.slices.append_slice(Slice(
                        word['end'],
                        self._source_duration,
                        type = 'silence'
                    ))

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