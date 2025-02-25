'''
This script generates normalized and attenuated copies of whatever input signals are provided.
Only tested and intended for mono signals.
Version: 0.2

Matej Huzvar
huzvamat@fel.cvut.cz
Prague, February 2025
'''

import os
import numpy as np
import soundfile as sf

def main():
    rawdir = 'raw'
    levdir = 'output'

    levels = [30]   # attenuation levels (besides 0) to be generated

    if not(os.path.isdir(rawdir)):
        raise Exception(f"Input folder {os.path.abspath(levdir)} not found!")

    if not(os.path.isdir(levdir)):
        os.makedirs(levdir)

    for file in os.listdir(rawdir):
        sig, fs = sf.read(os.path.join(rawdir, file))
        #normalisation
        sig = sig/np.max(np.abs(sig))
        sf.write(os.path.join(levdir, file[:-4] + '_00.wav'), sig, fs, subtype='PCM_24')
        for lev in levels:
            sig1 = sig*(10**(-lev/20))
            sf.write(os.path.join(levdir, file[:-4] + '_' + '{:02d}'.format(lev) + '.wav'), sig1, fs, subtype='PCM_24')

if __name__=="__main__":
    main()