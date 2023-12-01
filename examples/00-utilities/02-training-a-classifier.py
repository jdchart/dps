"""
02 TRAINING A CLASSIFIER

In DPS, you can try and identify who is speaking by training an neural network to recognize speakers.

NOTE : Why bother with this ?
"""
import dps

# Create an instance of the classifier class:
classifier = dps.Classifier()

# You can build a training corpus by adding audio files and giving the classifier their class:
classifier.append_training_data("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 001 - Atom/bd_dropp.wav", "bd")
classifier.append_training_data("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 001 - Atom/bd_dropp(0).wav", "bd")
classifier.append_training_data("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 001 - Atom/ch_fixer.wav", "hh")
classifier.append_training_data("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 001 - Atom/ch_ornament.wav", "hh")

# Keep track of the training data:
print(classifier.training_data)

# Perform audio analysis of the training data ready to train the classifier:
training_data = classifier.analyse_training_data()

classifier.train(epochs = 20)


classifier.predict("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 002 - 78e/bd_easea.wav")
classifier.predict("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 002 - 78e/bd_mov3.wav")
classifier.predict("/Users/jacob/Documents/Repos/dps/test-corpora/percs/Blips 002 - 78e/ch_upper.wav")