#!/usr/bin/env python3 
###------------------------------------------------------------------------------------------##
#
#@author narumeena
#@description core statistical course 
#source https://www.training.cam.ac.uk/booking/3371992
#
###------------------------------------------------------------------------------------------##


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro
from scipy.stats import wilcoxon


fishlengthDF=pd.read_csv('data/CS1-onesample.csv',sep='\t')
guanapo=fishlengthDF.Guanapo

print(guanapo)
print(guanapo.describe())

#box plot 
plt.boxplot(guanapo, labels=['Male Guppies'])
plt.ylabel('Length (mm)')
plt.savefig("data/cs1_boxplot.png")

#hostogram 
plt.hist(guanapo, bins=15)
plt.savefig("data/cs1_hist_plot.png")

#q-q plot 
p   =   qqplot(guanapo,line='s')
plt.savefig("data/cs1_q-q_plot.png")

#Perform a one-sample, two-tailed t-test:
print(ttest_1samp(guanapo, 20))

#Shapiro-Wilk test
print(shapiro(guanapo))


#wilcoxon test 
print(wilcoxon(guanapo-20,alternative="two-sided"))


plt.hist(guanapo, bins=15)
plt.savefig("data/cs1_hist_scond_plot.png")

plt.boxplot(guanapo)
plt.savefig("data/cs1_box_secondplot.png")