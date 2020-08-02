# Ticket to ride singapore board and ticket creation

import pandas as pd
import ticket_to_ride as t2r 
import matplotlib.font_manager as fm

# WARNING:change to file location of your fonts
font = fm.FontProperties(fname='C:/WINDOWS/FONTS/SHANLNC.ttf')

# %% Load data from the .csv file as pandas Dataframe

locations = pd.read_csv('ticket2ride_singapore_locations.csv') # load the location data

connections = pd.read_csv('ticket2ride_singapore_connections.csv')  # load the connection data

double_routes, double_len = t2r.get_double_routes(connections) # list of lists for routes, list conenctions

# %% Create graph for singapore
singapore_graph = t2r.build_graph(locations, connections)

# In[Plot graph]

t2r.draw_graph(singapore_graph)

# create dictionary with each short distance (points) and all routes with that distance    
len_data, _ = t2r.create_data_dictionary(singapore_graph)    
   
# get data on the closest neighbours to each node
all_routes, route_len = t2r.get_all_neighbours(singapore_graph)  


# In[create the board colouring with the double routes]
board_data, colour_counts = t2r.create_board_colouring(all_routes,route_len,double_routes,double_len,10)

# %%
# Get the board colouring and add double routes
t2r.show_board_colour(board_data,singapore_graph)

# In[Create the route cards]
# get counts for each route length based on Europe game
short_counts, long_counts = t2r.get_t2r_europe_ticket_counts()

# get short routes
short_routes, short_points = t2r.get_routes(len_data, short_counts, 30)

# get long routes
long_routes, long_points = t2r.get_routes(len_data, long_counts, 30)

# %%
# separate short routes into two lists- start and end destination   
short_routes_place1, short_routes_place2 = t2r.get_start_end_destination(short_routes)

# separate long routes into two lists- start and end destination    
long_routes_place1, long_routes_place2 = t2r.get_start_end_destination(long_routes)

# %% 
# create the tickets for short routes
t2r.create_tickets(short_routes,singapore_graph,short_points,font,'short')    

# create the tickets for long routes
t2r.create_tickets(long_routes,singapore_graph,long_points,font,'long') 