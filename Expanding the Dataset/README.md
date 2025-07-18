# Expanding the Dataset

This document describes the steps to expand the dataset with more data. First of all, thank you for helping make this dataset larger and better if you decided to do so. Please note, that the storage available on our servers is very limited, so you will very likely need to find space to put the data up yourself. All known additions to the dataset are and will be linked in [README](https://github.com/Mhuzvar/GFXSetCTU#contents) of the repository and in the [devices](https://github.com/Mhuzvar/GFXSetCTU/blob/main/devices.md) file.

## Recording Equipment

Needed:
- Soundcard capable of recording 24-bit 44.1 kHz audio with number of inputs and outputs at least equal to the number of recorded devices
    - almost any commercially available external soundcard on the market should be capable of 24-bit 44.1 kHz recording
    - the dataset is aimed at guitar effects and amplifiers, so inputs and outputs should be 6.3 mm (1/4") jacks
- the recorded device(s)
    - note that the base duration of the input data is approximately 58 minutes. For a device with two potentiometers at 11 settings each this is around 120 hours of recording.
- any recording software
    - [REAPER](https://www.reaper.fm/) project files are [available in the repository](https://github.com/Mhuzvar/GFXSetCTU/tree/main/Expanding%20the%20Dataset/REAPER), but it is not necessary to use REAPER specifically
- [Python](https://www.python.org/) in order to use the prepared scripts
    - Scripts were tested on version [3.12.3](https://www.python.org/downloads/release/python-3123/)

Recommended:
- [SWS extension](https://www.sws-extension.org/) for Reaper
    - only if using REAPER and the provided project file

## Input set

The `GuitarDataset` class inside `preprocess.py` found in [LSTM Model](https://github.com/Mhuzvar/GFXSetCTU/tree/main/LSTM%20Model)/[modules](https://github.com/Mhuzvar/GFXSetCTU/tree/main/LSTM%20Model/modules) performs level adjustment upon loading a `.wav`. The level adjusted signals are therefore not available in the dataset folder and need to be generated in order to record a device. [Expanding the Dataset](https://github.com/Mhuzvar/GFXSetCTU/tree/main/Expanding%20the%20Dataset) folder contains `levels.py` script, that generates the input signals automatically.

The required data structure for the script to work is:
```md
./
 ├── raw
 │    ├── noise.wav
 │    ├── ...
 │    └── ss.wav
 └── levels.py
```
The script will generate `output` directory with level adjusted input set.

## Recording

The recommended recording setup is described in the paper. It consists of routing soundcard output into the input of the recorded device and the output of the recorded device into the input of the soundcard like in the image below.

![Recording Setup](images/recsetup.png "Recording Setup")

Once the hardware setup is complete and the input set is prepared, the process is as follows:

0. Determine settings on the device to be variable
    - for example volume can be typically easily modeled by multiplication and therefore can be omitted
1. Prepare the input set
    - [Download](https://github.com/Mhuzvar/GFXSetCTU#how-to-access) the input signals and create normalized and attenuated copies using `prep_input.py` script
2. Gain Staging
    1. go through the (chosen variable) settings on the device and find the setting that produces the highest peaks on a sample input
    2. play the louder sections of the input sequence through the device and set output gain in your DAW and input gain on the sound card so there is no clipping from recording
3. Record the device
    - set potentiometers to a setting combination
    - mark setting combination in DAW
    - record the 58 minute sequence
        - if using REAPER with SWS extension, the provided project file contains a mark that stops the recording when the sequence is finished
    - repeat until all settings are recorded

## Post-processing

The current folder contains `sync.py` script to simplify the post-processing as much as possible, but some human input is still necessary. It was originally expected the input and output lag could be matched using cross correlation. While cross-correlation can be used to temporally match the device outputs to each other, the input-output pair is so different in some cases, this method turned out to be too unreliable. The user needs to only set the first delay manually and the script takes care of the rest.

All post-processing is performed by `sync.py` Python script in two phases. The first phase is synchronization, which requires no user input. The second phase is cutting the input into short samples, which requires user to manually set where the signal starts. The signals are synchronized from the first phase, so the start setting only needs to be set for the first setting combination.

The scripts works in the folllowing directory structure:
```md
./
 ├── dataset
 │    ├── raw
 │    │    └── noise.wav
 │    ├── to_sync
 │    │    ├── xx-dname_00_00-zzzzzz_xxxx.wav
 │    │    ├── ...
 │    │    └── xx-dname_10_10-zzzzzz_xxxx.wav
 │    ├── to_cut (generated by sync.py in the first step)
 │    │    ├── xx-dname_00_00-zzzzzz_xxxx.wav
 │    │    ├── ...
 │    │    └── xx-dname_10_10-zzzzzz_xxxx.wav
 │    ├── labels (generated by sync.py)
 │    │    └── dname
 │    │        ├── 00_00
 │    │        │    ├── noise_00.wav
 │    │        │    ├── ...
 │    │        │    └── ss_30.wav
 │    │        ├── ...
 │    │        └── 10_10
 │    │             ├── noise_00.wav
 │    │             ├── ...
 │    │             └── ss_30.wav
 │    └── siglens.txt
 └── sync.py
```
`siglens.txt` is provided in the repository with the script.