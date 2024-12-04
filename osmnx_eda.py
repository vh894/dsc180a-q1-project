# %%
import osmnx as ox
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# %%
ox.config(use_cache=False)

# Define the location for San Diego
place_name = "San Diego, California, USA"

# Download the street network for San Diego
graph = ox.graph_from_place(place_name, network_type='drive')

# %%
# Define the start and end coordinates
sdge = (32.8242841, -117.1455205)
charger = (32.88075714315878, -117.2419615625954)

# Get the nearest nodes in the graph to the start and end points
start_node = ox.distance.nearest_nodes(graph, sdge[1], sdge[0])
end_node = ox.distance.nearest_nodes(graph, charger[1], charger[0])

# Calculate the shortest path
shortest_route = ox.shortest_path(graph, start_node, end_node, weight='length')

# Plot the shortest route
fig, ax = ox.plot_graph_route(graph, shortest_route, node_size = 1, route_linewidth=4)


# %%
#Length of the route
edge_lengths = ox.utils_graph.get_route_edge_attributes(graph, shortest_route, 'length')
print('Distance from SDGE to charger in meters:', round(sum(edge_lengths)))

# %%
#Interactive route map

#use networkx to calculate the shortest path between 2 nodes
origin_node = start_node #list(graph.nodes())[0]
destination_node = end_node #list(graph.nodes())[-1]
route = nx.shortest_path(graph, origin_node, destination_node)

#plot the route with folium
ox.plot_route_folium(graph, route, weight = 6)


