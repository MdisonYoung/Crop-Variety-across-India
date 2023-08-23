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
    {'State2': 'Andaman and Nicobar Islands', 'ISO':'IN-AN','Old_Name':'Andaman and Nicobar Island', 'Value': 1},
    {'State2': 'Andhra Pradesh', 'ISO':'IN-AP' , 'Old_Name': 'Andhra Pradesh', 'Value': 2},
    {'State2': 'Arunachal Pradesh','ISO':'IN-AR' , 'Old_Name':'Arunachal Pradesh', 'Value': 3},
    {'State2': 'Assam', 'ISO':'IN-AS' ,'Old_Name': 'Assam', 'Value': 4},
    {'State2': 'Bihar', 'ISO':'IN-BR' ,'Old_Name': 'Bihar', 'Value': 5},
    {'State2': 'Chandigarh', 'ISO':'IN-CH' ,'Old_Name': 'CHANDIGARH', 'Value': 6},
    {'State2': 'Chhattisgarh','ISO':'IN-CT' , 'Old_Name':'Chhattisgarh', 'Value': 7},
    {'State2': 'Dadara and Nagar Haveli', 'ISO':'IN-DH' ,'Old_Name':'Dadra and Nagar Haveli', 'Value': 8},
    {'State2': 'Daman and Diu', 'ISO':'' ,'Old_Name': 'Daman and Diu', 'Value': 9},
    {'State2': 'Goa','ISO':'IN-GA' , 'Old_Name': 'Goa', 'Value': 10},
    {'State2': 'Gujarat', 'ISO':'IN-GJ' , 'Old_Name':'Gujarat', 'Value': 11},
    {'State2': 'Haryana', 'ISO':'IN-HR' ,'Old_Name': 'Haryana', 'Value': 12},
    {'State2': 'Himachal Pradesh', 'ISO':'IN-HP' ,'Old_Name':'Himachal Pradesh', 'Value': 13},
    {'State2': 'Jammu and Kashmir', 'ISO':'IN-JK' , 'Old_Name': 'Jammu and Kashmir', 'Value': 14},
    {'State2': 'Jharkhand', 'ISO':'IN-JH' , 'Old_Name': 'Jharkhand', 'Value': 15},
    {'State2': 'Karnataka', 'ISO':'IN-KA' , 'Old_Name': 'Karnataka', 'Value': 16},
    {'State2': 'Kerala', 'ISO':'IN-KL' ,'Old_Name': 'Kerala', 'Value': 17},
    {'State2': 'Laddakh','ISO':'IN-JK' , 'Old_Name': 'Laddak', 'Value': 18},
    {'State2': 'Madhya Pradesh', 'ISO':'IN-MP' ,'Old_Name': 'Madhya Pradesh', 'Value': 19},
    {'State2': 'Maharashtra','ISO':'IN-MH' , 'Old_Name': 'Maharashtra', 'Value': 20},
    {'State2': 'Manipur', 'ISO':'IN-MN' ,'Old_Name': 'Manipur', 'Value': 21},
    {'State2': 'Meghalaya','ISO':'IN-ML' , 'Old_Name': 'Meghalaya', 'Value': 22},
    {'State2': 'Mizoram','ISO':'IN-MZ' , 'Old_Name': 'Mizoram', 'Value': 23},
    {'State2': 'Nagaland', 'ISO':'IN-NL' ,'Old_Name': 'Nagaland', 'Value': 24},
    {'State2': 'Odisha','ISO':'IN-OR' , 'Old_Name': 'Odisha', 'Value': 25},
    {'State2': 'Punjab','ISO':'IN-PB' , 'Old_Name':'Punjab', 'Value': 26},
    {'State2': 'Rajasthan', 'ISO':'IN-RJ' ,'Old_Name': 'Rajasthan', 'Value': 27},
    {'State2': 'Sikkim','ISO':'IN-SK' , 'Old_Name': 'Sikkim', 'Value': 28},
    {'State2': 'Tamil Nadu', 'ISO':'IN-TN' ,'Old_Name':'Tamil Nadu', 'Value': 29},
    {'State2': 'Tamil Nadu','ISO':'IN-PY' , 'Old_Name': 'Puducherry', 'Value': 30},
    {'State2': 'Telangana', 'ISO':'IN-TG' ,'Old_Name':'Telangana', 'Value': 31},
    {'State2': 'Dadara and Nagar Havelli', 'ISO':'IN-DH' ,'Old_Name':'THE DADRA AND NAGAR HAVELI', 'Value': 32},
    {'State2': 'Tripura','ISO':'IN-TR' , 'Old_Name': 'Tripura', 'Value': 33},
    {'State2': 'Uttar Pradesh', 'ISO':'IN-UP' , 'Old_Name': 'Uttar Pradesh', 'Value': 34},
    {'State2': 'Uttarakhand', 'ISO':'IN-UT' , 'Old_Name': 'Uttarakhand', 'Value': 35},
    {'State2': 'West Bengal', 'ISO':'IN-WB' , 'Old_Name': 'West Bengal', 'Value': 36}
    ]

