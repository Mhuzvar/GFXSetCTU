import torch
from torch import nn
from torch.utils.data import DataLoader
import modules.preprocess as mprep
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt
import time
import argparse

def list_of_ints(arg):
    return list(map(int, arg.split(',')))

torch.cuda.empty_cache()
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    raise Exception("Cuda not available!")

class LSTM(nn.Module):
    def __init__(self, l1features, hdim, hnum):
        super().__init__()

        self.hdim = hdim
        self.hnum = hnum

        self.hidden1 = nn.Linear(1, l1features)
        self.act1 = nn.Tanh()
        self.hidden2 = nn.LSTM(l1features, hdim, num_layers=hnum, batch_first=True)
        self.output = nn.Linear(hdim, 1)
        self.act_output = nn.Tanh()
 
    def forward(self, x, h=None):
        if h == None:
            h = (Variable(torch.zeros(self.hnum, x.size(0), self.hdim)).to(device),
                 Variable(torch.zeros(self.hnum, x.size(0), self.hdim)).to(device))
        x = self.act1(self.hidden1(x))
        x, h = self.hidden2(x, h)
        x = self.act_output(self.output(x))
        return x, h

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--lr_decay", default=0, type=float, help="set learning rate decay (default = 0 acts the same as 1)")
    parser.add_argument("-l", "--levels", default=[0,6,12,18,24,30], type=list_of_ints, help="set signal levels for training")
    parser.add_argument("-t", "--trial", default=0, type=int, help="trial number in case of multiple runs with the same parameters")
    parser.add_argument("-n", "--l_comb_name", default='0', type=str, help="designation of level combination")
    args = parser.parse_args()

    levname = args.l_comb_name

    trial = args.trial
    n_input = 1 # single input stream
    n_steps = 44100 # timesteps
    batch_size = 16 # batch of data

    tr_levels = args.levels
    te_levels = [0, 6, 10, 12, 18, 20, 24, 30]
    testlist, trainlist = mprep.separate_data(input_dir='dataset/raw', label_dir='dataset/labels', settings=[], wlen=n_input, slen=n_steps)

    TrainSet = mprep.GuitarDataset(trainlist, wlen=n_input, slen=n_steps, lev=tr_levels)
    TestSet = mprep.GuitarDataset(testlist, wlen=n_input, slen=n_steps, lev=te_levels)

    TrainLoader = DataLoader(TrainSet, batch_size=batch_size, shuffle=True, drop_last=True)
    TestLoader = DataLoader(TestSet, batch_size=batch_size, shuffle=True, drop_last=True)

    torch.cuda.empty_cache()

    # Training Parameters
    n_adamAlpha = 1e-3
    n_adamEpsilon = 1e-8
    maxgrad = 1
    wd = 1e-12
    lr_decay = args.lr_decay

    l1features = 10
    hdim = 25
    hnum = 5

    model = LSTM(l1features, hdim, hnum).to(device)
    lossFunction = torch.nn.MSELoss().to(device)
    optimizer = torch.optim.Adam(model.parameters(),lr=n_adamAlpha,eps=n_adamEpsilon, weight_decay=wd)

    n_epochs = 100
    losses = np.zeros(n_epochs)
    losses_ctrl = np.zeros(n_epochs)

    best_loss = np.Inf

    aalpha = n_adamAlpha
    ts = time.time()
    for i in range(n_epochs):
        model.train()
        for x, y in TrainLoader:
            x = x.to(device)
            y = y.to(device)
            y_hat, _ = model(x)
        
            loss = lossFunction(y,y_hat)
        
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), maxgrad)
            optimizer.step()

        with torch.no_grad():
            model.eval()
            val_losses = []
            val_losses_ctrl = []
            for j in TestSet.lev:
                TestSet.setlevel(j)
                for xe, ye in TestLoader:
                    xe = xe.to(device)
                    ye = ye.to(device)
                    ye_hat, _ = model(xe)
                    loss = lossFunction(ye,ye_hat)
                    val_losses.append(loss.detach().cpu().numpy())
                    if j in TrainSet.lev:
                        val_losses_ctrl.append(loss.detach().cpu().numpy())
            losses[i] = np.mean(val_losses)
            losses_ctrl[i] = np.mean(val_losses_ctrl)
            if losses[i] < best_loss:
                print(f"current loss = {losses[i]:.10f}, lowest loss = {best_loss:.10f}" )
                best_loss = losses[i]
                torch.save(model.state_dict(), f'output/{n_adamAlpha:.2e}_{n_adamEpsilon:.2e}_{lr_decay}_{levname}_{trial}.pt')
        model.train()
        if lr_decay>0:
            aalpha = lr_decay*aalpha
            for param_group in optimizer.param_groups:
                param_group['lr'] = aalpha
    Te = (time.time()-ts)/n_epochs

    with open('timer.txt', 'a') as f:
        f.write(f'one epoch run time (h:m:s): {int(np.floor(Te/3600))}:{int(np.floor(Te/60)-(np.floor(Te/3600)*60)):02d}:{Te-np.floor(Te/60)*60:06.3f}\n')

    with open(f'output/{n_adamAlpha:.2e}_{n_adamEpsilon:.2e}_{lr_decay}_{levname}_t_{trial}.txt', 'w') as f:
        for i in losses:
            f.write(f"{i}\n")

    with open(f'output/{n_adamAlpha:.2e}_{n_adamEpsilon:.2e}_{lr_decay}_{levname}_{levname}_{trial}.txt', 'w') as f:
        for i in losses_ctrl:
            f.write(f"{i}\n")

if __name__=="__main__":
    main()
