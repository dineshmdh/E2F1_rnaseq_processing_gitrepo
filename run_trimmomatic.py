'''
Created on Dec 06, 2016

Run trimmomatic and save the output for hisat2.
Some of the functions are copied from run_sortmerna.py.
'''

import os
import re
import collections as col
import time 


rank = os.environ['SLURM_ARRAY_TASK_ID']

baseDir = "/work/dm237/e2fs/Output"
inputDir_base = baseDir+"/sortmerna"
outputDir = baseDir+"/trimmomatic"
if not (os.path.exists(outputDir)):
    os.makedirs(outputDir)

adapters_fa = "/dscrhome/dm237/bin/trimmomatic/trimmomatic-0.36/adapters/TruSeq3-PE-2.fa"

def get_inputPairs(filePath):
    files = os.listdir(filePath)
    files_R1 = sorted([x for x in files if "_R1.fastq" in x]) # forward reads
    files_R2 = sorted([x for x in files if "_R2.fastq" in x]) # reverse reads
    assert len(files_R1) == len(files_R2)
    readPairs = []
    for areadPair in zip(files_R1, files_R2):
        forward, reverse = areadPair
        assert re.split("_R1.", forward) == re.split("_R2.", reverse)
        readPair_wPath = [filePath+"/"+forward, filePath+"/"+reverse]
        readPairs.append(readPair_wPath)
    return readPairs


def run_trimmomatic(forwardFile, reverseFile, outputPath):
    '''
    forwardFile is like this: /full/path/LS05_CTTGTA_L008_001_subset_sortmerna_R1.fastq
    
    If ILLUMINACLIP:/adapters:2:30:10, then Trimmomatic will look for seed matches (16 bases) allowing maximally 2
    mismatches. These seeds will be extended and clipped if in the case of paired end
    reads a score of 30 is reached (about 50 bases), or in the case of single ended reads a
    score of 10, (about 17 bases)

    If SLIDINGWINDOW:4:15, then Scan the read with a 4-base wide sliding window, cutting when the average quality per
    base drops below 15
    '''
    forwardFile_name = forwardFile[forwardFile.rfind("/")+1:]
    outFileName_prefix = re.split("_R1.", forwardFile_name)[0]
    out_pre = outputPath+"/"+outFileName_prefix # just a shorthand (will be using a lot below)
    cmd = "trimmomatic PE -threads 12 -trimlog "+out_pre+"_trimmomatic.log "+forwardFile+" "+reverseFile+" "+out_pre+"_trimmomatic_R1.fastq "+out_pre+"_trimmomatic_unpaired_R1.fastq "+out_pre+"_trimmomatic_R2.fastq "+out_pre+"_trimmomatic_unpaired_R2.fastq ILLUMINACLIP:"+adapters_fa+":2:30:10 SLIDINGWINDOW:5:20 MINLEN:32"
    print("trimming..")
    start_time  = time.time()
    print(cmd)
    os.system(cmd)
    print("Time taken is:", time.time() - start_time)



readPairs = get_inputPairs(inputDir_base)
forwardFile, reverseFile = readPairs[int(rank)-1]
print("working on pair", forwardFile, reverseFile)
run_trimmomatic(forwardFile, reverseFile, outputDir)





