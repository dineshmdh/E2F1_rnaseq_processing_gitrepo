#!/bin/bash
#
# Created on Dec 11, 2016 (b/c htseq threw some max_buffer error with e2f1.bam (~30G) sorted by pos.
#
# 
#SBATCH --job-name=samtools_sort # this "#SBATCH" is read by SLURM and not left out as a comment.
##SBATCH --output=samtools.out
#SBATCH --mem=70G # Same as above. If u want to specify a memory of 1000Mb just remove that extra # at the beginning here.

samtools sort -n -@ 12 -o ../../Output/hisat2/e2f_assembled_sortedByName.bam -O bam -m 5G ../../Output/hisat2/e2f_assembled_sortedByPos_copy.bam

