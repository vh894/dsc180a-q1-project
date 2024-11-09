import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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


#Plotting the distribution of vehicles based on their fuel type of registration year
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='Year', weights='Vehicles', hue='Fuel', fill=True, common_norm=False)
plt.title('Density Plot of Vehicle Counts by Registration Year and Fuel Type')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()

#Plot of distribution of fuel type from all 2018 to 2023
grouped_df = df.groupby('Fuel').count()
grouped_df.rename(columns={'_id': 'Count'}, inplace = True)
grouped_df = grouped_df[['Count']]

ax = grouped_df.plot.pie(y='Count')
plt.legend(bbox_to_anchor=(1.5, 1), loc='upper left')
plt.title('Distribution of Fuel Type')


#Getting the zip codes in SDGE service areas
#Converting the CSV files into dataframes
col_index = [i for i in range(29)] + [i for i in range(41, 50)] + [70, 71, 72]
sdge_areas = pd.read_csv('SDGE_service_list.csv', usecols=['ZipCode'])

sdge_zip_codes = [str(element) for element in sdge_areas['ZipCode'].unique()]

#Trying to see what the average EV registration rate is across all SDGE areas
sdge_df = df[df['Zip Code'].isin(sdge_zip_codes)]
ev_sdge = sdge_df[sdge_df['Fuel'] == 'Battery Electric']
grouped_ev_sdge = ev_sdge[['Zip Code', 'Vehicles']]
grouped_ev_sdge = grouped_ev_sdge.groupby('Zip Code').sum()
grouped_ev_sdge['Vehicles'].hist()
plt.title('Distribution of Total EV Registrations Across SDGE Zip Codes from 2018 to 2024')
plt.xlabel('Number of EV Registrations')
plt.ylabel('Frequency')
plt.show()


#Plot to see the distribution of vehicles based on their registration year and their fuel type. This plot only displays cars within SDGE areas.
plt.figure(figsize=(10, 6))
sns.kdeplot(data=sdge_df, x='Year', weights='Vehicles', hue='Fuel', fill=True, common_norm=False)
plt.title('Distribution of Vehicles by Registration Year and Fuel Type for SDGE Service Areas')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()


#Plot to see the distribution of EV models across SDGE areas
plt.figure(figsize=(10, 6))
sns.kdeplot(data=ev_sdge, x='Year', weights='Vehicles', hue='Make', fill=True, common_norm=False)
plt.title('Density Plot of Vehicle Counts by Registration Year and EV Makes for SDGE Service Areas')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()


#Making a new column that displays whether the EV is from Tesla 
make_df = ev_sdge[['Make', 'Vehicles', 'Year']]
make_df['is_tesla'] = np.where(make_df['Make'] == 'TESLA', 'Yes', 'No')

#Plot to show how many Tesla vehicles are being registered compared to other EV models
plt.figure(figsize=(10, 6))
sns.kdeplot(data=make_df, x='Year', weights='Vehicles', hue='is_tesla', fill=True, common_norm=False)
plt.title('Density Plot of Tesla Vehicles in SDGE Service Areas By Registration Year')
plt.xlabel('Model Year')
plt.ylabel('Density')
plt.show()