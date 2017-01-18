'''
Created on Dec 08 2016.

Note: The hisat2 was run using hg19 genome. So, it is important that the
gtf file being used for htseq is also for hg19 assembly.

In runs 1 and 2, the bam files were sorted by position but htseq threw 
max_buffer reached error. So, for run3, the bam file used is sorted by name.
'''

import os
import re
import collections as col
import time


rank = os.environ['SLURM_ARRAY_TASK_ID']
inputDir = "/work/dm237/e2fs/Output/hisat2"
outputDir = "/work/dm237/e2fs/Output/htseq"
gtf_file = "/work/dm237/e2fs/Homo_sapiens.knownGene.hg19.sorted.withGenes.gtf"


def run_htseq(inputBamFile, outputFileName):
    print("working with bam file", inputBamFile)
    cmd = "htseq-count -f bam -r name --stranded no --type exon --idattr gene_id -m union "+inputDir+"/"+inputBamFile+" "+gtf_file+" > "+outputDir+"/"+outputFileName
    os.system(cmd)
    


bamFiles = [x for x in os.listdir(inputDir) if ("_L002_001_assembled_sorted.bam" in x) and not (".bai" in x)]
bamFile = bamFiles[int(rank)-1]
outFile = bamFile[:-4]+"_counts.txt"
run_htseq(bamFile, outFile)


