# GFXSetCTU

This repository contains all information related to the guitar dataset created for training ML models to perform as analog nonlinear devices.
The repository does **NOT** contain the dataset, but rather scripts, manuals, hints, and other support material that may be necessary for better utilization of the data.
To obtain the dataset, refer to sections [Contents](#contents) and [How to Access](#how-to-access).

Dataset was created under [Multimedia Technology Group (MMTG)](https://mmtg.fel.cvut.cz/) operating under the [Department of Radioelectronics](https://radio.fel.cvut.cz/) at [Faculty of Electrical Engineering](https://fel.cvut.cz/en), [Czech Technical University in Prague](https://www.cvut.cz/en).

## Using the Dataset

If you used the dataset in your work, please cite it as the following conference paper:
```
@INPROCEEDINGS{Huzv2505:Open,
AUTHOR="Matej Huzvar and Stanislav Vitek",
TITLE="Open Dataset for Modeling Nonlinear Systems for Electric Guitar",
BOOKTITLE="2025 35th International Conference Radioelektronika (RADIOELEKTRONIKA)
(RADIOELEKTRONIKA'25)",
ADDRESS="Hnanice, Czech Republic",
PAGES="3.91",
ABSTRACT="A robust representative dataset is a critical component in proper training
of any neural network. In this paper, we present a dataset designed
specifically for training models of nonlinear systems relevant to electric
guitar, including distortion effects and amplifiers. Our dataset, which
reflects developments in the design of electric guitars, is carefully
selected and ready for further extension using readily available commercial
recording equipment. The introduced dataset consists of source audio
signals recorded on several guitars and short synthesized samples, and
corresponding output signals from several systems at several setting
combinations."
}
```

## The Dataset

### Contents

The content with links is listed in the table below.
Refer to [How to Access](#how-to-access) section for further details.

| Device                                | Codename | Location                        | Status [^1] | Size [^2] | Author |
|---------------------------------------|----------|---------------------------------|-------------|-----------|--------|
| Boss DS-1                             | bds1     | [CTU fileshare](#how-to-access) | complete    | 37 GB     | MMTG   |
| Earthquaker Devices Spatial Delivery  | eqsd     | TBD                             | in progress | TBD       | MMTG   |
| EHX Lumberjack                        | lumb     | [CTU fileshare](#how-to-access) | complete    | 37 GB     | MMTG   |
| Keeley Dark Side                      | keds     | [CTU fileshare](#how-to-access) | partial     | 37 GB     | MMTG   |

The table above only refers to labels (signals fed through the respective devices).
The input signals can be found on [CTU provided fileshare](#how-to-access) along with the labels recorded by MMTG.
The input folder takes up approximately 230 MB of space.

[^1]: Status "complete" means the device is completely recorded, preprocessed and uploaded with all setting combinations. "Partial" means some setting combinations are yet to be completed. "In progress" means a reasonable set of combinations has to be recorded before the device is at least partially uploaded.
[^2]: These values are approximate. In case of incomplete status, the size given is the size of available data and will increase with time.

### How to Access

All data can be currently accessed through [fileshare](https://fel.sh.cvut.cz/huzvamat/GFXSetCTU/) provided by CTU.
In order to get to the data, you need authenticate with the following credentials:
- username: datareader
- password: ![pwd](pwd.png)

This will give you access to all of the files and you may download any subset of the dataset you need.
To download only a specified subset on a Linux machine, you may use `wget`[^3]:

[^3]: [Wget manual](https://www.gnu.org/software/wget/manual/wget.html)
```console
$ wget -r -l1 -nH --cut-dirs=1 --reject="index.html*" --user=USERNAME --ask-password https://fel.sh.cvut.cz/huzvamat/GFXSetCTU/path_to_desired_folder/
```

It should be possible to use `wget` on Windows 11 in PowerShell and it should be possible to install on MacOS through brew or port.
Neither Windows nor MacOS has been tested however.

Device recordings are placed in folders named by the device codename (see table in [Contents](#contents)) and divided into folders named according to device settings when recording.
See [devices.md](https://github.com/Mhuzvar/GFXSetCTU/blob/main/devices.md) for further information for each device.
The data structure is illustrated bellow:
```md
fel.sh.cvut.cz/huzvamat/GFXSetCTU/
 ├── labels
 │    ├── bds1
 │    │    ├── 00_00
 │    │    │    ├── noise_00.wav
 │    │    │    ├── ...
 │    │    │    └── ss_30.wav
 │    │    ├── ...
 │    │    └── 10_10
 │    │         └── ...
 │    ├── ...
 │    └── keds
 │         └── ...
 └── raw
      ├── noise.wav
      ├── ...
      └── ss.wav
```

## Expanding the Dataset

The process of adding recordings of a new device is explained in [Expanding the Dataset](https://github.com/Mhuzvar/GFXSetCTU/tree/main/Expanding%20the%20Dataset).
All known additions to the dataset are and will be linked on this page in table in [Contents](#contents).

## Other Content of the Repository

[LSTM Model](https://github.com/Mhuzvar/GFXSetCTU/tree/main/LSTM%20Model) folder contains scripts for training an LSTM model described in the paper using the dataset.

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
The license requires one to give appropriate credit, link to the
license and indicate if changes were made. These terms are considered fulfilled by [citing the paper](#using-the-dataset). 

[![CC BY 4.0](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)
