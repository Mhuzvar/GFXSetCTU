'''
This script is meant to be used in synchronization of signals when recording data for guitar amp/effect dataset under <website>.
Version: 0.2.1

Matej Huzvar
huzvamat@fel.cvut.cz
Prague, September 2024
'''

import os
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def gen_pulse(n, fs=44100, maxf=10e3):
    sigma = 1/maxf
    var = np.square(sigma)
    maxt = 4*sigma

    t = np.linspace(-maxt, maxt, round(2*maxt*fs), endpoint=True)
    pulse = np.exp(-np.square(t)/(2*var))
    out = np.tile(pulse, n)
    return out

def gen_testsig(maxfvals=[100, 1e3, 10e3], n=[], pre=0, post=0, fs=44100, filename='gpulses.wav'):
    if n==[]:
        n = len(maxfvals)*[5]
    elif isinstance(n, int):
        n = len(maxfvals)*[n]
    tsig=np.zeros(pre)
    for i in range(len(maxfvals)):
        tsig = np.append(tsig, gen_pulse(n[i], fs=fs, maxf=maxfvals[i]))
    tsig = np.append(tsig, np.zeros(post))
    #plt.plot(tsig)
    #plt.show()
    sf.write(filename, tsig, fs, subtype='PCM_24')

def xcorr(sig1, sig2):
    Rxy = np.correlate(sig1, sig2, "full")
    return Rxy

def sync(sig1, sig2):
    sig1=sig1/np.max(np.abs(sig1))
    sig2=sig2/np.max(np.abs(sig2))
    #plt.ion()
    if len(sig1)<len(sig2):
        sig2 = sig2[:len(sig1)]
    else:
        sig2 = np.append(sig2, np.zeros(len(sig1)-len(sig2)))
    sig2 = sig2 + min(sig1)-min(sig2)
    Rxx = np.correlate(sig1, sig1, "full")
    nolag = np.argmax(Rxx)
    Rxy = np.correlate(sig1, sig2, "full")
    amax = np.argmax(Rxy)
    lag = 0
    print(f"Detected lag: {nolag-amax} samples.")
    return nolag-amax

def gui_sync(sig1, sig2):
    sig1=sig1/np.max(np.abs(sig1))
    sig2=sig2/np.max(np.abs(sig2))
    plt.ion()
    if len(sig1)<len(sig2):
        sig2 = sig2[:len(sig1)]
    else:
        sig2 = np.append(sig2, np.zeros(len(sig1)-len(sig2)))
    sig2 = sig2 + min(sig1)-min(sig2)
    Rxx = np.correlate(sig1, sig1, "full")
    nolag = np.argmax(Rxx)
    Rxy = np.correlate(sig1, sig2, "full")
    amax = np.argmax(Rxy)
    lag = 0
    print(f"Detected lag: {nolag-amax} samples. No adjustment made yet.")
    startplot = 0
    while True:
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        line1, = ax.plot(sig1[startplot:min(startplot+2000, len(sig1))], 'b-')
        line2, = ax.plot(sig2[startplot:min(startplot+2000, len(sig1))], 'r-')
        plt.show()
        newlag = int(input("Type number of samples for correction (0 to finish sync): "))
        lag += newlag
        if newlag == 0:
            return lag
        startplot = int(input(f"Current start index: {startplot}, New start index: "))
        sig2 = np.roll(sig2, -newlag)

def nudge_file(filename, indir, outdir, n):     # check function
    sig, fs = sf.read(os.path.join(indir, filename))
    sig = np.roll(sig, -n)
    sf.write(os.path.join(outdir, filename), sig, fs)

def check_dim(filename):
    filename = filename[8:-16]
    dim = len(filename.split('_'))
    #for f in filename:
    #    if f=='_':
    #        dim+=1
    #dim+=1
    return dim

def opstr(data, idx):
    op = ''
    for i, j in enumerate(idx):
        op+=data[i][j]+'_'
    return op[:-1]

class datapiece():
    def __init__(self, devname, dim, options):
        self.name = devname
        self.dim = dim
        self.options = []
        for i in options:
            self.options.append([i])
    
    def expand(self, options):
        for i, op in enumerate(options):
            if not(op==[]) and not(op in self.options[i]):
                self.options[i].append(op)
    
    def initdata(self):
        arsize = []
        for i in range(self.dim):
            arsize.append(len(self.options[i]))
        self.synced = np.full(arsize, False)
        self.synced[tuple(self.dim*[0])]=True
        self.delay = np.ones(arsize)
    
    def find_idx(self, options):
        idx = []
        for i, op in enumerate(options.split('_')):
            idx.append(self.options[i].index(op))
        return tuple(idx)


