# Location-Based Optimization of Electric Vehicle Charging Networks

This project aims to find the factors that influence the location of electric vehicle (EV) charging stations within SDG&E service areas. It will perform data analysis with various features and datasets to discover the primary variables involved with EV charger placement.

## Description of the files
* The `AFDC_data.py` file uses an API to access data from the Alternative Fuels Data Center. It will create the `afdc_data.json` and the `ev_data.csv` files locally, which will be used in the EDA notebooks below. __Make sure that this is the first notebook that you run.__
* The `time_series-geospatial-eda.py` file will use the various CSV files in the repository to perform EDA. It will create several time-series and geospatial plots depicting information about the location of the EV chargers from `ev_data.csv` with its geographical location as well as other factors in the dataset. __This should be the second notebook that you run.__ Below is a list of all the datasets from the repository that the `time_series-geospatial-eda.py` file utilizes:
  * `ev_data.csv`: This file is created when you run `AFDC_data.py`
  * `SDGE_service_list.csv`: This file is in the `data` folder. It lists all the zip codes that SDG&E provides services for.
  * `zip_codes.geojson`: This file is in the `data` folder. It lists the geospatial boundaries of every city in San Diego County.
  * `oc_boundaries.geojson`: This file is in the `data` folder. It lists the geospatial boundaries of every city in Orange County.
  * `transit_stops.geojson`: This file is in the `data` folder. It lists all the transit stop locations in San Diego county.
* The `cenpy_eda.py` file plots choropleth maps based on US census data accessed through the Cenpy Python package. It also plots the location of the EV chargers on the heat maps so we can see if certain census data is correlated with the location of the chargers. Below is a list of all the datasets from the repository that the `cenpy.py` file utilizes:
  * `ev_data.csv`: This file is created when you run `AFDC_data.py`
  * `SDGE_service_list.csv`: This file is in the `data` folder. It lists all the zip codes that SDG&E provides services for. 
* The `osmnx-eda.py` file uses the OSMNX package to retrieve data about San Diego's infrastructure, street layout, and urban planning. It uses this data to create a plot of San Diego, which I used to display the route from the SDGE campus to a selected EV charger at UCSD.
* The `distribution_graphs_eda.py` file uses vehicle registration data from the California Open Data Portal. It shows the relationship between the vehicle's registration year, the city it was registered in, and the model of the vehicle through distribution plots. Below is a list of all the datasets from the repository that the `distribution_graphs_eda.py` file utilizes:
  * `2019_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2019.
  * `2020_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2020.
  * `2021_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2021.
  * `2022_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2022.
  * `2023_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2023.
  * `2024_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2024.
  * `ev_data.csv`: This file is created when you run `AFDC_data.py`
  * `SDGE_service_list.csv`: This file is in the `data` folder. It lists all the zip codes that SDG&E provides services for.
  * `zip_codes.geojson`: This file is in the `data` folder. It lists the geospatial boundaries of every city in San Diego County.
* The `poisson_eda.py` file uses vehicle registration data from the California Open Data Portal to conduct a Poisson distribution and a Monte Carlo simulation of the data. It shows the mean value of EV registrations for every zip code as well as it's confidence after conducting the simulation and then plots these results.
  * `2019_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2019.
  * `2020_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2020.
  * `2021_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2021.
  * `2022_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2022.
  * `2023_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2023.
  * `2024_data.csv`: This file is in the `distribution_graph_data` folder. It has data on all CA car registrations from 2024.
  * `SDGE_service_list.csv`: This file is in the `data` folder. It lists all the zip codes that SDG&E provides services for.
  * `zip_codes.geojson`: This file is in the `data` folder. It lists the geospatial boundaries of every city in San Diego County.
  
## Running the project
1. Download all of the files in the GitHub repository.
2. Open VS Code as your code editor. Make sure you have Python and Jupyter, both of which are published by Microsoft, installed as extensions on your VS Code. These extensions will allow run cells within each Python file in the Python Interactive window on VS Code. 
3. To install the dependencies, run the following command: `pip install -r requirements.txt`. Ensure that all the library versions listed in `requirements.txt` are installed in your VS Code environment. 
4. Open all of the files from this GitHub repository in VS Code. If you see the words "Run Cell | Run Above | Debug Cell" above each cell in the Python files, then you have the extensions from Step 2 correctly added. 
5. Navigate to the `AFDC_data.py` file. This Python file requires you to have an API to access the data. To get an API, go to `https://developer.nrel.gov/signup/`. Once you get your API key, replace the value of the variable `api_key` in the file with your personal API key as a string. Run each cell in this file by clicking the "Run Cell" text above each cell.
  - The fourth cell in this file will create the `afdc_data.json` file based on the data you requested with your API.
  - The last cell in this file will convert `afdc_data.json` into a CSV file called `ev_data.csv`.
6. Navigate to the `time_series-geospatial-eda.py` file. Run each cell in this file. This should create 3 time-series plots and 4 geospatial plots in the Python Interactive window.
7. Navigate to the `cenpy_eda.py` file. Run each cell in this file. This should create 4 choropleth maps in the Python Interactive window.
8. Navigate to the `osmnx-eda.py` file. Run each cell in this file. This should create 2 maps in the Python Interactive window. One map shows all the streets in San Diego County and a red line depicting the shortest distance from a selected EV charger to the SDG&E office location. The second map is an interactive map that also shows the shortest distance from the selected EV charger to the SDG&E office location.
9. Navigate to the `distribution_graphs_eda.py` file. Run each cell in this file. This should create 1 bar graph, 1 pie chart, 1 choropleth map, 1 histogram, and 4 distribution graphs in the Python Interaction window.
10. Navigate to the `poisson_eda.py` file. Run each cell in this file. This should create 1 histogram and 1 choropleth map in the Python Interaction window.
