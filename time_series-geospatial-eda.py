# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
#Converting the CSV files into dataframes
col_index = [i for i in range(29)] + [i for i in range(41, 50)] + [70, 71, 72]
df = pd.read_csv('ev_data.csv', usecols=[i for i in col_index], dtype={'zip': str, 'ev_network_web': str, 'ev_renewable_source': str, 'ev_other_evse': str, 'ev_workplace_charging': str}) 
sdge_areas = pd.read_csv('data/SDGE_service_list.csv', usecols=['ZipCode'])

# %%
#Getting the zip codes for all the areas at SDGE serves
sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]
sdge_zip_codes

# %%
#Querying the data to only include chargers within the areas that SDGE serves
df = df[df['zip'].isin(sdge_zip_codes)]
df

# %% [markdown]
# # Time-Series Graphs

# %%
#Creating new columns 

#Cleaning the data to get rid of any NaN values in the open_date column
time_df = df.dropna(subset=['open_date'])

#Making the open_date column into a datetime object
time_df['open_date'] = pd.to_datetime(time_df['open_date'])

time_df

# %%
#Creating a dataframe for the number of EV chargers opened every year for every city
time_graph = time_df
time_graph['open_year'] = df['open_date'].str[:4]
time_graph['open_year'] = time_graph['open_year'].dropna()
time_graph['open_year'] = time_graph['open_year'].astype(int)
time_graph = time_graph.groupby(['open_year', 'city']).count()
time_graph = time_graph.reset_index()
time_graph = time_graph[['open_year', 'city', 'station_name']]
time_graph['station_name'] = time_graph['station_name'].astype(float)
time_graph

# %%
#Array of all of the names of the cities that SDGE serves
city_names = time_graph['city'].unique()
city_names

# %%
#Plotting the number of EV chargers for every city over time
graph_df = pd.DataFrame() 
graph_df['open_year'] = np.arange(1997, 2025)

for city in city_names:
    num_chargers = []
    time_graph_subset = time_graph[time_graph['city'] == city].set_index('open_year')
    for i in graph_df['open_year']:
        if i in time_graph_subset.index:
            num_chargers = num_chargers + [time_graph_subset['station_name'].loc[i]]
        else:
            num_chargers = num_chargers + [0]
    graph_df[city] = num_chargers
    
graph_df = graph_df.set_index('open_year')

graph_df.plot(title = 'Change in the Number of EV Chargers for Every City Served by SDGE', xlabel = 'Year', ylabel = 'Number of Chargers');
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left');

# %%
#Time Series Plot to see if wealth has an impact on EV charger placement
graph_subset = graph_df.reset_index()
graph_subset = graph_subset[graph_subset['open_year'] >= 2009]
graph_subset = graph_subset.set_index('open_year')
graph_subset[['Rancho Santa Fe', 'Jamul', 'Del Mar', 'National City', 'Campo', 'Camp Pendleton']].plot(title = 'Change in the Number of EV Chargers for Top 3 Highest and Lowest Income Cities', xlabel = 'Year', ylabel = 'Number of Chargers');
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left');

# %%
#Total number of chargers over time
time_graph.plot('open_year', title = 'Number of EV Chargers Over Time', xlabel = 'Year', ylabel = 'Number of Chargers');

# %% [markdown]
# # Geospatial Plots

# %%
# Load GeoJSON
import geopandas as gpd
from shapely.geometry import Point

# %%
#Finding the total number of chargers in every city

total_chargers = df.groupby('city', as_index=False).count()
total_chargers['num_chargers'] = total_chargers['station_name']
total_chargers = total_chargers[['city', 'num_chargers']]
# total_chargers = total_chargers.loc[total_chargers['city'].isin(sdge_df['name'].unique())]
total_chargers['city'] = total_chargers['city'].str.strip()
total_chargers

# %%
#Creating a map of every city SDGE serves

#San Diego cities
geo_df5 = gpd.read_file('data/zip_codes.geojson')
geo_df5['name'] = geo_df5['community']
geo_df5 = geo_df5[['name', 'geometry']]

#Orange County cities
oc_df = gpd.read_file('data/oc_boundaries.geojson')
oc_df['name'] = oc_df['NAME']
oc_df = oc_df[['name', 'geometry']]
oc_df = oc_df.loc[oc_df['name'].isin(city_names)]
    
#All cities combined
sdge_df = pd.concat([geo_df5, oc_df])
sdge_df['name'] = sdge_df['name'].str.strip()

#Plotting the SDGE service area map
sdge_df.plot(column = 'name', legend = True, legend_kwds={'loc': 'upper left', 'bbox_to_anchor': (1, 1)})

# %%
#Creating a choropleth map of the number of chargers in every city

#Combining the mapping data and the total number of chargers data together 
gdf = sdge_df.merge(total_chargers, left_on='name', right_on='city')  

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot the choropleth map
gdf.boundary.plot(ax=ax, linewidth=1, color='black') 
gdf.plot(column='num_chargers', ax=ax, legend=True,
         cmap='OrRd',  # Choose a colormap
         missing_kwds={'color': 'lightgrey', 'label': 'Missing values'})  # Handle missing values

# Customize the plot
plt.title('Total Number of Electric Vehicle Chargers in Every City in San Diego County')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('off')  

#Putting labels for every city
for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['city']):
    ax.annotate(label, xy=(x, y), horizontalalignment='center', fontsize=5, color='black')


# Show the plot
plt.show()

# %%
#Dataframe without San Diego chargers
gdf2 = sdge_df.merge(total_chargers[total_chargers['city'] != 'San Diego'], left_on='name', right_on='city', how = 'left')  # Adjust 'name' if needed
gdf2

# %%
#Creating a choropleth map for the number of chargers in every city, excluding San Diego

#Dataframe without San Diego chargers
gdf2 = sdge_df.merge(total_chargers[total_chargers['city'] != 'San Diego'], left_on='name', right_on='city', how = 'left')  # Adjust 'name' if needed
gdf2

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot the choropleth map
gdf2.boundary.plot(ax=ax, linewidth=1, color='black') 
gdf2.plot(column='num_chargers', ax=ax, legend=True,
         cmap='OrRd',  # Choose a colormap
         missing_kwds={'color': 'lightgrey', 'label': 'Missing values'})  # Handle missing values

# Customize the plot
plt.title('Total Number of Electric Vehicle Chargers in Every City in SDGE Serves')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('off') 

#Putting labels for every city
for x, y, label in zip(gdf2.geometry.centroid.x, gdf2.geometry.centroid.y, gdf2['city']):
    ax.annotate(label, xy=(x, y), horizontalalignment='center', fontsize=5, color='black')


# Show the plot
plt.show()

# %%
#Creating a map of how close EV chargers are to transit stops

#Data for every transit stop in San Diego county
geo_df7 = gpd.read_file('data/transit_stops.geojson')

ax = gdf.plot()

# Plot the second GeoDataFrame on top
gdf_test = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
ax1 = gdf_test.plot(ax=ax, color = 'yellow', markersize = 2)
geo_df7.plot(ax=ax1, color="red", markersize = 0.5, alpha = 0.1)

plt.title('Transit Stops (Red) with EV Charger Locations (Yellow) Across SDGE Service Areas');
plt.axis('off');


