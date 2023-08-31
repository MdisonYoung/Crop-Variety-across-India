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
#   Merge tables to combine new and old state names
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


#   Remove all other seasons and only use "Whole Year" to depict yearly crop production

# use loc to select Whole Year for Season
merged = merged.loc[merged['Season']=='Whole Year ']


#%%
#   perform GROUP STATISTICS over states' crop productions

#   TOP 10 CROP TYPES by SUMMED AREA ACROSS INDIA by STATE

# group by state & crop type

#area by state & crop type
state_area = merged.groupby(['Crop', 'Crop_Year'])

#area by crop type
grouped = merged.groupby(['Crop'])

#SUM AREA ALL ACROSS India
sum_area1 = state_area['Area '].sum()

#SUM AREA by crop type
raw = grouped['Area '].sum()

#pull out 10 crops of raw with highest sums of area
top_10 = raw.sort_values()[-5:]

#reset index of sum_area1 to crop
sum_area1 = sum_area1.reset_index().set_index(['Crop'])

index_top10 = sum_area1.index.isin(top_10.index)
sum_area_top10 = sum_area1[index_top10]


sum_area_top10 = sum_area_top10.reset_index()


#%%

#   TOP 10 CROP TYPES by SUMMED YIELD ACROSS INDIA by STATE

# group by state & crop type

#yield by state & crop type
state_yield = merged.groupby(['Crop','Crop_Year'])

#yield by crop type
grouped_yield = merged.groupby(['Crop'])

#SUM YIELD ALL ACROSS India
sum_yield = state_yield['Yield'].sum()

#SUM YIELD by crop typw
raw_yield = grouped_yield['Yield'].sum()

#pull out 10 crops of raw_yield with highest sums of yield
top_10_yield = raw_yield.sort_values()[-5:]

#reset index of sum_yield to crop
sum_yield = sum_yield.reset_index().set_index(['Crop'])

index_topyield = sum_yield.index.isin(top_10_yield.index)
sum_yield_top10 = sum_yield[index_topyield]

sum_yield_top10 = sum_yield_top10.reset_index()


#%%
#  TOP 10 CROP TYPES by SUMMED AREA ACROSS INDIA by YEAR & STATE

#group by state, year, & crop
#yearattempt = merged.groupby(['State2','Crop','Crop_Year'])
#groupattempt = merged.groupby(['Crop'])

#SUM area all across India 
#sum_area_year = yearattempt['Area '].sum()

#sum_grouped = groupattempt['Area '].sum()

#pull out 10 crops with highest sums of area
#sort values says it is missing sort "by" ????
#top10year = sum_grouped.sort_values()[-5:]

#reset index of sum_area_year
#sum_area_year = sum_area_year.reset_index().set_index(['Crop'])

#HERE, THE INDEX BECAMES BOOL OF ALL FALSE?
#sum_index = sum_area_year.index.isin(top10year.index)

#sum_area_top10 = sum_area_year[sum_index]

#sum_area_top10 = sum_area_top10.reset_index()


#%%
#   Pivot the top 10 crop types by area in India (by year) into grid

#Pivot tables for both area top 10 and yield top 10

#   Crop Production by Area for the top 10 Crop Types

#drop nas - should I drop NAs or fill NAs with 0?
#pivot_sum_year = sum_area_top10.dropna(subset=['Crop','Crop_Year'])

#pivot, set columns, and value to production by area
#pivotyear = pivot_sum_year.pivot(index='Crop', columns=['Crop_Year'], values='Area ')

#grid = sum_area_top10.pivot(index='Crop_Year', columns=['Crop','Crop_Year'], values='Area ')

#fill na's
#grid = grid.fillna(0)


#   Crop Production by Yield for the top 10 Crop Types

#nas
#pivot_sum_yield = sum_yield_top10.dropna(subset=['Crop','Crop_Year'])

#pivot, set columns, and value to production by yield
#pivotyield = pivot_sum_yield.pivot(index='Crop',columns=['Crop_Year'], values='Yield')

#gridyield = sum_yield_top10.pivot(index='Crop_Year', columns=['Crop','Crop_Year'], values='Yield')

#gridyield = gridyield.fillna(0)

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

#moving sum_area
# group by state & crop type

#area by state & crop type
state_area = merged.groupby(['State2', 'Crop'])

#area by crop type
grouped = merged.groupby(['Crop'])

#SUM AREA ALL ACROSS India
sum_area = state_area['Area '].sum()

#reset index of sum_area to crop
sum_area = sum_area.reset_index().set_index(['Crop'])

#Convert state to a categorical in desired order
sum_area['State2'] = pd.Categorical(sum_area['State2'], categories=state_order, ordered=True)

#ort by state
df = sum_area.sort_values('State2')

#Reset the index
df = sum_area.reset_index(drop=False)

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
sum_area_df = statedf['Area '].sum()

rawdf = groupdf['Area '].sum()

# pull out the top 10 crops by area
top_10_df = rawdf.sort_values()[-10:]

#reset index of sum_area_df to crop
sum_area_df = sum_area_df.reset_index().set_index(['Crop'])

index_top10_df = sum_area_df.index.isin(top_10_df.index)
sum_area_top10_df = sum_area_df[index_top10_df]

sum_area_top10_df = sum_area_top10_df.reset_index()

#How can I sort by value (area) of the heatmap?
#sum_area_top10_df = sum_area_top10_df['Area '].sort_values()

#   Pivot table

#drop nas
clean = sum_area_top10_df.dropna(subset=['State2','Crop'])

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

#   Aggregate & sum area of over lowest 10 crop types 

