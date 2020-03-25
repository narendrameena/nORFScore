#!/usr/bin/env python3 
###-----------------------------------------------------------------------------##
#
#@author narumeena
#@descripton class and function to extract data from diffrent sources
#
###-----------------------------------------------------------------------------##

import pandas as pd
import pysam
import requests
from clint.textui import progress
import calendar
import time

class readFiles():
    def __init__(self):
        pass
    
    
        
    def fileDownload(self,url,filePath,fileName):

        """
        
        downloaidn a file from URL and storing it at given filePathe and fileName

        :param  url:         URL to downlaod the file
        :param  filePath:    filePathe where the file should be saved
        :param  fileName:    name of the file
        :return:             file pathe of the file
        
        """
        start_timestamp = calendar.timegm(time.gmtime())

        r = requests.get(url, stream=True)
        with open(filePath+fileName, "wb") as fileData:
            if r.status_code != 200:
                print("URL is not accessible, please provide a valid URL" )
                return "status code: " + str(r.status_code )
            else: 
                print("File available at given URL")
                totalLength = int(r.headers.get('content-length'))
                print("file Size: " + str(totalLength))
                for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(totalLength/1024) + 1):
                    if ch:
                        fileData.write(ch)

                stop_timestamp = calendar.timegm(time.gmtime())
                print("Total time to download the file: %d seconds" %(stop_timestamp-start_timestamp))

                return filePath + fileName


    def readBedGz(self, filePath):

        """

        reading a bed.gz as panda dataframe function 

        :param filePath: filepath for the bed.gz file
        :return:    data as panda dataframe

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
    #df = readBedGz.readBedGz(rightFilePath)   #should return a panda dataframe
    #print("summary of the dataframe\n")
    #print(df.head())
    #ßreadBedGz.readBedGz(wrongFilePath)   #should return a empty dataframe, also print a exception 
    url =   'https://www.encodeproject.org/files/ENCFF281ASO/@@download/ENCFF281ASO.bed.gz'

    print(readBedGz.fileDownload(url,'/mnt/hdd1/narendra/cambridge/projects/inProgress/nORFScore/code/python/data/test/','test.bed.gz'))


if __name__ == "__main__":
    main()
