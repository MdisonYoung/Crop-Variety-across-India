# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:06:17 2023

@author: myoun
"""


#   File for every states' crop production by area in year 2015



#   Import necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import csv
import seaborn as sns

#set default DPI at 300
plt.rcParams["figure.dpi"] = 300

#open dataset
crops = pd.read_csv("CropProduction.zip")


#%%
#   Rewrite the states into a csv file to line up with state names of geo-boundaries

#create list of state names
names = [
    {'State2': 'Andaman & Nicobar Island', 'Old_Name':'Andaman and Nicobar Island', 'Value': 1},
    {'State2': 'Andhra Pradesh', 'Old_Name': 'Andhra Pradesh', 'Value': 2},
    {'State2': 'Arunachal Pradesh', 'Old_Name':'Arunachal Pradesh', 'Value': 3},
    {'State2': 'Assam', 'Old_Name': 'Assam', 'Value': 4},
    {'State2': 'Bihar', 'Old_Name': 'Bihar', 'Value': 5},
    {'State2': 'Chandigarh', 'Old_Name': 'CHANDIGARH', 'Value': 6},
    {'State2': 'Chhattisgarh', 'Old_Name':'Chhattisgarh', 'Value': 7},
    {'State2': 'Dadara & Nagar Havelli', 'Old_Name':'Dadra and Nagar Haveli', 'Value': 8},
    {'State2': 'Daman & Diu', 'Old_Name': 'Daman and Diu', 'Value': 9},
    {'State2': 'Goa', 'Old_Name': 'Goa', 'Value': 10},
    {'State2': 'Gujarat', 'Old_Name':'Gujarat', 'Value': 11},
    {'State2': 'Haryana', 'Old_Name': 'Haryana', 'Value': 12},
    {'State2': 'Himachal Pradesh', 'Old_Name':'Himachal Pradesh', 'Value': 13},
    {'State2': 'Jammu & Kashmir', 'Old_Name': 'Jammu and Kashmir', 'Value': 14},
    {'State2': 'Jharkhand', 'Old_Name': 'Jharkhand', 'Value': 15},
    {'State2': 'Karnataka', 'Old_Name': 'Karnataka', 'Value': 16},
    {'State2': 'Kerala', 'Old_Name': 'Kerala', 'Value': 17},
    {'State2': 'Jammu & Kashmir', 'Old_Name': 'Laddak', 'Value': 18},
    {'State2': 'Madhya Pradesh', 'Old_Name': 'Madhya Pradesh', 'Value': 19},
    {'State2': 'Maharashtra', 'Old_Name': 'Maharashtra', 'Value': 20},
    {'State2': 'Manipur', 'Old_Name': 'Manipur', 'Value': 21},
    {'State2': 'Meghalaya', 'Old_Name': 'Meghalaya', 'Value': 22},
    {'State2': 'Mizoram', 'Old_Name': 'Mizoram', 'Value': 23},
    {'State2': 'Nagaland', 'Old_Name': 'Nagaland', 'Value': 24},
    {'State2': 'Odisha', 'Old_Name': 'Odisha', 'Value': 25},
    {'State2': 'Punjab', 'Old_Name':'Punjab', 'Value': 26},
    {'State2': 'Rajasthan', 'Old_Name': 'Rajasthan', 'Value': 27},
    {'State2': 'Sikkim', 'Old_Name': 'Sikkim', 'Value': 28},
    {'State2': 'Tamil Nadu', 'Old_Name':'Tamil Nadu', 'Value': 29},
    {'State2': 'Tamil Nadu', 'Old_Name': 'Puducherry', 'Value': 30},
    {'State2': 'Telangana', 'Old_Name':'Telangana', 'Value': 31},
    {'State2': 'Dadara & Nagar Havelli', 'Old_Name':'THE DADRA AND NAGAR HAVELI', 'Value': 32},
    {'State2': 'Tripura', 'Old_Name': 'Tripura', 'Value': 33},
    {'State2': 'Uttar Pradesh', 'Old_Name': 'Uttar Pradesh', 'Value': 34},
    {'State2': 'Uttarakhand', 'Old_Name': 'Uttarakhand', 'Value': 35},
    {'State2': 'West Bengal', 'Old_Name': 'West Bengal', 'Value': 36}
    ]

#write file name for csv
filename = "india_state_names.csv"

#specify column names
fieldnames = ["State2", "Old_Name", "Value"]

#open the file in write
with open (filename, mode="w", newline='') as file:
    #create a csv writer object
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    #write the header row
    writer.writeheader()
    #write the data to csv file
    writer.writerows(names)
    
new_names = pd.read_csv("india_state_names.csv")


#%%

#merge the crops df with the new_names
merged = crops.merge(new_names, left_on='State', right_on='Old_Name',how='left', indicator=True)

#check for mis-matches
print(merged['_merge'].value_counts())

#drop the unnecessary _merge column
merged = merged.drop(columns='_merge')

#switch over the correct state names
no_new = merged['State2'].isna()

merged['State2'] = merged['State'].where(no_new, merged['State2'])
print(merged['State2'].value_counts())

#%%

#check for state na's
nas = merged['State2'].isna().sum()

#   drop 'State' and 'Old_Name'
merged.drop(['State', 'Old_Name'], axis=1, inplace=True)

# drop NA's
merged.dropna(subset=['State2'], inplace=True)

#reset index
merged.reset_index(drop=True, inplace=True)

merged = merged.set_index('State2', drop=True)

#%%
#   Summary Statistics Time

#   ALL CROPS by AVERAGED AREA ALL ACROSS INDIA FOR 2015

state_area = merged.groupby(['State2', 'Crop', 'Value'])

# !!! do not do AVERAGE AREA ALL ACROSS India FOR 1997 - 2020
#mean_area = state_area['Area '].mean()

#reset index of mean_area
#mean_area = mean_area.reset_index()

#solve duplicate issue
#print(mean_area.duplicated(subset=['State2', 'Crop']))

#drop duplicates
#mean_area = mean_area.drop_duplicates(subset=['State2', 'Crop'])

#pivot into a grid DF
#grid = mean_area.pivot(index='State2', columns='Crop', values='Area ')
#grid = grid.fillna(0)


#%%



