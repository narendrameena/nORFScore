#!/usr/bin/env python3 
###-----------------------------------------------------------------------------------------##
#
#@author narumeena
#@description reading and Convert Parquet to CSV
#ß
#
###------------------------------------------------------------------------------------------##


import pandas as pd

def main():
    df = pd.read_parquet('../../../data/encode/Gene_expression_RNA-seq/GTEx/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_exon_reads.parquet')
    print(df.head())
    #df.to_csv('filename.csv')

    

if __name__ == "__main__":
    main()