#write file name for csv
filename = "india_state_names.csv"

#specify column names
fieldnames = ["State2","ISO", "Old_Name", "Value"]

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
#merge tables to combine new and old state names
merged = crops.merge(new_names, left_on='State', right_on='Old_Name',how='left', indicator=True)

#check for mis-matches
print(merged['_merge'].value_counts())
merged = merged.drop(columns='_merge')

#switch over the correct state names
no_new = merged['State2'].isna()

merged['State2'] = merged['State'].where(no_new, merged['State2'])
print(merged['State2'].value_counts())

#check for state na's
nas = merged['State2'].isna().sum()

#   drop 'State' and 'Old_Name'
merged.drop(['State', 'Old_Name'], axis=1, inplace=True)

# drop NA's
merged.dropna(subset=['State2'], inplace=True)

#reset index to "State2"
merged.reset_index(drop=True, inplace=True)

merged = merged.set_index('State2', drop=True)


#%%
#   perform GROUP STATISTICS over states' crop productions

#   TOP 10 CROP TYPES by SUMMED AREA ACROSS INDIA by STATE

# group by state & crop type

#area by state & crop type
state_area = merged.groupby(['State2', 'Crop'])

#area by crop type
grouped = merged.groupby(['Crop'])

#SUM AREA ALL ACROSS India
mean_area = state_area['Area '].sum()

#SUM AREA by crop type
raw = grouped['Area '].sum()

#pull out 10 crops of raw with highest sums of area
top_10 = raw.sort_values()[-10:]

#reset index of mean_area to crop
mean_area = mean_area.reset_index().set_index(['Crop'])

index_top10 = mean_area.index.isin(top_10.index)
mean_area_top10 = mean_area[index_top10]


mean_area_top10 = mean_area_top10.reset_index()

#%%
#  TOP 10 CROP TYPES by SUMMED AREA ACROSS INDIA by YEAR & STATE

#group by state, year, & crop
yearattempt = merged.groupby(['State2','Crop', 'Crop_Year'])
groupattempt = merged.groupby(['Crop'])

#SUM area all across India 
sum_area_year = yearattempt['Area '].sum()

sum_grouped = groupattempt['Area '].sum()

#pull out 10 crops with highest sums of area
#sort values says it is missing sort "by" ????
top10year = sum_area_year.sort_values()[-10:]

#reset index of sum_area_year
sum_area_year = sum_area_year.reset_index().set_index(['Crop'])

#HERE, THE INDEX BECAMES BOOL OF ALL FALSE?
sum_index = sum_area_year.index.isin(top10year.index)

sum_area_top10 = sum_area_year[sum_index]

sum_area_top10 = sum_area_top10.reset_index()


#%%
#   Pivot the top 10 crop types by area in India (by year) into grid

#Pivot table

#drop nas - should I drop NAs or fill NAs with 0?
pivot_sum_year = sum_area_top10.dropna(subset=['State2','Crop','Crop_Year'])

#pivot, set columns, and value to production by area
pivotyear = pivot_sum_year.pivot(index='Crop', columns=['State2', 'Crop_Year'], values='Area ')

grid = sum_area_top10.pivot(index='State2', columns=['Crop','Crop_Year'], values='Area ')

#fill na's
grid = grid.fillna(0)



#%%
#   sort the states in order by geography

#Desired order of states: NORTHERN STATES to SOUTHERN STATES