#groupby state & crop type
statedf2 = df.groupby(['State2', 'Crop'])

groupdf2 = df.groupby(['Crop'])

#SUM AREA across India over all years
sum_area_df2 = statedf2['Area '].sum()

rawdf2 = groupdf2['Area '].sum()

# pull out the top 10 crops by area
top_10_df2 = rawdf2.sort_values()[:10]

#reset index of sum_area_df to crop
sum_area_df2 = sum_area_df2.reset_index().set_index(['Crop'])

index_top10_df2 = sum_area_df2.index.isin(top_10_df2.index)
sum_area_top10_df2 = sum_area_df2[index_top10_df2]

sum_area_top10_df2 = sum_area_top10_df2.reset_index()

#How can I sort by value (area) of the heatmap?
#sum_area_top10_df = sum_area_top10_df['Area '].sort_values()

#   Pivot table

#drop nas
clean2 = sum_area_top10_df2.dropna(subset=['State2','Crop'])

#pivot, set columns, and value to area
heatmap_data2 = clean2.pivot(index='Crop', columns='State2', values='Area ')

#fill na's with 0
heatmap_data2 = heatmap_data2.fillna(0)

#   Plotting a heatmap

#figure, set size
fig2, ax2 = plt.subplots(figsize=(18,15))

#set ax to heatmap, set width of lines, color to cmap, shape to square, reduce cbar size, and emphasize differences with robust
ax2 = sns.heatmap(heatmap_data2, linewidths=.5, cmap='YlGnBu', annot=False, square=True,cbar_kws={"shrink": 0.35},robust=True)

#rotate state names on x axis
ax2.tick_params(axis='x', labelrotation = 75)

#set labels & title
ax2.set_ylabel("Crop Type",weight='bold',size=11.5)
ax2.set_xlabel("States (North to South)",weight='bold', size=11.5)
ax2.set_title("Production of Local Crops by Area in India", weight='bold', size=17)

#save to jpg
plt.savefig("India's Crop Production of Local Crops.jpg")


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
#maybe merge on one where districts is already dropped
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


#   Scatter - Plot the Top 10 Crop Types by YIELD over time (1998 - 2007)

#x-axis will be year, y-axis is Yield, colors of points are crop types


#must set crops to a numerical form for crop type by yield - found at https://www.geeksforgeeks.org/how-to-convert-categorical-variable-to-numeric-in-pandas/
sum_yield_top10['Crop'].replace(['Banana', 'Coconut ', 'Sugarcane','Onion', 'Potato'],
                        [0, 1, 2, 3, 4], inplace=True)


#plot figure
fig1,ax = plt.subplots(figsize=(10,10))
#choose colors
sum_yield_top10.plot.scatter(ax=ax, x='Crop_Year',y='Yield',c='Crop', cmap='magma')

# Add titles (main and on axis)
plt.xlabel("Years (1998-2017)")
plt.ylabel("Yield of Crops")
plt.title("Change in Crop Yield for India's Top 10 Crops")

# Show the graph
plt.show()


#   Scatter - Plot the Top 10 Crop Types by AREA over time (1998 - 2007)

#x-axis will be year, y-axis is Area, colors of points are crop types


#set crops to a numerical form for crop type by area
sum_area_top10['Crop'].replace(['Guar seed', 'Sugarcane', 'Coconut ', 'Potato', 'Coriander'],
                        [0, 1, 2, 3, 4], inplace=True)


#plot figure
fig2,ax2 = plt.subplots(figsize=(10,10))

#choose colors
sum_area_top10.plot.scatter(ax=ax2, x='Crop_Year',y='Area ',c='Crop', cmap='magma')

# Add titles (main and on axis)
plt.xlabel("Years (1998-2017)")
plt.ylabel("Area of Crops")
plt.title("Change in Crop Area for India's Top 10 Crops")

# Show the graph
plt.show()



#%%

#   Change date to year to plot the x-axis correctly, but with colored categories of crops

#convert a string to a Pandas datetime object and get the year
yeardate = pd.to_datetime(sum_yield_top10['Crop_Year'], format = "%Y")
sum_yield_top10['ymd'] = yeardate
sum_yield_top10['year'] = yeardate.dt.year
sum_yield_top10 = sum_yield_top10.drop(columns="ymd")

#choose colors
REGION_COLS = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2"]

#set df variable for x
YEAR = sum_yield_top10["year"].values

#set df variable for y
AREA = sum_yield_top10["Yield"].values

#set df variable for color
CROP = sum_yield_top10["Crop"].values
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

#this map shows varying colors of points and years are fixed, but only shows 5 points

#%%

#import packages
from matplotlib.lines import Line2D 

#figure
fig, ax = plt.subplots(figsize=(6, 6))

#set colors to top 5 cash crops : "Maize", "Rapeseed &Mustard", "Rice", "Soyabean", "Wheat"
colors = {0:'tab:blue', 1:'tab:orange', 2:'tab:green', 3:'tab:red', 4:'tab:purple'}

#scatter
ax.scatter(sum_yield_top10['Crop_Year'], sum_yield_top10['Yield'], c=sum_yield_top10['Crop'].map(colors))

# add a legend
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=3) for k, v in colors.items()]
ax.legend(title='color', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()

sns.lmplot(x='year', y='Yield', data=sum_yield_top10, hue=colors, fit_reg=False)




#dissimilarity indexes
# x will be time
# y will be the area or yield of crops
# color can be the types of crops
# then compare the amount of area / yield for top 10 or 5 crops and the top 10 or 5 indigenous crops ...
# in years of 2005-2010, then 2010-2015?




