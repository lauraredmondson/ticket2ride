# Ticket to ride graph and nodes

# Connections
import numpy as np

def get_t2r_europe_ticket_counts():
    '''
    Routes number will be done according to rough Ticket to ride
    Europe counts:
        
    Short routes:
    5 points: 5
    6 points: 5
    7 points: 5
    8 points: 13
    9 points: 2
    10 points: 5
    11 points: 2
    12 points: 2
    13 points: 1

    Long routes will be 20 cards upwards
    20 points: 3
    21 points: 3
    
    Include some bigger point routes (not in Europe game):
    22 points: 2
    23 points: 2

    Returns
    -------
    short_counts : dict of short route counts
    long_counts : dict of long route counts

    '''
    
    short_counts = {'5':5,'6':5,'7':5,'8':13,'9':2,'10':5,'11':2,'12':2,'13':1} # number of each pointed tickets
    
    long_counts = {'20':3,'21':3,'22':2,'23':2} 
    
    
    return short_counts, long_counts
    


def get_routes(data, counts, seed):
    '''
    Calculate the route cards

    Parameters
    ----------
    data : dict of distance lengths
        
    seed : int, seed for determining which place pairs are selected

    Returns
    -------
    route_sh : list of pairs for short routes
    points_sh : array of points for short route pairs

    '''
    
    np.random.seed(seed) # set random seed to generate card pairs
    
    total_cards = sum(list(counts.values())) # get total points value
    
    count_added = 0 # set couter
    
    points = np.zeros((total_cards,1)) # initialise points array
    
    route = [] # create list
    
    # go through each number- for each select a random number of routes. If the number is greater
    # than routes select maximum and add number of fails to array
    for point in counts:
        num = np.linspace(0,len(data[point])-1,len(data[point]))
        select = np.random.choice(num,counts[point],replace=False)
        
        for j in range(counts[point]):
            route.append(list(data[point][int(select[j])]))
            points[count_added ] = point
            count_added += 1

    return route, points
    


def get_start_end_destination(routes):
    '''
    Returns the start and end destination in separate lists for all route cards

    Parameters
    ----------
    routes : List of all generated route pairs

    Returns
    -------
    place1 : list of first place name in routes
    place2 : list of second place name in routes

    '''
    
    place1 = []
    place2 = []

    for pair in routes:
        place1.append(pair[0])
        place2.append(pair[1])
        
    return place1, place2
    
    