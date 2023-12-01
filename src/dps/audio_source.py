import os
import uuid
import json
import vosk
import wave
import pickle
from pydub import AudioSegment
import pandas as pd
from .utils import *
from .slice import Slice, SliceList

vosk.SetLogLevel(-1) # Supress vosk console output.

class AudioSource:
    def __init__(self, path : str, **kwargs) -> None:
        """Main audio source class."""

        self.source = path
        self.model_paths = kwargs.get("model_paths", os.path.join(os.getcwd(), "models"))
        
        self._file_name = os.path.splitext(os.path.basename(self.source))[0]
        self._source_duration = get_audiofile_length(path)

        self.slices = SliceList()

    def write(self, path : str) -> None:
        """Write the audio source to disk. The file name must use the extension ".pickle"."""

        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def split_word(self, index : int, dest_folder : str) -> str:
        """Pass the index of a slice and output as audio."""

        slice = self.slices[index]

        start_ms = slice.start * 1000
        end_ms = slice.end * 1000

        file_name = f"{str(index)}_{str(start_ms)}_{str(end_ms)}"
        if slice.type != None:
            file_name = file_name + f"_{slice.type}"
            if slice.type == "word":
                word = slice.props["word"]
                file_name = file_name + f"_{word}"
        final_dest = os.path.join(dest_folder, f"{file_name}.wav")

        audio_load = AudioSegment.from_wav(self.source)
        audio_load = audio_load[start_ms:end_ms]
        audio_load.export(final_dest, format="wav")
        return final_dest

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

    def _speech_recognition_parse(self, sr_results) -> None:
        """Update the slices SliceList with the reuslts of a vosk speech recognition analysis."""

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

    def _get_sr_model(self, model_name : str) -> str:
        """Return the path to a vosk model."""

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