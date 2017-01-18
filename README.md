# E2F1_rnaseq_processing
Processing done on E2F1 rnaseq data across 6 conditions; used in Igor's paper.

All the scripts ending in .q were run in SLURM for parallel processing of the samples and call their corresponding .py script. 

Details of the processing (also mentioned in the Methods section in the paper) is as follows:

E2F1 RNA-seq processing

The raw data can be downloaded from GEO using the accession number GSE93365. There were 5 forward (_R1.fastqz) and corresponding 5 reverse (_R2.fastqz) raw fastq files. The forward-reverse pairs were labeled “S1” to “S5” and corresponded to the following conditions:

S1: parental U2OS with serum
S2: U2OS YFP-ER-E2F1 sorted YFP-negative fraction 
S3: U2OS YFP-ER-E2F1 sorted YFP-low fraction
S4: U2OS YFP-ER-E2F1 sorted YFP-medium fraction
S5: U2OS YFP-ER-E2F1 sorted YFP-high fraction 

The raw fastq files were processed with sortmerna (1) and trimmomatic (2) to filter out the rRNA and adapter sequences respectively. The output reads were then aligned to the h19 genome assembly using HISAT2 (3). Afterwards, the read counts were obtained for each gene using HTSeq (4), under the default “-m union” mode. The GTF file used for HTSeq was obtained from the PrimerSeq library ((5), http://primerseq.sourceforge.net/gtf.html). The raw counts mapping to the genes were then converted to transcripts per million (TPM) values. For this, the mean fragment length for each condition (S1-S6) were computed using the Picard “CollectInsertSizeMetrics” module (https://broadinstitute.github.io/picard/). 


References

1.	Kopylova, E., Noe, L. and Touzet, H. (2012) SortMeRNA: fast and accurate filtering of ribosomal RNAs in metatranscriptomic data. Bioinformatics, 28, 3211-3217.
2.	Bolger, A.M., Lohse, M. and Usadel, B. (2014) Trimmomatic: a flexible trimmer for Illumina sequence data. Bioinformatics, 30, 2114-2120.
3.	Kim, D., Langmead, B. and Salzberg, S.L. (2015) HISAT: a fast spliced aligner with low memory requirements. Nature methods, 12, 357-360.
4.	Anders, S., Pyl, P.T. and Huber, W. (2015) HTSeq--a Python framework to work with high-throughput sequencing data. Bioinformatics, 31, 166-169.
5.	Tokheim, C., Park, J.W. and Xing, Y. (2014) PrimerSeq: Design and visualization of RT-PCR primers for alternative splicing using RNA-seq data. Genomics Proteomics Bioinformatics, 12, 105-109.


