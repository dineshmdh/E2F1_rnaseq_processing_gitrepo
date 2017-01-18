#!/bin/bash
# 
#SBATCH --job-name=htseq # this "#SBATCH" is read by SLURM and not left out as a comment.
#SBATCH --mem=70G # Same as above. If u want to specify a memory of 1000Mb just remove that extra # at the beginning here.

featureCounts -p -B -t exon -g gene_id -a ../../Homo_sapiens.knownGene.hg19.sorted.withGenes.gtf -o e2f1_featureCounts.txt -T 12 ../hisat2/e2f_assembled_sortedByPos.bam
