# Ticket to ride graph and nodes

# Connections
import networkx as nx
import numpy as np


def build_graph(locations, connections):
    '''
    Creates the graph structure with nodes (places) and connections between
    them according to the map

    Parameters
    ----------
    locations : pandas dataframe with location coordinates
    connections : pandas dataframe with place connections

    Returns
    -------
    G : network X graph

    '''
    
    G = nx.Graph() # create empty graph

    for idx, place in enumerate(locations.place): # add the node locations

        x = locations.coord_x[idx]  # get x coordinate
        y = locations.coord_y[idx]  # get y coordinate
        
        G.add_node(place, pos =(x,y)) # add node with place name and coordinates
        
     
    for idx in range(connections.shape[0]): # add the connections
        
        G.add_edge(connections.place_1[idx], connections.place_2[idx], weight=connections.length[idx]/10)

    
    return G


def get_double_routes(connections):
    '''
    Get list of double routes and their lengths

    Parameters
    ----------
    connections : pandas dataframe with place connections

    Returns
    -------
    double_routes : list of lists with two place names
    double_route_len : list of corresponding lengths for each pair

    '''
    
    double_routes = []
    double_routes_len = []
    
    for idx in range(len(connections)):
        
        if connections.double_route[idx] == 'Y':
            double_routes.append([connections.place_1[idx],connections.place_2[idx]])
            double_routes_len.append(connections.length[idx])


    return double_routes, double_routes_len


def shortest_path_route(graph):
    '''
    Get the shortest path between all place combinations using 
    Dijkstra.
    
    Parameters
    ----------
    graph : network X graph

    Returns
    -------
    dist_upper : numpy array of size no.places X np.places
                 Shortest path distances between all places (upper half only as symmetric)
    location_keys : numpy array of all corresponding location keys to shortest path array

    '''
    
    lengths = dict(nx.all_pairs_dijkstra_path_length(graph))    # Calculate all path lengths using network X function
    
    location_keys = np.sort(list(lengths.keys()))    # Convert to an array
    
    dist_table = np.zeros((len(location_keys),len(location_keys)))     # initialise array for distances
    
    # add data to array
    for i in range(len(location_keys)):
        for j in range(len(location_keys)):
            dist_table[i,j] = round(lengths[location_keys[i]][location_keys[j]]*10)
    
    dist_table = dist_table.astype(int)     # convert to integers
    
    dist_upper = np.triu(dist_table)     # get top part only

    return dist_upper, location_keys    # return distance table and keys



def create_data_dictionary(graph):
    '''
    Create a new data dictionary split by route length
    no duplicates of routes included (reversed duplicates, need to keep double routes)    

    Parameters
    ----------
    graph : network X graph

    Returns
    -------
    data_dict : dictionary of length keys (number of unique shortest paths). 
                List for each unique shortest path of all place pairs with that distance
    
    dist : Array of shortest distances from shortest_path_route

    '''
    
    sh_path = shortest_path_route(graph)     # find shortest paths
        
    dist = sh_path[0]   # get array of distances
    
    loc_keys = sh_path[1]   # get corresponding place names
    
    unique_lengths,length_counts = np.unique(dist,return_counts=True) # get all the unique shortest lengths
    
    unique_lengths = np.nonzero(unique_lengths)[0] # remove zero lengths (distance to selves)
    
    length_counts =np.delete(length_counts,0) # remove the first element from length counts (number of zero counts)

    data_dict = {}    # create dict
    
    for counts_idx, length in enumerate(unique_lengths):
        
      d_locs =  list(zip(*np.where(dist == int(length))))   # find indexes in distance array that equal chosen length

      data_dict[str(length)] = [] # initialise list at dictionary key
      
      for j, value in enumerate(d_locs): # cycle through each pair
      
          data_dict[str(length)].append([str(loc_keys[value[0]]), str(loc_keys[value[1]])]) # add locations to dictionary

    return data_dict,dist            



def get_all_neighbours(graph):
    '''
    Gets list of all nodes which are neighbouring and length of the connection

    Parameters
    ----------
    graph : network x graph

    Returns
    -------
    all_routes : List of all nearest neighbour pairs
    
    route_len : Array of route lengths between neighbours

    '''

    all_routes = []     # create list of neighbour pairs
    
    nodes = list((graph._node).keys())     # get all individual node names

    for node in nodes: # iterate through each node 'place' name
        
        neighbours = list(graph.neighbors(node))         # get all neighbours for each node
         
        for neighbour in neighbours:
            all_routes.append(sorted([node,neighbour])) # sort neighbours and add to list

            
    all_routes_set = set(tuple(x) for x in all_routes)     # remove duplicate pairs

    all_routes = [list(x) for x in all_routes_set]    # change to list
   
    data = graph.adj # extract atlas from graph (neighbours and distances)
    
    route_len = np.zeros((len(all_routes),1)) # initialise array to hold route lengths
    
    # get length of routes for pairs using network x atlas
    for idx in range(len(all_routes)):
        route_len[idx] = int(data[all_routes[idx][0]][all_routes[idx][1]]['weight']*10) # add length of connection
        
    return all_routes, route_len
   
