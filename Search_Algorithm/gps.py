#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2
Morgan Conner, University of Mary Washington, fall 2021
'''

from atlas import Atlas
import numpy as np
import logging
import sys
import math


def find_best_path(atlas):
    '''Finds the best path from src to dest, based on costs from atlas.
    Returns a tuple of two elements. The first is a list of city numbers,
    starting with 0 and ending with atlas.num_cities-1, that gives the
    optimal path between those two cities. The second is the total cost
    of that path.'''

    num_of_cities = atlas.get_num_cities()-1
    goal_state = num_of_cities
    #logging.info("Goal state is {}".format(goal_state))
    curr_node = 0
    total_cost = 0
    path_cost = 0
    frontier = []
    local_path = []
    local_path.append(0)
    nodes_expanded = []
    possible_goal_path = []

    #Add staring state
    frontier = [(local_path, path_cost)]

    while len(frontier) > 0:
        path_till_now, path_cost_till_now = frontier.pop(0)

        curr_node = path_till_now[-1]
        
        #goal state shouldn't be expanded
        if curr_node == goal_state:
            break
        
        #updates expanded nodes list
        atlas._nodes_expanded.add(curr_node)
        nodes_expanded.append(curr_node)
        
        next_node = 1
        neighbors = []
        #gets neighbors of curr_node
        for u in range(num_of_cities): 
            value = float(atlas._adj_mat[curr_node, next_node])
            if value == 0.0:
                value = math.inf
            elif value < sys.maxsize:
                if next_node not in path_till_now:
                    neighbors.extend([(next_node, value)])
            next_node += 1
        
        #adds neighbors to frontier
        for n in neighbors:
            path_to_neigh = []
            for i in path_till_now:
                path_to_neigh.append(i)
            path_to_neigh.append(n[0])
            neigh_cost = n[-1] + path_cost_till_now
            
            new_element = (path_to_neigh, neigh_cost)
            if (n not in atlas._nodes_expanded) and n not in frontier:
                frontier.append(new_element)

        #sort to find frontier path with lowest path cost
        frontier.sort(key = lambda x: x[1])

        #check if I hit goal state
        for f in frontier:
            if goal_state in f[0]:
                possible_goal_path.append(f)
        
        next_node = frontier[0][0][-1] 

        #updates total path cost
        if frontier[0][0][-2] in atlas._nodes_expanded:
            total_cost = frontier[0][-1]
        else:
            path_cost = atlas.get_road_dist(frontier[0][0][-2], next_node)
            total_cost = path_cost_till_now + path_cost
        #logging.debug("expanded nodes so far... {}".format(len(atlas._nodes_expanded)))


    #"set" of all possible goal paths
    final_goal_path = []
    for f in possible_goal_path:
        if f not in final_goal_path:
            final_goal_path.append(f)

    #sorts for optimal solution
    final_goal_path.sort(key = lambda x: x[1])
    #logging.debug("All final_goal_path {}\n".format(final_goal_path))

    
    #setting final total cost and nodes
    total_cost = final_goal_path[0][-1]
    nodes_expanded = final_goal_path[0][0]
    
    return (nodes_expanded,total_cost)
    


if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
        print("Usage: gps.py numCities|atlasFile [debugLevel].")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] not in ['DEBUG','INFO','WARNING','ERROR']:
            print('Debug level must be one of: DEBUG, INFO, WARNING, ERROR.')
            sys.exit(2)
        logging.getLogger().setLevel(sys.argv[2])
    else:
        logging.getLogger().setLevel('INFO')

    try:
        num_cities = int(sys.argv[1])
        logging.info('Building random atlas with {} cities...'.format(
            num_cities))
        usa = Atlas(num_cities)
        logging.info('...built.')
    except:
        logging.info('Loading atlas from file {}...'.format(sys.argv[1]))
        usa = Atlas.from_filename(sys.argv[1])
        logging.info('...loaded.')

    path, cost = find_best_path(usa)
    print('Best path from {} to {} costs {}: {}.'.format(0,
        usa.get_num_cities()-1, cost, path))
    print('You expanded {} nodes: {}'.format(len(usa._nodes_expanded),
        usa._nodes_expanded))

