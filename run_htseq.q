#!/bin/bash
# 
#SBATCH --job-name=htseq_on_reps # this "#SBATCH" is read by SLURM and not left out as a comment.
#SBATCH --output=htseq_on_reps.out
#SBATCH --array=1-6 # requesting 6 simultaneous runs of the following python script
#SBATCH --mem=30G # Same as above. If u want to specify a memory of 1000Mb just remove that extra # at the beginning here.

python run_htseq.py 2&> htseq_run_onallReps.log

