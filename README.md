# Location-Based Optimization of Electric Vehicle Charging Networks

This project aims to find the best locations within SDGE service areas to implement electric vehicle charging stations. It will identify the factors that influence where current EV chargers are, and discover how we can use these factors to find additional areas to place charging stations.

## Running the project

* To install the dependencies, run the following command from the root directory of the project: `pip install -r requirements.txt`
* The `AFDC_data.ipynb` notebook uses an API to access data from the Alternative Fuels Data Center. It will create the `afdc_data.json` and the `ev_data.csv` files locally, which will be used in the EDA notebooks below. __Make sure that this is the first notebook that you run.__
* The `time_series-geospatial-eda.ipynb` notebook will use the various CSV files in the repository to perform EDA. It will create several time-series and geospatial plots depicting information about the location of the EV chargers from `ev_data.csv` with its geographical location as well as other factors in the dataset. __This should be the second notebook that you run.__
* The `cenpy_eda.ipynb` notebook uses US census data to create heat maps of the San Diego area. It also plots the location of the EV chargers on the heat maps so we can see if certain census data is correlated with the location of the chargers.
* The `osmnx-_da.ipynb` notebook uses the OSMNX package to retrieve data about San Diego's infrastructure, street layout, and urban planning. It uses this data to create a plot of San Diego, which I used to display the route from the SDGE campus to a selected EV charger at UCSD.
* The `distribution_graphs_eda.ipynb` notebook uses vehicle registration data from the California Open Data Portal. It shows the relationship between the vehicle's registration year, the city it was registered in, and the model of the vehicle through distribution plots. 
