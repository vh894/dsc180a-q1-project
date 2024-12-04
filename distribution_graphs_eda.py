# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import geopandas as gpd

# %%
dtype_dict = {'_id': 'str', 'Date': 'str', 'Zip Code': 'str', 'Model Year': 'str', 'Fuel': 'str', 'Make': 'str', 'Duty': 'str', 'Vehicles': 'float64'}

#Reading in the CSV files for every year
df_2019 = pd.read_csv('distribution_graph_data/2019_data.csv', dtype = dtype_dict)
df_2020 = pd.read_csv('distribution_graph_data/2020_data.csv', dtype = dtype_dict)
df_2021 = pd.read_csv('distribution_graph_data/2021_data.csv', dtype = dtype_dict)
df_2022 = pd.read_csv('distribution_graph_data/2022_data.csv', dtype = dtype_dict)
df_2023 = pd.read_csv('distribution_graph_data/2023_data.csv', dtype = dtype_dict)
df_2024 = pd.read_csv('distribution_graph_data/2024_data.csv', dtype = dtype_dict)

#Changing the name of the column to match the labeling of the column from the other years
df_2024.rename(columns={'ZIP Code': 'Zip Code'}, inplace = True)

#Merging all 6 dataframes
df = pd.concat([df_2019, df_2020, df_2021, df_2022, df_2023, df_2024])

#Changing the Date column to be a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# %%
df

# %%
# Plotting the distribution of electric vehicle registrations over time
ev_only_df = df[df['Fuel'] == 'Battery Electric']
ev_only_df_year = ev_only_df[['Year', 'Vehicles']].groupby('Year').sum()
ev_only_df_year.plot(kind='bar', title = 'Electric Vehicle Registrations Over Time', xlabel = 'Year', ylabel = 'Count');

# %%
#Plotting the distribution of vehicles based on their fuel type of registration year
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='Year', weights='Vehicles', hue='Fuel', fill=True, common_norm=False)
plt.title('Density Plot of Vehicle Counts by Registration Year and Fuel Type')
plt.xlabel('Year')
plt.ylabel('Density')
fuel_types = df['Fuel'].unique()
handles = [mlines.Line2D([0], [0], color=sns.color_palette()[i], lw=3) for i in range(len(fuel_types))]
labels = [str(fuel) for fuel in fuel_types]
plt.legend(handles=handles, labels=labels, title='Fuel Type', loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

# %%
# Making a dataframe that shows the percentage of EVs in relation to other fuel types for every zip code
not_ev_df = df[df['Fuel'] != 'Battery Electric']
not_ev_df = not_ev_df[['Zip Code', 'Vehicles']].groupby('Zip Code').sum()
grouped_ev = ev_only_df[['Zip Code', 'Vehicles']]
grouped_ev = grouped_ev.groupby('Zip Code').sum()
merged_ev = grouped_ev.merge(not_ev_df, on = 'Zip Code')
merged_ev['Percentage'] = (merged_ev['Vehicles_x'] / merged_ev['Vehicles_y']) * 100

# SD boundaries
geo_df5 = gpd.read_file('data/zip_codes.geojson')
geo_df5['name'] = geo_df5['community']
geo_df5['Zip Code'] = geo_df5['zip']
geo_df5 = geo_df5[['name', 'geometry', 'Zip Code']]

# Merging the CV values with the SD boundaries
merged_df = geo_df5.merge(merged_ev, how='left', on='Zip Code')
merged_df['name'] = merged_df['name'].astype(str)
merged_df

# %%
# Plotting the choropleth map that shows the percentage of EVs in relation to other fuel types for every zip code 
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot the choropleth map
merged_df.boundary.plot(ax=ax, linewidth=1, color='black') 
merged_df.plot(column='Percentage', ax=ax, legend=True,
         cmap='Blues',  # Choose a colormap
         missing_kwds={'color': 'lightgrey', 'label': 'Missing values'}) 

# Customize the plot
plt.title('Percentage of EVs For Every San Diego City')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('off')  

#Putting labels for every city
for x, y, label in zip(merged_df.geometry.centroid.x, merged_df.geometry.centroid.y, merged_df['name']):
    ax.annotate(label, xy=(x, y), horizontalalignment='center', fontsize=5, color='black')

# Show the plot
plt.show()

# %%
#Converting the CSV files into dataframes
col_index = [i for i in range(29)] + [i for i in range(41, 50)] + [70, 71, 72]
chargers = pd.read_csv('ev_data.csv', usecols=[i for i in col_index], dtype={'zip': str, 'ev_network_web': str, 'ev_renewable_source': str, 'ev_other_evse': str, 'ev_workplace_charging': str}) 
sdge_areas = pd.read_csv('data/SDGE_service_list.csv', usecols=['ZipCode'])

#Getting the zip codes for all the areas at SDGE serves
sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]