class sdata():
    def __init__(self, flist):
        i = -1
        self.data = []
        self.devs = []
        for f in flist:
            dev = f[3:7]
            if not(dev in self.devs):
                self.devs.append(dev)
                self.data.append(datapiece(dev, check_dim(f), f[8:-16].split('_')))
                i+=1
            self.data[i].expand(f[8:-16].split('_'))
        for dt in self.data:
            dt.initdata()


def sync_folder(instfile, indir, outdir):       # finish
    with open(instfile, 'r') as slens:
        sl = slens.readlines()
        sl = [(f.split(' ')[0], int(f.split(' ')[1])) for f in sl]      # sigs and lens in (signame, len) formatted tuple
        filelist = [f for f in os.listdir(indir)]
        filelist = sorted(filelist)                                     # recorded signals to be synced

        syncdata = sdata(filelist)

        i = 0
        #while keepgoing:
        for i, f in enumerate(filelist):
            j = syncdata.devs.index(f[3:7])
            idx = syncdata.data[j].find_idx(f[8:-16])

            sig, fs = sf.read(os.path.join(indir, f))         # load first part of the recording

            if syncdata.data[j].synced[idx]:
                print("already synced!")
            else:
                idx_n = []
                for k in range(syncdata.data[j].dim):
                    if idx[k]>0:
                        idx_n.append([l for l in idx])
                        idx_n[-1][k]-=1
                        idx_n[-1]=tuple(idx_n[-1])
                    if idx[k]<len(syncdata.data[j].options[k])-1:
                        idx_n.append([l for l in idx])
                        idx_n[-1][k]+=1
                        idx_n[-1]=tuple(idx_n[-1])
                l = 0
                while not(syncdata.data[j].synced[idx_n[l]]):
                    l+=1
                m=0
                fref=[]
                while fref==[]:
                    if filelist[m][3:7]==syncdata.devs[j] and filelist[m][8:-16]==opstr(syncdata.data[j].options, idx_n[l]):
                        fref = filelist[m]
                    m+=1
                ref, fs = sf.read(os.path.join(outdir, fref))
                nudge = sync(ref[:20000], sig[:20000])
                if nudge>0:
                    sig = sig[nudge:]
                elif nudge<0:
                    sig = np.insert(sig, 0, np.zeros(-nudge))
                syncdata.data[j].synced[idx]=True
            
            sf.write(os.path.join(outdir, f), sig, fs)

def cut_folder(instfile, indir, outdir, lvls):
    n, fs = sf.read('dataset/dataset_final/raw/noise.wav')
    with open(instfile, 'r') as slens:
        sl = slens.readlines()
        sl = [(f.split(' ')[0], int(f.split(' ')[1])) for f in sl]      # sigs and lens in (signame, len) formatted tuple
        filelist = [f for f in os.listdir(indir)]
        filelist = sorted(filelist)                                     # recorded signals to be synced
        i = 0
        devs = []
        nudges = []
        keepgoing = True
        while keepgoing:
            sig, fs = sf.read(os.path.join(indir, filelist[i]))         # load first part of the recording
            fdir = os.path.join(outdir, filelist[i][3:7])
            subdir = os.path.join(fdir, filelist[i][8:-16])

            print(subdir)

            #i+=1
            if filelist[i][3:7] in devs:
                nudge = nudges[devs.index(filelist[i][3:7])]
            else:
                devs.append(filelist[i][3:7])
                nudges.append(gui_sync(n, sig[:n.size]))
                nudge = nudges[-1]

            sig = sig[nudge:]                                           # removing samples at beginning

            if not os.path.exists(fdir):
                os.makedirs(fdir)
                print('making directory ' + fdir)
            if not os.path.exists(subdir):
                os.makedirs(subdir)
                print('making directory ' + subdir)
            for lev in lvls:
                for f in sl:
                    fname = f[0] + '_' + lev + '.wav'
                    if sig.size < f[1]:
                        sig = np.append(sig, sf.read(os.path.join(indir, filelist[i]))[0])
                        i+=1
                    sf.write(os.path.join(subdir, fname), sig[:f[1]], fs)
                    sig = sig[f[1]+fs:]
            i+=1
            if i >= len(filelist):
                keepgoing = False

def main():
    print("\n============\nWarning!\nThis program works with unchecked inputs! Make sure inputs are in correct format and of reasonable values.\n============\n")
    mode = int(input("Modes:\n0 = synchronization\n1 = finalizing synchronized folder\nSelect one: "))
    if not mode:
        # syncing folder
        sync_folder('dataset/dataset_final/siglens.txt', 'dataset/dataset_final/to_sync', 'dataset/dataset_final/to_cut')
    else:
        cut_folder('dataset/dataset_final/siglens.txt', 'dataset/dataset_final/to_cut', 'dataset/dataset_final/labels', ['30', '00'])
        

if __name__=="__main__":
    main()
