#!/usr/bin/env python3 
###-----------------------------------------------------------------------------------------##
#
#@author narumeena
#@description calculating allele imbalance based on gnomad allel frequecy 
#source https://davetang.org/muse/2017/03/10/gnomad-allele-frequency-pathogenic-clinvar-variants/
###------------------------------------------------------------------------------------------##


import gzip
import hail as hl 
hl.init(default_reference='GRCh38')  

def main():
    #chromosome 21 for testing 
    clinvar_path            =   "../../../analysis/variantsMappedOnnORFs/clinvar/clivar_db_v2_Pathogenic_only_with_chr.vcf.bgz"
    #all genome Grch38
    #hail_v3_vcf_grch38  =   "../../../data/gnomAD/gnomad.genomes.r3.0.sites.vcf.bgz"
    #chr21 = hl.import_vcf(vcf_path)

    #import whole genome 
    genome  =   hl.import_vcf(clinvar_path, reference_genome='GRCh38')
    db      =   hl.experimental.DB()
    genome      =   db.annotate_rows_db(genome, "gencode")

    print(genome.rows().select().show(5))
    print(hl.methods.summarize_variants(genome))
    

if __name__ == "__main__":
    main()