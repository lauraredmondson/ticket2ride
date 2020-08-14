# Ticket to ride graph and nodes

# Connections
import numpy as np
from collections import Counter
import pandas as pd

def add_locomotives(board_data,colours):
    '''
    Add locomotives to non-tunnel track

    Parameters
    ----------
    board_data : pandas dataframe with board data

    Returns
    -------
    board_data : pandas dataframe with 'Y' added to column locomotive if track have a locomotive

    '''
    # add two locomotives for each
    
    # for each colour select randomly select route with 2 or 3 length
    for i in range(len(colours)):
        
        # get index of all routes with those colours
        all_indexes = board_data[board_data.trackColour == colours[i]]

        # get routes between 2 and 3 
        all_indexes = all_indexes[all_indexes.tunnel == 'None'].index

        # randomly select from indexes
        idx_choice = np.random.choice(all_indexes,2)
        
        # add 'Y' to the data dict
        board_data.at[idx_choice, 'locomotive'] = 'Y'
    
    return board_data
    
    
def add_tunnels(board_data, colours):
    '''
    Adding tunnels- each colour has 1 tunnels totaling 2 or 3 spaces

    Parameters
    ----------
    board_data : pandas dataframe with board data
        
    colours : List of colours
        
    Returns
    -------
    board_data : pandas dataframe with 'Y' added to column tunnel if track should be tunnel

    '''
    
    # for each colour select randomly select route with 2 or 3 length
    for i in range(len(colours)):
        
        # get index of all routes with those colours
        all_indexes = board_data[board_data.trackColour == colours[i]]
        
        # get routes between 2 and 3 
        all_indexes = all_indexes[all_indexes['trackLength'].between(2, 3)].index

        # randomly select from indexes
        idx_choice = np.random.choice(all_indexes)
        
        # add 'Y' to the data dict
        board_data.at[idx_choice, 'tunnel'] = 'Y'
    
    return board_data
    

def create_board_colouring(route_list ,route_len, double_routes_list, double_routes_len, seed):
    '''
    Create the colouring for the board based on europe game counts. 
    Adds suggested locomotive and tunnel placement.
    
    Based on Ticket to ride Europe colour data:
    Colours: between 22-23 of each (use 22 here)
    Grey: 100
    
    Colour tunnels: 2-3 of each
    Grey tunnels: 19 
    
    locomotives: 17    
    
    Currently only 1 tunnel for each colour, and 2 locomotives for each colour
    
    
    Parameters
    ----------
    route_list : list of neighbouring routes
    
    route_len : length of each neighbouring route
    
    double_routes_list : list of neighbouring routes (duplicates)
    
    double_routes_len : length of each neighbouring duplicate route
        
    seed : int, random seed setting

    Returns
    -------
    board_data : pandas dataframe with information about board 
                 colouring, tunnel and locomotive placement.
    '''
    
    # add seed
    np.random.seed(seed)
    
    # append the extra route
    route_list = route_list + double_routes_list
   
    route_len = np.append(route_len,double_routes_len) # append double routes to route list
        
    # create initial number of track colours dict
    track_colour_dict ={'yellow':22,'blue':22,'green':22,'red':22,'purple':22,'black':22,'white':22,'orange':22,
           'grey':100}
    
    colours = list(track_colour_dict.keys()) # get list of colours from dictionary
    
    # convert to probabilities
    prob = np.array([*track_colour_dict.values()], dtype=np.float32)

    prob = prob/np.sum(prob)
    
    select_array = np.linspace(0,len(prob)-1,len(prob))

    # create dataframe
    board_data = pd.DataFrame(route_list, columns= ['place1', 'place2'])
    board_data['trackLength'] = route_len
    board_data['trackColour'] = ['None'] * len(route_list)
    board_data['tunnel'] = ['None'] * len(route_list)
    board_data['locomotive'] = ['None'] * len(route_list)
    
    
    # create color for each track section between two nodes
    for idx, route_length in enumerate(route_len):

        idx_choice = np.random.choice(select_array, 1, p=prob) # select color based on probabilities
        
        # index of selected colour
        colour_sel = colours[int(idx_choice)] # get the random colour index
        
        # update numbers of colours list
        track_colour_dict[colour_sel] -= int(route_length)
        
        # update probabilities
        prob = np.array([*track_colour_dict.values()], dtype=np.float32)
        
        for p, item in enumerate(prob): # check that no item is less than 0
            if item < 0:
                prob[p] = 0 # set probability to zero if less than zero
        
        prob = prob/np.sum(prob)

        # add colour to list
        board_data.at[idx, 'trackColour'] = colour_sel
    
    # add random tunnels to board
    board_data = add_tunnels(board_data, colours)
    
    # add random locomotives
    board_data = add_locomotives(board_data, colours)
    
    # count number of each board colour
    colour_counts = Counter(board_data.trackColour)

    return board_data, colour_counts
