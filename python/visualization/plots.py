###--------------------------------------------------------------------------------------##
#
#@author narumeena
#@description style the plots 
#
###--------------------------------------------------------------------------------------##


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dask
import dask.dataframe as dd
import numpy as np


def tadCount():
    df    =   pd.read_csv('../../../analysis/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C_closest_all.bed.gz',compression='gzip',sep='\t',header=None)
    #sns.countplot()
    #groupDf =   df.groupby([6,10]).size()
    ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000,np.inf]
    print(df[[10]].values.flatten())
    groupDf =   df.groupby(pd.cut(df[[10]].values.flatten() , bins=ranges,labels=[-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000], right=False)).count()[1]
    print(groupDf)
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.50)
    groupDf.plot.bar()
    ax.set(xlabel='distance', ylabel='# of TAD')
    ax.set_xticklabels(ax.get_xticklabels(),verticalalignment='baseline')
    ax.tick_params(axis='x', which='major', pad=130)
    plt.savefig("../../../figures/tad_count_wrt_to_distance.png")

    """ result 
    (-10000000, -1000000]    39169982
    (-1000000, -100000]       7905179
    (-100000, -10000]         1227004
    ( -10000, -1000]            163762
    (-1000, 0]                9746198
    (0, 1000]                   19194
    (1000, 10000]              156695
    (10000, 100000]           1274653
    (100000, 1000000]         7811781
    (1000000, 10000000]      38800997
    """
   
def promoterCount():
    df    =   pd.read_csv('../../../analysis/encode/Promoter_enhancer_links_ChIA-PET_closest_all.bed.gz',compression='gzip',sep='\t',header=None,error_bad_lines=False)
    #sns.countplot()
    print(df.head())
    #groupDf =   df.groupby([6,10]).size()
    ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000,np.inf]
    groupDf =   df.groupby(pd.cut(df[[19]].values.flatten(), bins=ranges,labels=[-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000], right=False)).count()[1]
    print(groupDf)
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.50)
    groupDf.plot.bar()
    ax.set(xlabel='distance', ylabel='# of Promoter and Enhancer')
    ax.set_xticklabels(ax.get_xticklabels(),verticalalignment='baseline')
    ax.tick_params(axis='x', which='major', pad=130)
    plt.savefig("../../../figures/promotre_count_wrt_to_distance.png")

    """
    (-10000000, -1000000]     3622540
    (-1000000, -100000]       3720570
    (-100000, -10000]         2014108
    (-10000, -1000]            543819
    (-1000, 0]               33327562
    (0, 1000]                   55558
    (1000, 10000]              387645
    (10000, 100000]           1802538
    (100000, 1000000]         3670489
    (1000000, 10000000]       3615733
    """

def openChromatin():
    chunksize = 10 ** 5
    ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000]
    groupDf =  pd.DataFrame({'index':ranges,1:[0,0,0,0,0,0,0,0,0,0,0]})
    for df in pd.read_csv('../../../analysis/encode/Open_chromatin_DNase_seq_closest_all.bed.gz',compression='gzip',sep='\t',header=None,error_bad_lines=False, chunksize=chunksize):
        #sns.countplot()
        sd = dd.from_pandas(df, npartitions=10)
        #sd = dd.from_pandas(df, npartitions=10)
        ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000,np.inf]
        tmp     =   sd.compute().groupby(pd.cut(df[[17]].values.flatten(), bins=ranges,labels=[-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000], right=False)).count()[1]
   
        groupDf =   pd.concat([groupDf.reset_index(), tmp.reset_index()]).groupby('index')[1].sum().reset_index()
    print(groupDf)
    groupDf = groupDf.set_index('index')
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.50)
    groupDf.plot.bar()
    ax.set(xlabel='distance', ylabel='# of OpenChromatin')
    ax.set_xticklabels(ax.get_xticklabels(),verticalalignment='baseline')
    ax.tick_params(axis='x', which='major', pad=130)
    plt.savefig("../../../figures/OpenChromatin_count_wrt_to_distance.png")
   
def histonMark():
    chunksize = 10 ** 5
    ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000]
    groupDf =  pd.DataFrame({'index':ranges,1:[0,0,0,0,0,0,0,0,0,0,0]})
    for df in pd.read_csv('../../../analysis/encode/Histone_mark_enrichment_ChIP-seq_closest_all.bed.gz',compression='gzip',sep='\t',header=None,error_bad_lines=False, chunksize=chunksize):
        #sns.countplot()
        sd = dd.from_pandas(df, npartitions=10)
        print(df.head())
        #sd = dd.from_pandas(df, npartitions=10)
        ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000,np.inf]
        tmp     =   sd.compute().groupby(pd.cut(df[[17]].values.flatten(), bins=ranges,labels=[-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000], right=False)).count()[1]
        groupDf =   pd.concat([groupDf.reset_index(), tmp.reset_index()]).groupby('index')[1].sum().reset_index()
    print(groupDf)
    groupDf = groupDf.set_index('index')
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.50)
    groupDf.plot.bar()
    ax.set(xlabel='distance', ylabel='# of Histone_mark')
    ax.set_xticklabels(ax.get_xticklabels(),verticalalignment='baseline')
    ax.tick_params(axis='x', which='major', pad=130)
    plt.savefig("../../../figures/Histone_mark_count_wrt_to_distance.png")

def example():
    dt    =   {0: 'object', 2: 'int64', 1: 'int64',3:'object',4:'int64',5:'object',6:'object',7:'object',8:'int64',9:'int64',10:'object',11:'int64',12:'object',13:'float64',14:'float64',15:'float64',16:'int64',17:'int64'}
    df    =   pd.read_csv('../../../analysis/encode/Histone_mark_enrichment_ChIP-seq_closest_all_example.bed.gz',compression='gzip',sep='\t',header=None,error_bad_lines=False)
    sd = dd.from_pandas(df, npartitions=10)
    #sns.countplot()
    print(df.head())
    ranges  =   [-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000,np.inf]
    groupDf =   sd.compute().groupby(pd.cut(df[[17]].values.flatten(), bins=ranges,labels=[-10000000,-1000000,-100000,-10000,-1000,0,1000,10000,100000,1000000,10000000], right=False)).count()[1]
    print(groupDf.reset_index())
    groupDf =   pd.concat([groupDf.reset_index(), groupDf.reset_index()]).groupby('index')[1].sum().reset_index()
    groupDf = groupDf.set_index('index')
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.50)
    groupDf.plot.bar()
    ax.set(xlabel='distance', ylabel='# of Histone_mark')
    ax.set_xticklabels(ax.get_xticklabels(),verticalalignment='baseline')
    ax.tick_params(axis='x', which='major', pad=130)
    plt.savefig("../../../figures/test.png")
    plt.show()
    

def main():
    #promoterCount()
    openChromatin()
    histonMark()
    example()
    

if __name__ == "__main__":
    main()