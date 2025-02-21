#!/bin/bash
#PBS -N LSTM_model
#PBS -l select=1:ncpus=1:mem=8gb:ngpus=1:scratch_local=8gb
#PBS -l walltime=26:00:00

# define a DATADIR variable: directory where the input files are taken from and where output will be copied to
DATADIR=/home/user/project      # placeholder, edit to fit your needs
OUTDIR=/home/project/output     # also a placeholder

SEQ='0'
TRIAL=0
if ! [ -d $DATADIR/trialcount/levcomp/$SEQ ];
then
    mkdir $DATADIR/trialcount/levcomp/$SEQ
fi

while [ -f $DATADIR/trialcount/levcomp/$SEQ/$TRIAL ];
do
    ((TRIAL++))
done
touch $DATADIR/trialcount/levcomp/$SEQ/$TRIAL

# append a line to a file "jobs_info.txt" containing the ID of the job, the hostname of node it is run on and the path to a scratch directory
# this information helps to find a scratch directory in case the job fails and you need to remove the scratch directory manually
echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $DATADIR/jobs_info.txt

# test if scratch directory is set
# if scratch directory is not set, issue error message and exit
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

# copy input files to scratch directory
# if the copy operation fails, issue error message and exit
cp $DATADIR/containers/container.sif  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }     # subtitute for your container location
cp $DATADIR/main.py  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp -r $DATADIR/modules  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp -r $DATADIR/dataset  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

# move into scratch directory
cd $SCRATCHDIR

mkdir output

#cuddly chainsaw test
singularity exec --nv container.sif python main.py -d 0.999 -n $SEQ -l 0,30 -t $TRIAL            # check container name and other parameters

cp -r $OUTDIR/timer.txt  $SCRATCHDIR/output/ || { echo >&2 "Error while copying input file(s)!"; exit 2; }
singularity exec container.sif python modules/timer.py

# move the output to user's DATADIR or exit in case of failure
cp -r $SCRATCHDIR/output/* $OUTDIR || { echo >&2 "Result file(s) copying failed (with a code $?)"; exit 4; }

# clean the SCRATCH directory
clean_scratch
