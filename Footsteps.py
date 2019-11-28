import networkx as nx
import numpy as np
from custom_utils import *

class Footsteps:
    def __init__(self, graph):
        # Graph(len(list_of_locations), len(list_of_homes), list_of_locations, list_of_homes, starting_car_location, adjacency_matrix) 
        self.graph = graph
        self.G = self.graph.G
        self.path = None
        self.dropoffs = {}

    def solve(self):
        "*** YOUR CODE HERE ***"
        return output(G, self.path, self.dropoffs)

    ### Helper Functions ###
    # 1) Return a dictionary F where the keys represent the edge(u,v) and values represent the frequency they are walked on.
    def feet(self):
        pass

    # 2) Remove all entries with values < 2.
    def filter_feet(self, paths):
        pass

    # 3) Run all-pairs shortest paths on G
    def allPairs(self):
        pass

    # 4-6) Greedy step + DFS
    def greedy_step(self, v):
        # for each edge of v not already in the cycle
        # run BFS depth 5, appending all home vertices you visit in a list H
        pass

    # Helper: Find edge from F that is most traversed
    def _mostFootsteps(self, v):
        pass

    # Helper: Find closest home to v
    def _closestHome(self, v):
        pass
