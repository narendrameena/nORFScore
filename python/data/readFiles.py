#!/usr/bin/env python3 
###-----------------------------------------------------------------------------##
#
#@author narumeena
#@descripton class and function to extract data from diffrent sources
#
###-----------------------------------------------------------------------------##

import pandas as pd

class readFiles():
    def __init__(self):
        pass
    
    def readBedGz(self, filePath):
        """

        reading bed.gz as panda dataframe function 

        :arg filePath: filepath for the bed.gz file
        :return :data as panda dataframe

        """
        df  =   []
        try:
            colNames=["chrom", "chromStart", "chromEnd", "name","score","strand","signalValue","pValue","qValue","peak"]
            df  =   pd.read_csv(filePath, compression='gzip', names=colNames, header=0, sep='\t')
        except IOError:
            print("Could not read file:" + filePath + "please check if file exist and in bed.gz formate")
        else:
            print("successfully read the file:", filePath )

        return df
        



def main():
    rightFilePath   =   "/mnt/hdd1/narendra/cambridge/projects/inProgress/nORFScore/data/encode/data/ENCFF744DYN.bed.gz"
    #wrongFilePath   =   "ENCFF744DYN.bed.gz"
    readBedGz   =   readFiles()
    df = readBedGz.readBedGz(rightFilePath)   #should return a panda dataframe
    print("summary of the dataframe\n")
    print(df.head())
    #ßreadBedGz.readBedGz(wrongFilePath)   #should return a empty dataframe, also print a exception 


if __name__ == "__main__":
    main()
