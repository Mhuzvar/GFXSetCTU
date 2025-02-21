# The Devices

This document contains information on the devices within the dataset.
For more general information, see [readme](https://github.com/Mhuzvar/GFXSetCTU/blob/main/README.md).

The table contains:
- full name of the device as marketed by the manufacturer
- codename under which the device is refered to in the dataset
- list of potentiometers on the device
- list of switches on the device
    - Switches are not labeled sometimes. In such cases, they are listed as _one-word-description<list/of/modes>_
- list of settings used when recording in the same order as in filenames

Example from the table:
| Device                                    | Codename | Potentiometers                  | Switches              | Settings in Dataset            |
|-------------------------------------------|----------|---------------------------------|-----------------------|--------------------------------|
| Boss DS-1                                 | bds1     | TONE, LEVEL, DIST               | --                    | TONE, DIST                     |

The row describes an entry of [Boss DS-1](https://www.boss.info/global/products/ds-1/). The first field (**Device**) contains the official name. In this dataset, it was given the codename _bds1_, which can be found in the second field (**Codename**). All recordings made using this device are labeled with this codename. The pedal features three potentiometers, _TONE_, _DIST_, and smaller _LEVEL_. They are listed in the third field (**Potentiomenters**). There are no switches on the device, so the fourth field (**Switches**) reads "_--_". The last field (**Settings in Dataset**) lists the potentiometers (and switches if there were any) for which multiple settings were recorded. The _LEVEL_ potentiometer, that is not listed among them was set to a constant value in the middle of its range (12 o'clock) for all recordings.

| Device                                    | Codename | Potentiometers                  | Switches              | Settings in Dataset            |
|-------------------------------------------|----------|---------------------------------|-----------------------|--------------------------------|
| Boss DS-1                                 | bds1     | TONE, LEVEL, DIST               | --                    | TONE, DIST                     |
| Earthquaker Devices Spatial Delivery      | eqsd     | Range, Filter, Resonance        | Mode                  | Mode, Range, Filter, Resonance |
| EHX Lumberjack                            | lumb     | VOL, LOG FACTOR, BOOST          | --                    | LOG FACTOR, BOOST              |
| Keeley Dark Side (fuzz side only)         | keds     | LEVEL, FILTER, FUZZ             | mode<FLAT/FULL/SCOOP> | mode, FILTER, FUZZ             |