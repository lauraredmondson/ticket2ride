# Ticket to ride graph and nodes

# Connections
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

def draw_graph(graph):
    '''
    Visualise the graph

    Parameters
    ----------
    graph : network x graph

    '''
    
    plt.figure(figsize=(13,7))
    
    edges,weights = zip(*nx.get_edge_attributes(graph,'weight').items())
    
    pos = nx.get_node_attributes(graph, 'pos')

    # draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=70)
    
    # draw edges
    nx.draw_networkx_edges(graph, pos, node_color='b', edge_color=weights, 
                           edge_cmap=plt.cm.Blues, edgelist=edges,
                           width=2)
    
    # add labels
    nx.draw_networkx_labels(graph, pos, font_size=5, label_pos=1, font_family='sans-serif')
    
    plt.axis('off')
    plt.gca().invert_yaxis()
    plt.savefig("weighted_graph.pdf")
    plt.show()


def show_board_colour(board_data,G):    
    '''
    Recreate board colouring on the graph, plots and saves as .pdf file

    Parameters
    ----------
    board_colour : pandas dataframe with board data
        
    G : network x graph

    Returns
    -------
    None.

    '''
    
    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())   # get list of nodes locations

    node_locations = nx.get_node_attributes(G, 'pos')  # get list of nodes locations

    colours = {'yellow':[1,1,0],'blue':[0,0,1],'green':[0,1,0],'red':[1,0,0],'purple':[0.5,0,0.5],'black':[0,0,0],'white':[0.9,0.9,0.9],'orange':[1,0.7,0],
           'grey':[0.5,0.5,0.5]}
    

    nx.draw_networkx_nodes(G, node_locations, node_size=70)     # plot nodes
    
    duplicates = board_data.pivot_table(index=['place1','place2'], aggfunc='size')
    
    duplicate_split = len(duplicates)   # find locations of duplicates
    
    X_all = []
    Y_all = []
    colour = np.zeros((len(board_data),3))
    
    # plot connections for single routes
    for idx in range(duplicate_split):
        
        # extract coordinates of two neighbours
        pair = [board_data.place1[idx],board_data.place2[idx]]
        
        X = [node_locations[pair[0]][0], node_locations[pair[1]][0]]
        Y = [node_locations[pair[0]][1], node_locations[pair[1]][1]]
        
        X_all.append(X)     # append to array of all x coords
        Y_all.append(Y)     # append to array of all y coords
        
        colour[idx,:] = colours[board_data.trackColour[idx]]    # add colour RGB code
    
     # show double routes
     # find distances between two nodes. Plot until halfway
    for idx in range(duplicate_split+1,len(board_data)):
        
        # extract coordinates of two neighbours
        pair = [board_data.place1[idx],board_data.place2[idx]]
        
        X_dup = [node_locations[pair[0]][0], node_locations[pair[1]][0]]
        Y_dup = [node_locations[pair[0]][1], node_locations[pair[1]][1]]
        
        # find midpoint between two coords
        X_dup[1] = (X_dup[0] + X_dup[1])/2
        Y_dup[1] = (Y_dup[0] + Y_dup[1])/2
        
        X_all.append(X_dup)     # append to array of all x coords
        Y_all.append(Y_dup)     # append to array of all y coords

        colour[idx,:] =  colours[board_data.trackColour[idx]]     # add colour RGB code
    
    for idx in range(len(X_all)):
        plt.plot(X_all[idx],Y_all[idx],color=colour[idx,:]) # plot all the coords
        
    plt.axis("off")
    plt.savefig("colour_graph.pdf")
    plt.show()
         
    
def create_tickets(routes,graph,points,font,filename):
    '''
    Creates tickets for ticket2ride game, saves each as .png file

    Parameters
    ----------
    routes : all ticket routes
        
    graph : network x graph
    
    points : number of points for each route
    
    font : string, font file location
        
    filename : string, whether the ticket is a short or long route

    Returns
    -------
    None.

    '''
    
    # generate folder for graph routes
    filepath = filename + '_routes'
    
    try:
        os.mkdir(filepath)
    except OSError:
        print ("%s already exists" % filepath)
    else:
        print ("Created directory %s " % filepath)
    
    
    for i in range(len(routes)):
        
        fig, ax = plt.subplots(1,edgecolor='k')
        fig.set_size_inches(3.5,2.5)
        
        edges,weights = zip(*nx.get_edge_attributes(graph,'weight').items())
        
        pos = nx.get_node_attributes(graph, 'pos')
        
        # edges
        nx.draw_networkx_edges(graph, pos, node_color='b', edge_color='gray', edgelist=edges,
                               width=2)
        
        # nodes
        nx.draw_networkx_nodes(graph, pos, node_size=40, node_color='gray', ax=ax)
        
        # draw key nodes bigger
        # node 1- plot in colour
        nx.draw_networkx_nodes(graph, pos, node_size=150, nodelist = routes[i],  node_color='maroon',ax=ax)
        
        # X,Y coords for route line plotting
        X = [pos[routes[i][0]][0],pos[routes[i][1]][0]]
        Y = [pos[routes[i][0]][1],pos[routes[i][1]][1]]
        
        # add text to cards
        
        # route text
        # Points string
        points_text = "Points: " + str(int(points[i][0]))
        plt.text(20, 55, points_text,  fontproperties=font, fontsize=15)    # add points text
        
        # Add ticket name 
        route_text_1 = routes[i][0].replace("_", " ") 
        plt.text(40, -3, route_text_1.title() + " To ", ha='center', fontproperties=font,  fontsize=10)
        
        route_text_2 = routes[i][1].replace("_", " ")   
        plt.text(40, 1, route_text_2.title() ,ha='center', fontproperties=font,  fontsize=10)

        plt.axis('off')     # turn box off around map
        
        plt.plot(X,Y,color='maroon',linestyle="--",linewidth=4)     # add line between places
        
        plt.gca().invert_yaxis()
        
        plt.savefig(filepath + '/' + filename + '_' + routes[i][0] + '_' + routes[i][1] + '_graph.png')
        
        plt.show()
        
        plt.close()