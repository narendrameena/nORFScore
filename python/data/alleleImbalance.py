#!/usr/bin/env python3 
###-----------------------------------------------------------------------------------------##
#
#@author narumeena
#@description calculating allele imbalance based on gnomad allel frequecy 
#
###------------------------------------------------------------------------------------------##


import gzip
import hail as hl 
hl.init(default_reference='GRCh38')  



def main():
    #chromosome 21 for testing 
    vcf_path            =   "../../../data/gnomAD/gnomad.genomes.r2.1.1.sites.21.liftover_grch38.vcf.bgz"
    #all genome Grch38
    hail_v3_vcf_grch38  =   "../../../data/gnomAD/gnomad.genomes.r3.0.sites.vcf.bgz"
    chr21 = hl.import_vcf(vcf_path)

    #import whole genome 
    genome  =   mt = hl.import_vcf(hail_v3_vcf_grch38)

    print(genome.rows().select().show(5))
    

if __name__ == "__main__":
    main()