# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:13:54 2023

@author: myoun
"""


#   File for India's top 10 crop production by area summed over 1997-2020



#   Import necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import csv
import seaborn as sns

#set default DPI at 300
plt.rcParams["figure.dpi"] = 300

#open dataset
crops = pd.read_csv("CropProduction.zip")