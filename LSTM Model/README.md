# Sample Model

This folder contains scripts with which one can replicate the training described in the paper. The scripts are generally ready to use, but details such as file locations will need to be specified first.

Content:
- `train.sh` bash script that can be used to submit the training as a job to [OpenPBS](https://www.openpbs.org/) server running [Singularity](https://docs.sylabs.io/guides/latest/user-guide/)
- `main.py` Python script that tkes care of the training loop
- modules folder containing:
    - `preprocess.py` Python file containing preprocessing functions and `GuitarDataset` class
    - `timer.py` Python script used for keeping track of time per epoch when running several training jobs at once
