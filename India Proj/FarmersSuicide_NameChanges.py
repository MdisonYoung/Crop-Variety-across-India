# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#   Import necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import csv
import seaborn as sns

#set default DPI at 300
plt.rcParams["figure.dpi"] = 300

#open dataset
crops = pd.read_csv("CropProduction.zip")


# 28 states exist within India.
#   Check the dataset's variables

#check the variety & counts of crops in India 
# 55 crops
print(crops['Crop'].value_counts())

#check the variety of seasons
print(crops['Season'].value_counts())
#Kharif, Rabi, Whole Year, Summer, Winter, Autumn

#check the states
#INCORRECT: bunch of districts for states and unique values
print(crops['State'].value_counts())

#print state names without the duplicates
print(crops['State'].drop_duplicates())

#%%
#   Rewrite the states into a csv file to line up with state names of geo-boundaries

#create list of state names
names = [
    {'State2': 'Andaman & Nicobar Island', 'Old_Name':'Andaman and Nicobar Island', 'Value': 1},
    {'State2': 'Andhra Pradesh', 'Old_Name': 'Andhra Pradesh', 'Value': 2},
    {'State2': 'ArunÄchal Pradesh', 'Old_Name':'Arunachal Pradesh', 'Value': 3},
    {'State2': 'Assam', 'Old_Name': 'Assam', 'Value': 4},
    {'State2': 'BihÄr', 'Old_Name': 'Bihar', 'Value': 5},
    {'State2': 'ChandÄ«garh', 'Old_Name': 'CHANDIGARH', 'Value': 6},
    {'State2': 'ChhattÄ«sgarh', 'Old_Name':'Chhattisgarh', 'Value': 7},
    {'State2': 'DÄdra and Nagar Haveli and DamÄn and Diu', 'Old_Name':'Dadra and Nagar Haveli', 'Value': 8},
    {'State2': 'DÄdra and Nagar Haveli and DamÄn and Diu', 'Old_Name': 'Daman and Diu', 'Value': 9},
    {'State2': 'Goa', 'Old_Name': 'Goa', 'Value': 10},
    {'State2': 'GujarÄt', 'Old_Name':'Gujarat', 'Value': 11},
    {'State2': 'HaryÄna', 'Old_Name': 'Haryana', 'Value': 12},
    {'State2': 'HimÄchal Pradesh', 'Old_Name':'Himachal Pradesh', 'Value': 13},
    {'State2': 'Jammu and KashmÄ«r', 'Old_Name': 'Jammu and Kashmir', 'Value': 14},
    {'State2': 'JhÄrkhand', 'Old_Name': 'Jharkhand', 'Value': 15},
    {'State2': 'KarnÄtaka', 'Old_Name': 'Karnataka', 'Value': 16},
    {'State2': 'Kerala', 'Old_Name': 'Kerala', 'Value': 17},
    {'State2': 'LadÄkh', 'Old_Name': 'Laddak', 'Value': 18},
    {'State2': 'Madhya Pradesh', 'Old_Name': 'Madhya Pradesh', 'Value': 19},
    {'State2': 'MahÄrÄshtra', 'Old_Name': 'Maharashtra', 'Value': 20},
    {'State2': 'Manipur', 'Old_Name': 'Manipur', 'Value': 21},
    {'State2': 'MeghÄlaya', 'Old_Name': 'Meghalaya', 'Value': 22},
    {'State2': 'Mizoram', 'Old_Name': 'Mizoram', 'Value': 23},
    {'State2': 'NÄgÄland', 'Old_Name': 'Nagaland', 'Value': 24},
    {'State2': 'Odisha', 'Old_Name': 'Odisha', 'Value': 25},
    {'State2': 'Punjab', 'Old_Name':'Punjab', 'Value': 26},
    {'State2': 'RÄjasthÄn', 'Old_Name': 'Rajasthan', 'Value': 27},
    {'State2': 'Sikkim', 'Old_Name': 'Sikkim', 'Value': 28},
    {'State2': 'Tamil NÄdu', 'Old_Name':'Tamil Nadu', 'Value': 29},
    {'State2': 'Tamil NÄdu', 'Old_Name': 'Puducherry', 'Value': 30},
    {'State2': 'TelangÄna', 'Old_Name':'Telangana', 'Value': 31},
    {'State2': 'DÄdra and Nagar Haveli and DamÄn and Diu', 'Old_Name':'THE DADRA AND NAGAR HAVELI', 'Value': 32},
    {'State2': 'Tripura', 'Old_Name': 'Tripura', 'Value': 33},
    {'State2': 'Uttar Pradesh', 'Old_Name': 'Uttar Pradesh', 'Value': 34},
    {'State2': 'UttarÄkhand', 'Old_Name': 'Uttarakhand', 'Value': 35},
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
merged = crops.merge(new_names, left_on='State', right_on='Old_Name',how='left', indicator=True)

#check for mis-matches
print(merged['_merge'].value_counts())
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
#   perform GROUP STATISTICS over states' crop productions

#   TOP 10 Crops by AVERAGED AREA ALL ACROSS India FOR 1997 - 2020

#%%

#   ALL CROPS by AVERAGED AREA ALL ACROSS INDIA FOR 1997 - 2020
# THE HARD WAY
#group by state, crop type, value number
state_area = merged.groupby(['State2', 'Crop'])

grouped = merged.groupby(['Crop'])

#AVERAGE AREA ALL ACROSS India FOR 1997 - 2020
mean_area = state_area['Area '].sum()

raw = grouped['Area '].sum()
top_10 = raw.sort_values()[-10:]

#reset index of mean_area
mean_area = mean_area.reset_index().set_index(['Crop'])

index_top10 = mean_area.index.isin(top_10.index)
mean_area_top10 = mean_area[index_top10]


mean_area_top10 = mean_area_top10.reset_index()


grid = mean_area_top10.groupby(['State2','Crop']).sum().unstack().fillna(0)


#do i concenatate each state with the crops

#%%
#this one doesn't run
# Area is not unique, the label must be a tuple with elements corresponding to each level
grid = grid.sort_values(by='Area ', ascending=False, inplace=True)

sns.heatmap(grid,cmap='YlGnBu')


#%%
#pivot into a grid DF - THE EASY WAY

grid = mean_area_top10.pivot(index='State2', columns='Crop', values='Area ')
grid = grid.fillna(0)

sns.heatmap(grid, cmap='YlGnBu_r')

#%%
#   sort the states from north to south

# Define the desired order of states: NORTHERN STATES to SOUTHERN STATES
state_order = ['Jammu & Kashmir',
               'Himachal Pradesh',
               'Punjab',
               'Uttarakhand',
               'Haryana',
               'Uttar Pradesh',
               'Rajasthan',
               'Arunachal Pradesh',
               'Sikkim',
               'Assam',
               'West Bengal',
               'Nagaland',
               'Bihar',
               'Meghalaya',
               'Manipur',
               'Madhya Pradesh',
               'Jharkhand',
               'Tripura',
               'Mizoram',
               'Gujarat',
               'Chhattisgarh',
               'Odisha',
               'Maharashtra',
               'Daman & Diu',
               'Dadara & Nagar Havelli',
               'Telangana',
               'Andhra Pradesh',
               'Goa',
               'Karnataka',
               'Kerala',
               'Tamil Nadu',
               'Andaman & Nicobar Island'
               ]

# Convert the 'state' column to a categorical data type with the desired order
mean_area['State2'] = pd.Categorical(mean_area['State2'], categories=state_order, ordered=True)

# Sort the DataFrame by 'state' column
df = mean_area.sort_values('State2')

# Reset the index
df = mean_area.reset_index(drop=False)

#%%
# SORT North-South STATES' CROPS BY AREA for HEATMAP

#dict to specify order
state_order_d = {State2: i for i, State2 in enumerate(state_order)}

#Map the states to corresponding positions in the desired order
df['state_order'] = df['State2'].map(state_order_d)

#Sort by state_order
df = df.sort_values('state_order')

#write out df to csv
df.to_csv('output.csv',index=False)


#%%
#aggregate & sum over top 10 
statedf = df.groupby(['State2', 'Crop'])

groupdf = df.groupby(['Crop'])

#AVERAGE AREA ALL ACROSS India FOR 1997 - 2020
mean_area_df = statedf['Area '].sum()

rawdf = groupdf['Area '].sum()
top_10_df = rawdf.sort_values()[-10:]

#reset index of mean_area
mean_area_df = mean_area_df.reset_index().set_index(['Crop'])

index_top10_df = mean_area_df.index.isin(top_10_df.index)
mean_area_top10_df = mean_area_df[index_top10_df]

mean_area_top10_df = mean_area_top10_df.reset_index()

#sorting by value? want to change crop order !!
#mean_area_top10_df = mean_area_top10_df['Area '].sort_values()

#Pivot table
clean = mean_area_top10_df.dropna(subset=['State2','Crop'])
heatmap_data = clean.pivot(index='State2', columns='Crop', values='Area ')

#fill na's
heatmap_data = heatmap_data.fillna(0)

#before final heat-mapping, I need to sort by highest area crops
#tight layout / design the heatmap

fig, ax = plt.subplots(figsize=(15,15))
ax = sns.heatmap(heatmap_data, linewidths=.5, cmap='YlGnBu', annot=False)
ax.set(xlabel="Crop Type", ylabel="States from N to S")
ax.set(title="Indian States' Area of Crops from N to S")

#%%
ax.xaxis.tick_top()

#https://seaborn.pydata.org/generated/seaborn.heatmap.html ???

#%%
plt.savefig('geographicheatmap.png')


#%%

#Open Farmer Suicide Data

farmdistress = pd.read_csv("OGD_FarmerSuicides_2015.csv")

#check the states
#INCORRECT: bunch of districts for states and unique values
print("State Names in Farmer Suicide Dataset:", farmdistress['State/UT'].value_counts())

# Title case the State/UT column

mod = farmdistress.copy()
fixstates = mod['State/UT'].str.title()
mod['State/UT'] = fixstates


#rename incorrect name formats
states_corrected = [
    {"State": "Andaman and Nicobar Islands", "State/UT": "A & Nislands"},
    {"State":"ArunÄchal Pradesh", "State/UT": "Arunachal Pradesh"},
    {"State":"BihÄr", "State/UT": "Bihar"},
    {"State":"ChhattÄ«sgarh", "State/UT": "Chhattisgarh"},
    {"State":"GujarÄt", "State/UT": "Gujarat"},
    {"State":"DÄdra and Nagar Haveli and DamÄn and Diu", "State/UT":"D & N Haveli"},
    {"State":"DÄdra and Nagar Haveli and DamÄn and Diu", "State/UT":"Daman & Diu"},
    {"State":"Delhi", "State/UT":"Delhi (Ut)"},
    {"State":"HaryÄna", "State/UT": "Haryana"},
    {"State":"HimÄchal Pradesh", "State/UT": "Himachal Pradesh"},
    {"State":"Jammu and KashmÄ«r", "State/UT":"Jammu & Kashmir"},
    {"State":"JhÄrkhand", "State/UT": "Jharkhand"},
    {"State":"KarnÄtaka", "State/UT": "Karnataka"}, 
    {"State":"MahÄrÄshtra", "State/UT": "Maharashtra"}, 
    {"State":"MeghÄlaya", "State/UT": "Meghalaya"},
    {"State":"NÄgÄland", "State/UT": "Nagaland"},
    {"State":"RÄjasthÄn", "State/UT": "Rajasthan"},
    {"State":"Tamil NÄdu", "State/UT": "Tamil Nadu"},
    {"State":"TelangÄna", "State/UT": "Telangana"},
    {"State":"UttarÄkhand", "State/UT": "Uttarakhand"},
    {"State":"Tamil NÄdu", "State/UT":"Puducherry"}  
    ]

#write file name for csv
farm_file = "farmdistress_statenames.csv"

#specify column names for merged df
fieldnames1 = ["State", "State/UT"]

#open the file in write
with open (farm_file, mode="w", newline='') as file:
    #create a csv writer object
    writer = csv.DictWriter(file, fieldnames=fieldnames1)
    #write the header row
    writer.writeheader()
    #write the data to csv file
    writer.writerows(states_corrected)
    
farmnames = pd.read_csv("farmdistress_statenames.csv")

farm_merged = mod.merge(farmnames, left_on='State/UT', right_on='State/UT',how='left', indicator=True)

# remove incorrect state names & replace with names from new state column

#check for mis-matches
print(farm_merged['_merge'].value_counts())
farm_merged = farm_merged.drop(columns='_merge')

#switch over the correct state names
no_new2 = farm_merged['State'].isna()

farm_merged['State'] = farm_merged['State/UT'].where(no_new2, farm_merged['State'])
print(farm_merged['State'].value_counts())

#   drop State/UT column with incorrect names 
farm_merged.drop(['State/UT'], axis=1, inplace=True)

# drop NA's
farm_merged.dropna(subset=['State'], inplace=True)

#reset index to State column
farm_merged.reset_index(drop=True, inplace=True)

farm_merged = farm_merged.set_index('State', drop=True)

farm_merged.to_csv('farmer_suicides.csv',index=True)

