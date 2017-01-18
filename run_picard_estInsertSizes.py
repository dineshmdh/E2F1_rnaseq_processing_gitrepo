# Created on Dec 14, 2016


import os
import re


inputDir = "/work/dm237/e2fs/Output/hisat2"
outputDir = "/work/dm237/e2fs/Output/picard_insertSizes"

rank = os.environ['SLURM_ARRAY_TASK_ID']

def get_inputFiles():
    files = os.listdir(inputDir)
    inFiles = [x for x in files if ("_L002_001_assembled_sorted.bam" in x) and not (".bai" in x)]
    return inFiles


inFiles = get_inputFiles()
inFile = inFiles[int(rank)-1]
print("estimating insert size for ", inFile)

outFilePrefix = re.split("_assembled", inFile.strip())[0]+"_picardInsertSize"
picard_cmd="picard CollectInsertSizeMetrics I="+inputDir+"/"+inFile+" O="+outputDir+"/"+outFilePrefix+".txt H="+outputDir+"/"+outFilePrefix+".pdf" 

print("picard cmd: ", picard_cmd)
os.system(picard_cmd)


