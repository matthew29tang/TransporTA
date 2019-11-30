import networkx as nx
import numpy as np
import random
from custom_utils import *
from data_structures import *

class Christofides:
    def __init__(self, graph):
        # Graph(len(list_of_locations), len(list_of_homes), list_of_locations, list_of_homes, starting_car_location, adjacency_matrix)
        self.graph = graph
        self.G = self.graph.G
        self.nxG = self.graph.nxG
        self.homes = set(self.graph.houses)
        self.path = []
        self.dropoffs = {}
        self.length = 0
        self.mst = None
        self.perfect_matching = None
        self.eulerian_tour = None
        self.mst_distances = None

    def solve(self):
        "*** YOUR CODE HERE ***"
        self.length = list(nx.all_pairs_dijkstra_path_length(self.nxG))
        self.mst = nx.minimum_spanning_tree(self.nxG)
        self.perfect_matching = self._compute_min_perfect_matching(self.mst)
        self.eulerian_tour = list(nx.eulerian_circuit(self.perfect_matching))
        self.path = [u for u, v in self.eulerian_tour] + [list(self.eulerian_tour)[-1][1]]
        return smartOutput(self.graph, self.path, self.length, list(self.homes))

    ### Helper Functions ###
    def _compute_min_perfect_matching(self, mst):
        mst_distances = dict(nx.all_pairs_dijkstra_path_length(mst))
        odd_vertices = []
        for i in mst.nodes:
            if (len(mst.__getitem__(i))%2 == 1):
                odd_vertices += [i]
        random.shuffle(odd_vertices)
        while odd_vertices:
            v = odd_vertices.pop()
            length = float("inf")
            closest = 0
            for u in odd_vertices:
                if v != u and mst.has_edge(v, u) == False and mst_distances[v][u] < length:
                    length = mst_distances[v][u]
                    closest = u
            mst.add_edge(v, closest, weight=length)
            odd_vertices.remove(closest)
        return mst
