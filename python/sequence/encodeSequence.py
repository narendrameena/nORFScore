#!/usr/bin/env python3 
###--------------------------------------------------------------------------------------##
#
#@author narumeena
#@description encode a  sequence
#source https://www.biostat.wisc.edu/bmi776/spring-18/lectures/noncoding-variants.pdf
#
###--------------------------------------------------------------------------------------##

import pysam


def getsequence():

    # open vcf file
    vcf = pysam.VariantFile("../../../analysis/variantsMappedOnnORFs/clinvar/clivar_db_v2_Pathogenic_only_without_chr_sort.vcf",mode='r',threads=4)
    # open fasta file
    genome = pysam.FastaFile("../../../data/refrenceGenome/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa")
    # define by how many bases the variant should be flanked
    flank = 50

    # iterate over each variant
    for record in vcf:
        # extract sequence
        print(record)
        # The start position is calculated by subtract the number of bases
        # given by 'flank' from the variant position. The position in the vcf file
        # is 1-based. pysam's fetch() expected 0-base coordinate. That's why we
        # need to subtract on more base.
        #
        # The end position is calculated by adding the number of bases
        # given by 'flank' to the variant position. We also need to add the length
        # of the REF value and subtract again 1 due to the 0-based/1-based thing.
        #
        # Now we have the complete sequence like this:
        # [number of bases given by flank]+REF+[number of bases given by flank]
        seq = genome.fetch(record.chrom, record.pos-1-flank, record.pos-1+len(record.ref)+flank)

        # print out tab seperated columns:
        # CRHOM, POS, REF, ALT, flanking sequencing with variant given in the format '[REF/ALT]'
        print(
            record.chrom,
            record.pos,
            record.ref,
            record.alts[0],
            '{}[{}/{}]{}'.format(seq[:flank], record.ref, record.alts[0], seq[flank+len(record.ref):]),
            sep="\t"
        )




def main():
    getsequence()

    

if __name__ == "__main__":
    main()