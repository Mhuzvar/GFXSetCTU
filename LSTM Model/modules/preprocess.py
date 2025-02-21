# preprocessing script/module for guitar dataset
#
# Matej Huzvar
# Prague, February 2024
# Work in progress

import os
import numpy as np
import soundfile as sf
import torch
import torchaudio
import random
from torch.utils.data import Dataset

cwd = os.getcwd()
fs = 44100

def load_audio(filename):
    """
    Loads .wav, checks if fs is 44.1 kHz and returns torch tensor with the waveform.
    """
    sig, fss = torchaudio.load(filename)
    if fs != fss:
        print("Wrong sample rate in file " + filename + "!")
        return None
    return sig

def minwstep(slen, wlen, mode=True):
    """
    Finds maximum wstep to minimize removed parts of signal when cutting into segments.
    Only allows wstep > 0.9*wlen
    """

    wstep = wlen
    wnum = slen//wlen
    loss = slen - wnum*wlen
    if loss == 0:
        return wstep, wnum, 0
    for i in range(wstep, int(np.floor(0.9*wlen)),-1):
        wn = np.floor((slen-wlen)/i)
        if slen - i*(wn)+wlen < loss:
            wstep = i
            wnum = wn+1
            loss = slen - i*(wn)+wlen
        if loss == 0:
            return wstep, wnum, 0
    if mode:
        return wstep, wnum, random.randint(0,loss)
    else:
        return wstep, wnum, loss

def separate_data(input_dir='dataset/inputs', label_dir='dataset/labels', dev='bds1', settings=[12, 12], wlen=1, slen=5000, save=False):
    # structure: 
    #   pair input name to output name (without level)
    #   when file gets called, level will be randomly chosen
    #   + solves risk of overfitting caused by data being too similar
    trlist = [] # list of tuples in format (raw path, label path, index, wiggle)
    telist = []
    for file in os.listdir(input_dir):
        infile = os.path.join(input_dir, file)

        # getting label name
        outbase = file[:-4]
        if settings == []:
            outfile = os.path.join(label_dir, dev, outbase)
        else:
            sts = ''
            for i in settings:
                sts = sts + f"{settings[0]:02d}_"
            outfile = os.path.join(label_dir, dev, sts[:-1], outbase)
        
        raw, _ = sf.read(infile, dtype='float32')
        
        # cutting into smaller windows
        outsiglen = wlen*slen
        wstep, wnum, loss = minwstep(raw.size, outsiglen, True)

        for i in range(wnum):
            st = i*wstep + loss
            if random.randint(0,99)<20:     # test
                if not telist:
                    telist = [(infile, outfile, st, wstep)]
                else:
                    telist.append(((infile, outfile, st, wstep)))
            else:                           # train
                if not trlist:
                    trlist = [(infile, outfile, st, wstep)]
                else:
                    trlist.append(((infile, outfile, st, wstep)))

    if save:                                    # doesnt really work
        with open('testlist.txt','w') as flist:
            flist.write(telist)
        with open('trainlist.txt','w') as flist:
            flist.write(trlist)
    else:
        return telist, trlist


    if save:                                    # doesnt really work
        with open('testlist.txt','w') as flist:
            flist.write(telist)
        with open('trainlist.txt','w') as flist:
            flist.write(trlist)
    else:
        return telist, trlist

class GuitarDataset(Dataset):
    def __init__(self, flist, transform=None, target_transform=None, wlen=1, slen=5000, lev = []):
        self.flist = flist                          # list of tuples in format (raw path, label path, index, wiggle)
        self.wlen = wlen
        self.slen = slen
        self.transform = transform
        self.target_transform = target_transform
        self.lev = lev
        self.currentlevel = []

    def __len__(self):
        return len(self.flist)

    def __getitem__(self, idx):
        raw = load_audio(self.flist[idx][0])
        if self.lev == []:
            label = load_audio(self.flist[idx][1])
        elif isinstance(self.lev, list):
            if self.currentlevel == []:
                lvl = self.lev[random.randint(0, len(self.lev)-1)]
            else:
                lvl = self.currentlevel
            raw = raw/torch.max(torch.abs(raw))
            raw = raw*(10**(-lvl/20))
            label = load_audio(self.flist[idx][1] + f"_{lvl:02d}.wav")
        else:
            raise Exception("Wrong levels input! Must be a list or []")

        raw, label = raw[:,self.flist[idx][2]:self.flist[idx][2]+self.wlen*self.slen], label[:,self.flist[idx][2]:self.flist[idx][2]+self.wlen*self.slen]

        # reshape to L x H_in (time x wlen)
        raw = torch.reshape(raw, (raw.size(dim=1)//self.wlen, self.wlen))
        label = torch.reshape(label, (label.size(dim=1)//self.wlen, self.wlen))

        if self.transform:
            raw = self.transform(raw)
        if self.target_transform:
            label = self.target_transform(label)
        return raw, label
    
    def setlevel(self, lev):
        self.currentlevel = lev

def test_function():
    #if len(os.listdir("dataset/prepped/test/input"))==0:
    #    prep_v2()
    #if len(os.listdir("dataset/ssprepped/test/input"))==0:
    #    prepare_sinesweep()

    telist, trlist = separate_data(input_dir='dataset/allnoon_v2/raw', label_dir='dataset/allnoon_v2/labels', settings=[], save=False)
    trainset = GuitarDataset(trlist, lev=[0])
    testset = GuitarDataset(telist, lev=[0])
    print(len(trainset))
    print(len(testset))
    raw, lab = trainset[0]
    print(raw.dtype)

if __name__=="__main__":
    test_function()
