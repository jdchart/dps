from .utils import read_json
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import math
import matplotlib.pyplot as plt

class SpeechAnalysis:
    def __init__(self, path, **kwargs) -> None:
        """
        Class to perform operations on a speech analysis file.

        kwargs
        - fps : frames per second in the raw curve.
        - window_size : length in ms of a frame in the raw curve.
        """

        self.analysis_path = path
        self.window_size = kwargs.get("window_size", 15.625)
        self.fps = kwargs.get("fps", 64)

        if "fps" in kwargs:
            self.fps = kwargs.get("fps")
            self.window_size = 1000 / self.fps
        elif "window_size" in kwargs:
            self.window_size = kwargs.get("window_size")
            self.fps = math.floor(1000 / self.window_size)
        
        self.raw_analysis = None
        self.media = kwargs.get("media", None)
        self.media_length_ms = kwargs.get("media_length", None)
        self.media_length_frames = None
        self.num_words = None
        
        self._load_analysis()
        self._get_media_length()

        self.media_length_frames =  int(self.media_length_ms * (self.fps / 1000))
        
        self.raw_curve = self._get_raw_curve()
        self.confidence_curve = self._get_confidence_curve()

    def get_dps(self, **kwargs):
        """Return the dps: "dits par seconde", number of words spoken / second."""

        if "region" in kwargs:
            start_ms = kwargs.get("region")["start_ms"]
            end_ms = kwargs.get("region")["end_ms"]
        else:
            start_ms = 0
            end_ms = self.media_length_ms

        dur_ms = end_ms - start_ms

        num_words = self._count_words_region_ms(start_ms, end_ms)

        return num_words / (dur_ms / 1000)
    
    def get_dps_feature_curve(self, window_size = 128, hop_size = 32):
        """
        kawrgs
        - window_size (frames): default: 128. Number of frames in an analysis window. Should be at least the fps.
        - hop_size (frames) : default: 32. analysis window hop. window_size should be divisible by hop_size.
        """
        result = np.zeros(len(self.raw_curve[1]))
        counts = np.zeros(len(self.raw_curve[1]))

        for start in range(0, len(self.raw_curve[1]) - window_size + 1, hop_size):
            end = start + window_size
            # window = self.raw_curve[1][start:end]
            dur_ms = ((end - start) / self.fps) * 1000
            window_result = self._count_words_region_frames(start, end) / (dur_ms / 1000)

            result[start:end] += window_result
            counts[start:end] += 1
        
        result = result / counts
        return result

    def _count_words_region_ms(self, start_ms, end_ms):
        start_frames = self._ms_to_frames(start_ms)
        end_frames = self._ms_to_frames(end_ms)

        return self._count_words_region_frames(start_frames, end_frames)
        
    def _count_words_region_frames(self, start_frame, end_frame):
        i = start_frame
        num_words = 0
        current_word = 0

        while i < end_frame:
            this_frame = self.raw_curve[1][i]
            if this_frame != current_word:
                if this_frame != 0:
                    num_words = num_words + 1
                current_word = this_frame
            i = i + 1
        return num_words
   
    def _ms_to_frames(self, time_ms):
        return math.floor((time_ms / 1000) * self.fps)

    def _load_analysis(self):
        """Read json and update raw_analysis and media."""
        data = read_json(self.analysis_path)
        self.raw_analysis = data["result"]
        self.num_words = len(data["result"])
        if "media" in data:
            if self.media == None:
                self.media = data["media"]
        self.media_length_ms = data["media_length"] * 1000

    def _get_media_length(self):
        """Return media length in ms."""
        # try:
        #     if self.media.endswith(('.mp4', '.mkv', '.avi', '.mov')):
        #         clip = VideoFileClip(self.media)
        #     elif self.media.endswith(('.mp3', '.wav', '.aac', '.flac')):
        #         clip = AudioFileClip(self.media)
        #     else:
        #         raise ValueError("Unsupported file format")
            
        #     self.media_length_ms = clip.duration * 1000
        #     self.media_length_frames = (self.media_length_ms / 1000) * self.fps
        #     clip.close()
        # except Exception as e:
        #     print(f"Error: {e}")
        pass

    def _get_raw_curve(self):
        """
        Processes the speech recognition data into a time series array of 2 dimensions:
        - class each frame 0 (silence) 1 (spoken)
        - each frame either silence (0) or an incremental int for each new word
        """

        num_frames = math.floor(self.media_length_frames)
        
        curve_1 = np.zeros((num_frames), dtype = int)
        curve_2 = np.zeros((num_frames), dtype = int)
        for i, word in enumerate(self.raw_analysis):
            start_frame = math.floor(word["start"] * 1000 / self.window_size)
            end_frame = math.floor(word["end"] * 1000 / self.window_size)
            curve_1[start_frame:end_frame] = 1
            curve_2[start_frame:end_frame] = i + 1
        return np.array((curve_1, curve_2))
    
    def display_raw_curve(self, dim = 0):
        plt.figure(figsize=(10, 6))
        frame_numbers = np.arange(len(self.raw_curve[dim]))
        plt.plot(frame_numbers, self.raw_curve[dim], drawstyle='steps-post')

        plt.xlabel('Frame')
        plt.ylabel('Value')
        if dim == 0:
            plt.title('Silence or spoken')
        else:
            plt.title('Silence or word index')
        plt.show()

    def _get_confidence_curve(self, silence_mode = "ffill"):
        """
        silence_mode: how to fill confidence in silent frames:
            - "nan": silence is NaN
            - "zero": silence is 0.0
            - "ffill": forward-fill last known confidence
        """
        num_frames = math.floor(self.media_length_frames)
        if silence_mode == "zero":
            conf_curve = np.zeros((num_frames,), dtype=float)
        else:
            conf_curve = np.full((num_frames,), np.nan, dtype=float)

        for word in self.raw_analysis:
            start_frame = math.floor(word["start"] * 1000 / self.window_size)
            end_frame = math.floor(word["end"] * 1000 / self.window_size)
            conf_curve[start_frame:end_frame] = word["conf"]

        if silence_mode == "ffill":
            valid = ~np.isnan(conf_curve)
            if np.any(valid):
                last_valid = np.maximum.accumulate(np.where(valid, np.arange(num_frames), -1))
                conf_curve = conf_curve[last_valid]
            else:
                conf_curve[:] = 0.0

        return conf_curve