state_order = ['Laddakh',
               'Jammu and Kashmir',
               'Himachal Pradesh',
               'Punjab',
               'Uttarakhand',
               'Chandigarh',
               'Haryana',
               'Delhi',
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
               'Daman and Diu',
               'Dadara and Nagar Haveli',
               'Telangana',
               'Andhra Pradesh',
               'Goa',
               'Karnataka',
               'Kerala',
               'Tamil Nadu',
               'Andaman and Nicobar Islands'
               ]

#Convert state to a categorical in desired order
mean_area['State2'] = pd.Categorical(mean_area['State2'], categories=state_order, ordered=True)

#ort by state
df = mean_area.sort_values('State2')

#Reset the index
df = mean_area.reset_index(drop=False)

#dict specifying order
state_order_d = {State2: i for i, State2 in enumerate(state_order)}

#Map the states to positions in the desired order
df['state_order'] = df['State2'].map(state_order_d)

#Sort by N-to-S order
df = df.sort_values('state_order')

#write out df to csv
df.to_csv('output.csv',index=False)


#%%
#   Aggregate & sum area of over top 10 crop types 

#groupby state & crop type
statedf = df.groupby(['State2', 'Crop'])

groupdf = df.groupby(['Crop'])

#SUM AREA across India over all years
mean_area_df = statedf['Area '].sum()

rawdf = groupdf['Area '].sum()
top_10_df = rawdf.sort_values()[-10:]

#reset index of mean_area to crop
mean_area_df = mean_area_df.reset_index().set_index(['Crop'])

index_top10_df = mean_area_df.index.isin(top_10_df.index)
mean_area_top10_df = mean_area_df[index_top10_df]

mean_area_top10_df = mean_area_top10_df.reset_index()

#How can I sort by value (area) of the heatmap?
#mean_area_top10_df = mean_area_top10_df['Area '].sort_values()

#   Pivot table

#drop nas
clean = mean_area_top10_df.dropna(subset=['State2','Crop'])

#pivot, set columns, and value to area
heatmap_data = clean.pivot(index='Crop', columns='State2', values='Area ')

#fill na's with 0
heatmap_data = heatmap_data.fillna(0)

#   Plotting a heatmap

#figure, set size
fig, ax = plt.subplots(figsize=(18,15))

#set ax to heatmap, set width of lines, color to cmap, shape to square, reduce cbar size, and emphasize differences with robust
ax = sns.heatmap(heatmap_data, linewidths=.5, cmap='YlGnBu', annot=False, square=True,cbar_kws={"shrink": 0.35},robust=True)

#rotate state names on x axis
ax.tick_params(axis='x', labelrotation = 75)

#set labels & title
ax.set_ylabel("Crop Type",weight='bold',size=11.5)
ax.set_xlabel("States (North to South)",weight='bold', size=11.5)
ax.set_title("Production of Cash Crops by Area in India", weight='bold', size=17)

#save to jpg
plt.savefig("India's Crop Production of Cash Crops.jpg")

#https://seaborn.pydata.org/generated/seaborn.heatmap.html 

#%%

#   Open Farmer Suicide Data 

#used for creating GIS chloropleth of farmer suicides in India in 2015

farmdistress = pd.read_csv("OGD_FarmerSuicides_2015.csv")

#check the states
print("State Names in Farmer Suicide Dataset:", farmdistress['State/UT'].value_counts())

#title case the State/UT column
mod = farmdistress.copy()
fixstates = mod['State/UT'].str.title()
mod['State/UT'] = fixstates


