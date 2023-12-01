from .utils import *
import uuid
import subprocess
import scipy
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy

tf.random.set_seed(42) # Initial tensorflow seed.

class Classifier:
    def __init__(self) -> None:
        """An MLP neural network classifier."""

        self.training_data = {}
        self.x_train = None
        self.y_train = None
        self.model = None
        self.class_map = {}

    def append_training_data(self, audio_file_path : str, class_name : str) -> None:
        """Add a new input for classifier training."""

        if class_name in self.training_data:
            self.training_data[class_name].append(audio_file_path)
        else:
            self.training_data[class_name] = [audio_file_path]

    def analyse_training_data(self) -> None:
        """Perform descriptor analysis on training data."""

        self.x_train = None
        self.y_train = None
        self.class_map = {}
        done_first = False
        for i, class_name in enumerate(self.training_data):
            for audio_file_path in self.training_data[class_name]:
                res = self._audio_analysis(audio_file_path)
                if done_first:
                    self.x_train = np.vstack([self.x_train, res])
                    self.y_train = np.vstack([self.y_train, [i]])
                else:
                    self.x_train = res
                    self.y_train = np.array([i])
                    done_first = True
        self.x_train = tf.convert_to_tensor(self.x_train)
        self.y_train = tf.convert_to_tensor(self.y_train)
    
    def train(self, **kwargs) -> None:
        """Train the neural network."""

        self.model = self._get_model(self.x_train.shape[1], len(self.training_data))
        
        history = self.model.fit(self.x_train, self.y_train, epochs=kwargs.get('epochs', 10), batch_size=32)  #, validation_data=(X_test, y_test))

    def predict(self, audio_file: str) -> None:
        """Predict the class of an audio file using the current model."""

        prediction_input = self._audio_analysis(audio_file)
        prediction_input = tf.reshape(prediction_input,shape=(1,91))

        prediction = self.model.predict(prediction_input)

        print()
        print("PREDICTION:")
        print(prediction)

        predicted_classes = tf.argmax(prediction, axis=1)
        print("PREDICTED CLASSES:")
        print(predicted_classes.numpy())

    def _get_model(self, input_dims : int, num_classes : int) -> Sequential:
        """Return the neural network."""

        model = Sequential()

        model.add(Dense(units=128, activation='relu', input_dim=input_dims))
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=num_classes, activation='softmax'))
        
        model.compile(optimizer=Adam(learning_rate=0.001),
              loss=SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
        return model

    def _get_training_data(self) -> None:
        pass

    def _audio_analysis(self, sound_file : str) -> np.array:
        """Perform audio analysis on each word found in a fragment of sound."""
        
        for_analysis = os.path.join(create_temp_folder(), f"{str(uuid.uuid4())}_analysis_input.wav")
        as_mono = convert_to_mono(sound_file, for_analysis)
        analysis = self._wave_to_np(self._stats(self._mfcc(as_mono)))
        return analysis.flatten()
        
    def _mfcc(self, src : str) -> str:
        """Perform MFCC analysis on audio file and return path to results."""

        out_dest = os.path.join(create_temp_folder(), f"{str(uuid.uuid4())}_mfcc_analysis.wav")
        call_list = ["fluid-mfcc", "-source", src, "-features", out_dest]
        subprocess.run(call_list, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return out_dest
    
    def _stats(self, src: str) -> str:
        """Perform stat analysis on fluid analysis result and return path to results."""

        out_dest = os.path.join(create_temp_folder(), f"{str(uuid.uuid4())}_stats.wav")
        call_list = ["fluid-stats", "-source", src, "-stats", out_dest]
        subprocess.run(call_list, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return out_dest
    
    def _wave_to_np(self, path: str) -> np.array:
        try:
            rate, data = scipy.io.wavfile.read(path)
            return data
        except:
            print(f"Unable to read {path}")
