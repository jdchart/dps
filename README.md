# dps

A python package for DPS analysis (dit-par-seconde).

1. [Overview](#overview)
2. [Setup](#setup)
3. [Roadmap](#roadmap)

## Overview

Based on the work of Théo Heugebaert, and developped by Jacob Hart and Théo Heugebaert, DPS offers an environment for dealing with analysis of the number of words spoken in an audio file, deriving various metrics from this raw data, and comparing analyses of different sources. It emerged from the analysis of theatre, but can be applied to any field investigating the analysis of spoken word.

### Speech recognition:

In DPS, we use [vosk](https://pypi.org/project/vosk/) for speech recognition. See [setup](#setup) for how to use different models. The `AudioSource()` class has method called `speech_recognition()` that will perform the speech recognition analysis. This will update the `AudioSource()` object's `slices` attribute, which is an instance of the DPS `SliceList()` class.

```python
from dps import AudioSource

src = AudioSource('path/to/audio_file.wav')
src.speech_recognition()
print(src.slices)
```

## Setup

DPS runs as a normal python package, and will eventually be published on the pip. For the moment, you can clone this repo as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) and run `pip install src/` from root to start working. It is recommended to use virtual environments. You will also need to set up a few other things:

### ffmpeg

DPS uses ffmpeg to resample audio to match Vosk's models input size.

To install ffmpeg:

```shell
brew install ffmpeg
```

### Vosk models

DPS uses Vosk for speech recognition. It is in the roadmap to streamline this process, but for the moment, you will need to download the models [here](https://alphacephei.com/vosk/models) and place them in a `models` foler at the root of your project folder.

### FluCoMa CLI

DPS uses the FluCoMa CLI for audio analysis. It is in the roadmap to streamline this process, but for the moment, you will need to download the CLI tools [here](https://github.com/flucoma/flucoma-cli/releases/tag/1.0.6) and place them in your system `bin`. It is advised to create a virtual environment for you project and place them in that bin.

### nodejs

You will have to have nodejs installed on your system. We recommend using [nvm](https://github.com/nvm-sh/nvm), or you can download [nodejs](https://nodejs.org/en) from here and install it.

### Install node modules.

The validation interface is a [svelte]() web app that runs on a local browser. For this to work, you will need to install the nodejs modules. To do this, run the [update_validation_interface.sh](/shell/update_validation_interface.sh) that is found in the `shell` folder from the repo directory. For this to work, you will first need to run the following command from the repo directory (this gives the shell script permission to be run, you only need to do it once):

```shell
chmod a+x shell/update_validation_interface.sh
```

## Roadmap

### Priority

- [ ] Add normalization and boost gain to audio source input (also possibly remove noise).
- [ ] Reading and writing AudioSource (csv for segmentations and anlyses, pickle for object)
- [ ] Create a validation interface.
- [ ] Merge AudioSources (add one to the end of another)
- [ ] Post processing
- [ ] Intepretation
- [ ] Metrics
- [ ] Visualisations
- [ ] AudioSource comparisons
- [ ] Implement possible word list (`KaldiRecognizer(model, 16000, "zero oh one two three four five six seven eight nine")`)
- [ ] Cache files that are copied to the validation interface.

### If possible

- [ ] Optimize _preprocess_audio() in AudioSource().
- [ ] Add Vosk model, Flucoma CLI and svelte app modules download to setup.
- [ ] Add tests
- [ ] Video playback for validator