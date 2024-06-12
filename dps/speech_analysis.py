from .utils import read_json
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import math
import matplotlib.pyplot as plt

class SpeechAnalysis:
    def __init__(self, path, **kwargs) -> None:
        
        self.analysis_path = path
        self.media = kwargs.get("media", None)
        self.window_size = kwargs.get("window_size", 10)
        self.raw_analysis = None
        self.media_length = kwargs.get("media_length", None)
        self.num_words = None
        
        self._load_analysis()
        self._get_media_length()
        
        self.raw_curve = self._get_raw_curve()

    def _load_analysis(self):
        """Read json and update raw_analysis and media."""
        data = read_json(self.analysis_path)
        self.raw_analysis = data["result"]
        self.num_words = len(data["result"])
        if "media" in data:
            if self.media == None:
                self.media = data["media"]

    def _get_media_length(self):
        """Return media length in ms."""
        try:
            if self.media.endswith(('.mp4', '.mkv', '.avi', '.mov')):
                clip = VideoFileClip(self.media)
            elif self.media.endswith(('.mp3', '.wav', '.aac', '.flac')):
                clip = AudioFileClip(self.media)
            else:
                raise ValueError("Unsupported file format")
            
            self.media_length = clip.duration * 1000
            clip.close()
        except Exception as e:
            print(f"Error: {e}")

    def _get_raw_curve(self):
        """
        Processes the speech recognition data into a time series array of 2 dimensions:
        - class each frame 0 (silence) 1 (spoken)
        - each frame either silence (0) or an incremental int for each new word
        """

        num_frames = math.floor(self.media_length / self.window_size)
        curve = np.zeros((num_frames, num_frames), dtype = int)
        for i, word in enumerate(self.raw_analysis):
            start_frame = int(word["start"] / self.window_size)
            end_frame = int(word["end"] / self.window_size)
            curve[start_frame:end_frame, 0] = 1
            curve[start_frame:end_frame, 1] = i + 1
            print(f"{start_frame} - {end_frame} : 1 and {i + 1}...")
        return curve
    
    def display_raw_curve(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        bar_width = self.window_size
        bar_positions = np.arange(self.window_size)

        # Plot each class
        colors = ['blue', 'green']  # Colors for each class
        for i in range(self.num_words):
            ax.bar(bar_positions, self.raw_curve[:, i], width=bar_width, align='edge', color=colors[i], label=f'Class {i+1}')

        # Set the x-axis labels
        ax.set_xlabel('Frame')
        ax.set_ylabel('Class')
        # ax.set_title('Frame Class Distribution')
        ax.legend()
        plt.xticks(np.arange(0, self.window_size, step=50), rotation=90)  # Adjust as needed

        plt.tight_layout()
        plt.show()