#Querying the data to only include chargers within the areas that SDGE serves
chargers = chargers[chargers['zip'].isin(sdge_zip_codes)]
chargers

# %%
#Plot of distribution of fuel type from all 2018 to 2023
grouped_df = df.groupby('Fuel').count()
grouped_df.rename(columns={'_id': 'Count'}, inplace = True)
grouped_df = grouped_df[['Count']]

ax = grouped_df.plot.pie(y='Count')
plt.legend(bbox_to_anchor=(1.5, 1), loc='upper left');
plt.title('Distribution of Fuel Type');

# %%
#Getting the zip codes in SDGE service areas

#Converting the CSV files into dataframes
col_index = [i for i in range(29)] + [i for i in range(41, 50)] + [70, 71, 72]
sdge_areas = pd.read_csv('data/SDGE_service_list.csv', usecols=['ZipCode'])

sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]
sdge_zip_codes

# %%
#Trying to see what the average EV registration rate is across all SDGE areas
sdge_df = df[df['Zip Code'].isin(sdge_zip_codes)]
ev_sdge = sdge_df[sdge_df['Fuel'] == 'Battery Electric']
grouped_ev_sdge = ev_sdge[['Zip Code', 'Vehicles']]
grouped_ev_sdge = grouped_ev_sdge.groupby('Zip Code').sum()
grouped_ev_sdge['Vehicles'].hist()
plt.title('Distribution of Total EV Registrations Across SDG&E Zip Codes from 2018 to 2024')
plt.xlabel('Number of EV Registrations')
plt.ylabel('Frequency')
plt.show()

# %%
grouped_ev_sdge.sort_values(by='Vehicles')

#San Diego, which has the zip code 92130, has the highest number of EV registrations.

# %%
#Plot to see the distribution of vehicles based on their registration year and their fuel type. This plot only displays cars within SDGE areas.
plt.figure(figsize=(10, 6))
sns.kdeplot(data=sdge_df, x='Year', weights='Vehicles', hue='Fuel', fill=True, common_norm=False)
plt.title('Distribution of Vehicles by Registration Year and Fuel Type for SDG&E Service Areas')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()

# %%
#Plot to see the distribution of EV models across SDGE areas
plt.figure(figsize=(10, 6))
sns.kdeplot(data=ev_sdge, x='Year', weights='Vehicles', hue='Make', fill=True, common_norm=False)
plt.title('Density Plot of Vehicle Counts by Registration Year and EV Makes for SDG&E Service Areas')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()

# %%
#Making a new column that displays whether the EV is from Tesla 
make_df = ev_sdge[['Make', 'Vehicles', 'Year']]
make_df['is_tesla'] = np.where(make_df['Make'] == 'TESLA', 'Yes', 'No')

#Plot to show how many Tesla vehicles are being registered compared to other EV models
plt.figure(figsize=(10, 6))
sns.kdeplot(data=make_df, x='Year', weights='Vehicles', hue='is_tesla', fill=True, common_norm=False)
plt.title('Density Plot of Tesla Vehicles in SDG&E Service Areas By Registration Year')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()


