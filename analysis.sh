# combine the two genomes
cat genome/yeast.fa genome/transposon.fa > combined.fa
# Trim/filter the data
TrimmomaticPE A0171771A_1.fq A0171771A_2.fq A0171771A_1.trim.fq A0171771A_1.untrim.fq A0171771A_2.trim.fq A0171771A_2.untrim.fq SLIDINGWINDOW:4:20 MINLEN:25
# build indexes of the combined genome
bowtie2-build genome/combined.fa genome/combined
export BOWTIE2_INDEXES=$(pwd)/genome
# align the paired ends to the genome
bowtie2 -x combined -very-fast -p 4 -1 A0171771A_1.trim.fq -2 A0171771A_2.trim.fq -S A0171771A.sam
# convert sam file to bam file
samtools view -S -b A0171771A.sam > A0171771A.bam
# sort the BAM file
samtools sort A0171771A.bam -o A0171771A_sorted.bam
samtools index A0171771A_sorted.bam
# filter the BAM file; FLAG = 4,8 and MAPQ < 13
samtools view -F 8 -F 4 -q 13 -b A0171771A_sorted.bam > A0171771A_filtered.bam
samtools index A0171771A_filtered.bam