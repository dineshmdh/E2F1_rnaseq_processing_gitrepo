# Created on Dec 06, 2016
# 
# Save the sortmerna_[1/2].fastq outputs (also if i want to run fastqc on them later). Remove the other files.

import os
import re
import collections as col
import time

rank = os.environ['SLURM_ARRAY_TASK_ID']

inputDir_base = "/work/dm237/e2fs/raw_data"
outputDir_base = "/work/dm237/e2fs/Output"
if not (os.path.exists(outputDir_base+"/sortmerna")):
    os.makedirs(outputDir_base+"/sortmerna")


sortmerna_db = "/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/rfam-5.8s-database-id98.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/rfam-5.8s-database-id98:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/rfam-5s-database-id98.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/rfam-5s-database-id98:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-arc-16s-id95.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-arc-16s-id95:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-arc-23s-id98.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-arc-23s-id98:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-bac-16s-id90.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-bac-16s-id90:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-bac-23s-id98.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-bac-23s-id98:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-euk-18s-id95.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-euk-18s-id95:/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-euk-28s-id98.fasta,/dscrhome/dm237/bin/sortmerna-2.1b/rRNA_databases/silva-euk-28s-id98" # copied from bash variable $SORTMERNA_DB in compute01, which was created following sortmerna manual


def get_inputPairs(filePath):
    '''
    Get a tuple of pairs on which to perform the sortmerna, including merging and unmerging
    '''
    files = os.listdir(filePath)
    files_R1 = sorted([x for x in files if "_R1" in x]) # forward reads
    files_R2 = sorted([x for x in files if "_R2" in x]) # reverse reads
    assert len(files_R1) == len(files_R2)
    
    pairs = []
    for areadPair in zip(files_R1, files_R2):
	forward, reverse = areadPair
	assert re.split("_R1", forward) == re.split("_R2", reverse) 
	readPair_wPath = [filePath+"/"+forward, filePath+"/"+reverse]
	pairs.append(readPair_wPath)
    return pairs


def run_sortmerna(forwardFile, reverseFile, outputDir):
    '''
    Note the files have full path as well. The path is to the raw read directories.
    Example of how to call command line:     
    sortmerna --ref $SORTMERNA_DB --reads LS07_CGATGT_L005_merged_001.fastq --paired_in -a 16 --log --fastx --aligned LS07_CGATGT_L005_subset_rRNA --other LS07_CGATGT_L005_subset_sortmerna
    
    Here, I need to do these in sequence:
    1. Unzip the copied fastq.gz files
    2. merge the reads (that are in the outputDir) using sortmerna merging script
    3. run sortmerna as in the example above. (This will take about 15-20 mins)
    4. Unmerge the _subset_sortmerna.fastq file to forward and reverse reads (using sortmerna unmerging script)
    5. Remove all the non-relevant files: raw reads copied, merged raw reads, original sortmerna output which is merged
    6. (Optional) compress the subset_rRNA.fastq outputs yielded by sortmerna
    '''
    start_time = time.time()
    print("    copying the read files")
    os.system("cp "+forwardFile+" "+outputDir)
    os.system("cp "+reverseFile+" "+outputDir)
    os.chdir(outputDir) # CHANGING WORKING DIRECTORY TO OUTPUTDIR
   
    forwardFileName = forwardFile[forwardFile.rfind("/")+1 : ] # getting rid of .gz
    reverseFileName = reverseFile[reverseFile.rfind("/")+1 :]
 
    print("unzipping the .gz files")
    os.system("gunzip "+forwardFileName)
    os.system("gunzip "+reverseFileName)

    forwardFileName = forwardFileName[: -3] # getting rid of .gz
    reverseFileName = reverseFileName[: -3]

    print("    merging the read files")
    mergedFileName = "_merged_".join(re.split("_R1_",forwardFileName)) 
    os.system("/dscrhome/dm237/bin/sortmerna-2.1b/scripts/merge-paired-reads.sh "+forwardFileName+" "+reverseFileName+" "+mergedFileName)

    print("    running sortmerna on the merged files")
    sortmerna_prefix = "_".join(re.split("_merged_", mergedFileName))
    sortmerna_prefix = sortmerna_prefix[ : sortmerna_prefix.find(".fastq")]
    os.system("sortmerna --ref "+sortmerna_db+" --reads "+mergedFileName+" --paired_in -a 16 --log --fastx --aligned "+sortmerna_prefix+"_subset_rRNA --other "+sortmerna_prefix+"_subset_sortmerna")

    # now unmerge (is this actually required for trimmomatic) and remove the unnecessary files
    os.system("rm "+forwardFileName); 
    os.system("rm "+reverseFileName)
    os.system("rm "+mergedFileName) # now that the *_subset_sortmerna.fastq is generated, this can be deleted.
    os.system("rm *subset_rRNA.fastq")
    os.system("/dscrhome/dm237/bin/sortmerna-2.1b/scripts/unmerge-paired-reads.sh "+sortmerna_prefix+"_subset_sortmerna.fastq "+sortmerna_prefix+"_subset_sortmerna_R1.fastq "+sortmerna_prefix+"_subset_sortmerna_R2.fastq")
    os.system("rm "+sortmerna_prefix+"_subset_sortmerna.fastq") #no need of this file after unmerging
    print("Time taken for sortmerna is", time.time() - start_time) 
    
    #return sortmerna_prefix+"_subset_sortmerna_R1.fastq", sortmerna_prefix+"_subset_sortmerna_R2.fastq"



readPairs = get_inputPairs(inputDir_base)

currReadPair = readPairs[int(rank)-1]
forward_forSort, reverse_forSort = currReadPair # for sortmerna

# run sortmerna and trimmomatic
run_sortmerna(forward_forSort, reverse_forSort, outputDir_base+"/sortmerna")



