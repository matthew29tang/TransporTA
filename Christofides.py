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
        self.hamiltonian_path = None

    def solve(self):
        "*** YOUR CODE HERE ***"
        self.length = list(nx.all_pairs_dijkstra_path_length(self.nxG))
        self.mst = nx.minimum_spanning_tree(self.nxG)
        self.perfect_matching = self._compute_min_perfect_matching(self.mst)
        """
        print("size", self.perfect_matching.size())
        for i in self.perfect_matching.nodes:
            print(len(self.perfect_matching.__getitem__(i)), i)
        """
        self.eulerian_tour = list(nx.eulerian_circuit(self.perfect_matching))
        self.tour_list = [u for u, v in self.eulerian_tour]# + [list(self.eulerian_tour)[-1][1]]
        self.path = self.reorganize_list(self.tour_list, self.graph.start)
        self.hamiltonian_path = self.create_hamiltonian_path(self.path)
        return smartOutput(self.graph, self.hamiltonian_path, self.length, list(self.homes))

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
            closest = -1
            for u in odd_vertices:
                if v != u and mst.has_edge(v, u) == False and mst_distances[v][u] < length:
                    length = mst_distances[v][u]
                    closest = u
            if closest == -1:
                for s in odd_vertices:
                    if v != s and mst_distances[v][s] < length:
                        length = mst_distances[v][s]
                        closest = s
            if mst.has_edge(v, closest) == False:
                mst.add_edge(v, closest, weight=length)
            odd_vertices.remove(closest)
        remove_edges = {}
        nodes = []
        for i in mst.nodes:
            for j in mst.nodes:
                if i != j and (len(mst.__getitem__(i))%2 == 1) and (len(mst.__getitem__(j))%2 == 1) and mst.has_edge(i, j) and j not in remove_edges:
                    remove_edges[i] = j
        for key in remove_edges:
            mst.remove_edge(key, remove_edges[key])
        remove_nodes = []
        for k in mst.nodes:
            if (len(mst.__getitem__(k)) == 0):
                remove_nodes += [k]
        for a in remove_nodes:
            mst.remove_node(a)
        return mst

    def create_hamiltonian_path(self, path):
        result = np.asarray(path)
        start_indices = []
        buffer = 0
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i+1]
            if (self.nxG.has_edge(start, end) == False):
                list = nx.dijkstra_path(self.nxG,start,end)
                li = list[1: len(list) - 1]
                li_array = np.asarray(li)
                result = np.insert(result, i+buffer+1, li_array)
                buffer += len(li)
        return result.tolist()

    def reorganize_list(self, list, start):
        place = 0
        result = []
        for i in range(len(list)):
            if list[i] == start:
                place = i
                break
        for i in range(place, len(list)):
            result += [list[i]]
        for i in range(place):
            result += [list[i]]
        return result + [start]
