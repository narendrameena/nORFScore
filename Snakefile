"""
@author narumeena
@description run four variant caller methods Genome Analysis Tool Kit HaplotypeCaller, Strelka2 and Samtools-Varscan2 and  deepvaraint from goggle on golden dataset 
"""


##------------------------------------------------------------------###
#base folder and diffrent global attributes 
##------------------------------------------------------------------###

BASE_DIR            = '/mnt/hdd1/narendra/cambridge/projects/inProgress/nORFScore/'

REF_DIR             = "/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/"
INDEX               = REF_DIR + "data/genome/GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly"
REF_FASTA           = REF_DIR + "data/genome/GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
REF_GTF             = REF_DIR + "data/genome/GRCh38/Homo_sapiens.GRCh38.98.gtf"


###--------------------------------------------------------------------------------##
#tools
###--------------------------------------------------------------------------------##

GATK            = "/mnt/hdd1/narendra/cambridge/projects/inProgress/tools/gatk-4.1.4.1/gatk"

samples = ["SRR8369888", "SRR8381428","SRR8454587","SRR8454590","SRR8591413"]


rule all:
    input:
        expand(BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem.bam", sample=samples)


rule fastp:
    input:
        read1 = BASE_DIR + "data/goldenDataSet/{sample}_1.fastq",
        read2 = BASE_DIR + "data/goldenDataSet/{sample}_2.fastq"
    output: 
        read1 = BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_1.fastq",
        read2 = BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_2.fastq"
    threads: 40
    shell:
        "fastp -i {input.read1} -o {output.read1} -I {input.read2} -O {output.read2} -w {threads}"
    

rule bwa:
    input:
        ref     = REF_FASTA,
        read1   = BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_1.fastq",
        read2   = BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_2.fastq"
    output:
        temp(BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem.bam")
    log:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem.log"
    threads: 40
    shell:
        "bwa mem -t {threads} {input} | samtools view -Sb - > {output} 2> {log}"


rule samtools_sort:
    input:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem.bam"
    output:
        protected(BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.bam")
    log:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.log"
    threads: 40
    shell:
        "samtools sort -O bam {input} -o {output} --threads {threads} > {log}"



rule samtools_index:
    input:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.bam"
    output:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.bam.bai"
    log:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.bam.bai.log"
    threads: 40
    shell:
        "samtools index {input} > {log}"

rule gatkMarkDuplicates:
    input:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.bam"
    output:
        bam         =   BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort_dedup.bam",
        matrixFile  =   BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort_dedup_matrix.txt"
    log:
        BASE_DIR + "analysis/goldenDatasetVcf/{sample}/{sample}_fastp_bwaMem_sort.dedup.log"
    threads: 40
    shell:
        GATK + "MarkDuplicates -I  {input} -M {output.matrixFile} -O {output.bam}> {log}"


