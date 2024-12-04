# %%
import requests
import pandas as pd

# %%
api_key = ''
station_url = f'https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={api_key}&fuel_type=ELEC'

# %%
request = requests.get(station_url)

# %%
data = request.content
with open('afdc_data.json', 'wb') as f:
    f.write(data)

# %%
x = request.json()

# %%
df = pd.DataFrame(x['fuel_stations']) 
df = df.set_index('station_name')
df = df[df.get('state') == 'CA']
df

# %%
df.to_csv('ev_data.csv')


