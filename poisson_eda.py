# %%
import pandas as pd
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# %%
# Getting zip codes within SDGE service areas
sdge_areas = pd.read_csv('data/SDGE_service_list.csv', usecols=['ZipCode'])
sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]

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
# Getting car registrations within the SDGE zip codes
sdge_df = df[df['Zip Code'].isin(sdge_zip_codes)]

# Getting only electric car registrations
ev_sdge = sdge_df[sdge_df['Fuel'] == 'Battery Electric']

# %%
# Rearranging the order of ev_sdge
ev_sdge = ev_sdge.groupby(['Date', 'Zip Code']).Vehicles.sum().reset_index()
ev_sdge = ev_sdge.pivot(index = 'Zip Code', columns = 'Date', values = 'Vehicles').fillna(0).reset_index()
ev_sdge = ev_sdge.melt(id_vars = ['Zip Code'], var_name = 'Date', value_name = 'counts')
ev_sdge

# %%
# Poisson distribution for each zip code
poisson_dict = {}
for z in ev_sdge['Zip Code'].unique():
    counts = ev_sdge[ev_sdge['Zip Code'] == z]['counts']
    lambda_val = np.mean(counts)
    poisson_dict[z] = lambda_val

poisson_dict

# %%
# Conducting 1000 random samples for the Monte Carlo distribution
results = {}
n_samples = 1000
for i in range(n_samples):
    val = []
    for z in poisson_dict.keys():
        value = poisson.rvs(mu = poisson_dict[z], size = 1)
        val.append(value[0])
        results[i] = val

# %%
# Putitng the results into a dataframe
ev_results = pd.DataFrame(results, index = poisson_dict)
ev_results

# %%
# Plotting the results on a histogram
ev_results.sum(axis=0).hist(bins = 7)
plt.title('Distribution of the Total Number of EV Registraions in a Zip Code')
plt.xlabel('Number of EV Registrations')
plt.ylabel('Count')
plt.show()

# %% [markdown]
# # Choropleth Map of the Confidence of the Mean EV Registrations Per Zip Code Using Coefficient of Variation

# %%
# Load GeoJSON
import geopandas as gpd
from shapely.geometry import Point

# %%
# Number of samples for the Monte Carlo simulation
n_samples = 1000

# Simulating the Monte Carlo results and calculating mean, standard deviation, and coefficient of variation (CV)
simulation_results = []

for zip_code, mean in poisson_dict.items():
    samples = np.random.poisson(mean, size=n_samples)
    mean_value = np.mean(samples)
    std_dev = np.std(samples)
    # Coefficient of Variation (CV) = std_dev / mean
    if mean_value != 0:
        cv = std_dev / mean_value 
    else:
        cv = np.inf 
    simulation_results.append({
        'Zip Code': zip_code,
        'Mean': mean_value,
        'Standard Deviation': std_dev,
        'Coefficient of Variation': cv
    })

# Creating a dataframe of the simulation results
df_simulation = pd.DataFrame(simulation_results)
df_simulation

# %%
# SD boundaries
geo_df5 = gpd.read_file('data/zip_codes.geojson')
geo_df5['name'] = geo_df5['community']
geo_df5['Zip Code'] = geo_df5['zip']
geo_df5 = geo_df5[['name', 'geometry', 'Zip Code']]

# Merging the CV values with the SD boundaries
merged_df = geo_df5.merge(df_simulation, how='left', on='Zip Code')
merged_df['name'] = merged_df['name'].astype(str)
merged_df

# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot the choropleth map
merged_df.boundary.plot(ax=ax, linewidth=1, color='black') 
merged_df.plot(column='Coefficient of Variation', ax=ax, legend=True,
         cmap='Blues',  # Choose a colormap
         missing_kwds={'color': 'lightgrey', 'label': 'Missing values'})  # Handle missing values

# Customize the plot
plt.title('Confidence of the Mean EV Registrations Per Zip Code')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('off')  

#Putting labels for every city
for x, y, label in zip(merged_df.geometry.centroid.x, merged_df.geometry.centroid.y, merged_df['name']):
    ax.annotate(label, xy=(x, y), horizontalalignment='center', fontsize=5, color='black')

# Show the plot
plt.show()


