#!/bin/bash

#SBATCH -o python_%A_%a.out # Standard output, %A is the placeholder for jobID and %a is the placeholder for arrayID (1-3, in this case)
#SBATCH -e python_%A_%a.err # Standard error
#SBATCH --array=1-6 # requesting 6 simultaneous runs of the following python script
#SBATCH --mem=20G

python run_trimmomatic.py




