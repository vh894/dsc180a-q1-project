import cenpy as cp
from cenpy import products
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

acs = cp.products.ACS()

#Converting the CSV files into dataframes
col_index = [i for i in range(29)] + [i for i in range(41, 50)] + [70, 71, 72]
df = pd.read_csv('ev_data.csv', usecols=[i for i in col_index], dtype={'zip': str, 'ev_network_web': str, 'ev_renewable_source': str, 'ev_other_evse': str, 'ev_workplace_charging': str}) 
sdge_areas = pd.read_csv('SDGE_service_list.csv', usecols=['ZipCode'])

#Getting the zip codes for all the areas at SDGE serves
sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]

#Querying the data to only include chargers within the areas that SDGE serves
df = df[df['zip'].isin(sdge_zip_codes)]


#Getting the income census data
sd_income_df = products.ACS(2019).from_county('San Diego, CA', level = 'tract', variables = 'B06011_001E')
oc_income_df = products.ACS(2019).from_county('Orange County, CA', level = 'tract', variables = 'B06011_001E')

income_df = pd.concat([sd_income_df, oc_income_df])
income_df.rename(columns={'B06011_001E': 'Median Income'}, inplace = True)
income_df = income_df.to_crs(epsg=4326)

# Plot of the income distribution with EV charger locations
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15,15))
ax = income_df.plot('Median Income', ax=ax, cmap='plasma', legend=True, legend_kwds={'orientation': 'horizontal'})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

ax.set_facecolor('k')
gdf.plot(ax=ax, color='white', markersize=6)
plt.title('Income Distribution and EV Charger Locations Across SDGE Service Areas');
plt.show()


#Getting the population census data
sd_pop_df = products.ACS(2019).from_county('San Diego, CA', level = 'tract', variables = 'B01003_001E')
oc_pop_df = products.ACS(2019).from_county('Orange County, CA', level = 'tract', variables = 'B01003_001E')

pop_df = pd.concat([sd_pop_df, oc_pop_df])
pop_df.rename(columns={'B01003_001E': 'Population'}, inplace = True)
pop_df = pop_df.to_crs(epsg=4326)

# Plot of the population distribution with EV charger locations
fig, ax = plt.subplots(figsize=(15,15))
ax = pop_df.plot('Population', ax=ax, cmap='plasma', legend=True, legend_kwds={'orientation': 'horizontal'})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

ax.set_facecolor('k')
gdf.plot(ax=ax, color='white', markersize=6)
plt.title('Total Population Distribution and EV Charger Locations Across SDGE Service Areas');
plt.show()


#Getting the number of commuting vehicle census data
sd_com_df = products.ACS(2019).from_county('San Diego, CA', level = 'tract', variables = 'B08015_001E')
oc_com_df = products.ACS(2019).from_county('Orange County, CA', level = 'tract', variables = 'B08015_001E')

com_df = pd.concat([sd_com_df, oc_com_df])
com_df.rename(columns={'B08015_001E': 'Commuting Vehicles'}, inplace = True)
com_df = com_df.to_crs(epsg=4326)

# Plotting the average commuting vehicle count with EV charger locations
fig, ax = plt.subplots(figsize=(15,15))
ax = com_df.plot('Commuting Vehicles', ax=ax, cmap='plasma', legend=True, legend_kwds={'orientation': 'horizontal'})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

ax.set_facecolor('k')
gdf.plot(ax=ax, color='white', markersize=6)
plt.title('Average Commuting Vehicle Count and EV Charger Locations Across SDGE Service Areas');
plt.show()