#rename incorrect state name formats
states_corrected = [
    {"State": "Andaman and Nicobar Islands", "State/UT": "A & Nislands"},
    {"State":"Dadara and Nagar Haveli", "State/UT": "D & N Haveli"},
    {"State":"Daman and Diu", "State/UT":"Daman & Diu"},
    {"State":"Delhi", "State/UT":"Delhi (Ut)"},
    {"State":"Jammu and Kashmir", "State/UT": "Jammu & Kashmir"},
    {"State":"Tamil Nadu", "State/UT":"Puducherry"}  
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
    
#read farm names csv
farmnames = pd.read_csv("farmdistress_statenames.csv")

#merge farm names onto mod
farm_merged = mod.merge(farmnames, left_on='State/UT', right_on='State/UT',how='left', indicator=True)

#   Remove incorrect state names & replace with names from new state column

#check for mis-matches
print(farm_merged['_merge'].value_counts())
farm_merged = farm_merged.drop(columns='_merge')

#switch over the correct state names

#check for na's
no_new2 = farm_merged['State'].isna()

farm_merged['State'] = farm_merged['State/UT'].where(no_new2, farm_merged['State'])
print(farm_merged['State'].value_counts())

#drop State/UT column with incorrect names 
farm_merged.drop(['State/UT'], axis=1, inplace=True)

# drop NA's
farm_merged.dropna(subset=['State'], inplace=True)

#merge dataset of farmer suicides 1 onto dataset of crops?
farm_merged_2 = farm_merged.merge(merged, left_on='State', right_on='State2',how='outer', indicator=True)


#%%
#remove unnecessary columns

selected_columns = ["State", "ISO", "Total Farmers"]

farm_merged_final = farm_merged_2[selected_columns]

#reset index to State column

farm_merged_final.reset_index(drop=True, inplace=True)

farm_merged_final = farm_merged_final.set_index('State', drop=True)

#drop duplicates
farm_merged_final = farm_merged_final.drop_duplicates()

#save to csv
farm_merged_final.to_csv('farmer_suicides.csv',index=True)


#add Ladakh row?


#%%
#Scatterplot thyyyymme

#import packages
import numpy as np


#   Scatter - Plot the Top 10 Crop Types by Area over time (1998 - 2007)

#x-axis will be year, y-axis is area, colors of points are crop types


#set x, y, color, linewidth
plt.scatter(x="Crop_Year", y="Area ", c='Black', s=100, cmap="Blues", alpha=0.4, edgecolors="grey", linewidth=2)


fig1,ax = plt.subplots()
sum_area_top10.plot.scatter(ax=ax, x='Crop_Year',y='Area ',c='Black', cmap='magma')

# Add titles (main and on axis)
plt.xlabel("Years (1998-2017)")
plt.ylabel("Area of Crops")
plt.title("Change in Crop Area for India's Top 10 Crops")

# Show the graph
plt.show()

#In this scatter-plot, I cannot choose the c (color) to be multi-colored, but the years are plotted correctly on the x.


#%%

#   Change date to year to plot the x-axis correctly, but with colored categories of crops

#convert a string to a Pandas datetime object and get the year
yeardate = pd.to_datetime(sum_area_top10['Crop_Year'], format = "%Y")
sum_area_top10['ymd'] = yeardate
sum_area_top10['year'] = yeardate.dt.year
sum_area_top10 = sum_area_top10.drop(columns="ymd")

#choose colors
REGION_COLS = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2"]

#set df variable for x
YEAR = sum_area_top10["year"].values

#set df variable for y
AREA = sum_area_top10["Area "].values

#set df variable for color
CROP = sum_area_top10["Crop"].values
CROP = np.unique(CROP)

#figure
#set the size
fig, ax = plt.subplots(figsize=(8,8))
for crops, color in zip(CROP, REGION_COLS):
    idxs = np.where(CROP == crops)
    # No legend will be generated if we don't pass label=species
    ax.scatter(
        YEAR[idxs], AREA[idxs], label=crops,
        s=50, color=color, alpha=0.7
    )
    
ax.legend();

#this map shows varying colors of points but the year is being mapped as an integer, not a date?

#%%

#import packages
from matplotlib.lines import Line2D 

#figure
fig, ax = plt.subplots(figsize=(6, 6))

#set colors to top 5 cash crops : "Maize", "Rapeseed &Mustard", "Rice", "Soyabean", "Wheat"
colors = {'Maize':'tab:blue', 'Rapeseed &Mustard':'tab:orange', 'Rice':'tab:green', 'Soyabean':'tab:red', 'Wheat':'tab:purple'}

#scatter
ax.scatter(sum_area_top10['Crop_Year'], sum_area_top10['Area '], c=sum_area_top10['Crop'].map(colors))

# add a legend
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=3) for k, v in colors.items()]
ax.legend(title='color', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()

sns.lmplot(x='Crop_Year', y='Area ', data=sum_area_top10, hue='colors', fit_reg=False)




#dissimilarity indexes
# x will be time
# y will be the area of crops?
# color can be the types of crops
# then compare the amount of area for top 10 crops and the top 10 indigenous crops ...
# in years of 2005-2010, then 2010-2015?








