'''
Created on Dec 7,2016

Run HiSAT2, sort the bam / sam file generated and generate the corresponding bai file as well. 
'''

import os
import re
import collections as col
import time

rank = os.environ['SLURM_ARRAY_TASK_ID']
baseDir = "/work/dm237/e2fs/Output"
inputDir = baseDir+"/trimmomatic"
outputDir = baseDir+"/hisat2"
if not (os.path.exists(outputDir)):
    os.mkdirs(outputDir)

genome_index = "/work/dm237/genome/hg19/genome"


def get_forward_and_reverse_readLists(filePath):
    '''
    Given a path with trimmomatic outputs, generate two lists of files (no path added) -- 
    one for the forward fastq files and one for the reverse. 
    The forward reads all have *_trimmomatic_R1.fastq file denominations, for instance. 
    Note: We are ignoring reads that are unpaired (*_trimmomatic_unpaired_R[1/2].fastq).
    '''
    files = os.listdir(filePath)
    reads_R1 = sorted([filePath+"/"+x for x in files if "_trimmomatic_R1.fastq" in x]) 
    reads_R2 = sorted([filePath+"/"+x for x in files if "_trimmomatic_R2.fastq" in x])
    assert len(reads_R1) == len(reads_R2)    
    return reads_R1, reads_R2


def run_hisat2(forwardFiles, reverseFiles, outputDir):
    '''
    Run hisat2 using forwardFiles (a list of _trimmomatic_R1.fastq files) and 
    reverseFiles (a list of _trimmomatic_R2.fastq files). 
    (Added on Dec 13, 2016: Note this list contains just one element for one 
    of 6 replicates)
    Also, sort the bam files and generate the .bai files (which might be usedi
    later to visualize the reads in a genome browser).
    '''
    fileName = re.split("/", forwardFiles[0].strip())[-1]
    out_prefix = re.split("_subset", fileName)[0]
    outFileName = out_prefix+"_assembled.sam"
    
    # run hisat2
    hisat2_start = time.time()
    hisat2_cmd = "hisat2 -p 12 -x "+genome_index+" -1 "+",".join(forwardFiles)+" -2 "+",".join(reverseFiles)+" -S "+outputDir+"/"+outFileName+" --add-chrname"
    os.system(hisat2_cmd)
    print("    hisat2 finished running. Time taken is", time.time() - hisat2_start)

    # get sorted bam
    sort_cmd = "samtools view -bS "+outputDir+"/"+outFileName+" | samtools sort - -o "+outputDir+"/"+outFileName[:-4]+"_sorted.bam"
    sort_start = time.time()
    os.system(sort_cmd)
    print("    now we have sorted bam. Time taken is", time.time() - sort_start)

    # create the bam index file
    bam_indx_cmd = "samtools index "+outputDir+"/"+outFileName[:-4]+"_sorted.bam "+outputDir+"/"+outFileName[:-4]+"_sorted.bam.bai"
    bam_indx_start = time.time()
    os.system(bam_indx_cmd)
    print("    bam index file created. Time taken is", time.time() - bam_indx_start) 

    # remove the sam file now
    os.system("rm "+outputDir+"/"+outFileName)
    print("    sam file is removed..")



readPairs_all = get_forward_and_reverse_readLists(inputDir)
forwardFiles_all, reverseFiles_all = readPairs_all # for all six read pairs
assert len(forwardFiles_all) == len(reverseFiles_all)


forwardFiles_this = [forwardFiles_all[int(rank)-1]] # selecting just one read pair
reverseFiles_this = [reverseFiles_all[int(rank)-1]]
run_hisat2(forwardFiles_this, reverseFiles_this, outputDir)



