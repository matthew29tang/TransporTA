import networkx as nx
import numpy as np
from custom_utils import *

class Christofides:
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