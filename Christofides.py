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
        self.remove_nodes = []
        self.allPairsLengths = None

    def solve(self):
        "*** YOUR CODE HERE ***"
        self.length = dict(nx.all_pairs_dijkstra_path_length(self.nxG))
        self.allPairsLengths = list(nx.all_pairs_dijkstra_path_length(self.nxG))
        self.mst = nx.minimum_spanning_tree(self.nxG)
        self.perfect_matching = self._compute_min_perfect_matching(self.mst)
        """
        print("size", self.perfect_matching.size())
        for i in self.perfect_matching.nodes:
            print(len(self.perfect_matching.__getitem__(i)), i)
        """
        self.eulerian_tour = list(nx.eulerian_circuit(self.perfect_matching))
        self.tour_list = [u for u, v in self.eulerian_tour]# + [list(self.eulerian_tour)[-1][1]]
        #print("tour list", self.tour_list)
        self.incomplete_path = self.add_back_removed_nodes(self.tour_list, self.remove_nodes)
        #print(self.incomplete_path)
        self.complete_path = self.reorganize_list(self.incomplete_path, self.graph.start)
        #print(self.complete_path)
        self.hamiltonian_path = self.create_hamiltonian_path(self.complete_path)
        #print(self.hamiltonian_path)
        #for i in range(len(self.hamiltonian_path) - 1):
            #if self.nxG.has_edge(self.hamiltonian_path[i], self.hamiltonian_path[i+1]) == False:
                #print(self.hamiltonian_path[i], self.hamiltonian_path[i+1])
        #for i in self.nxG.nodes:
            #if i not in self.hamiltonian_path:
                #print(i, "False")
        return smartOutput(self.graph, self.hamiltonian_path, self.allPairsLengths, list(self.homes))

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
        for k in mst.nodes:
            if (len(mst.__getitem__(k)) == 0):
                self.remove_nodes += [k]
        for a in self.remove_nodes:
            mst.remove_node(a)
        self.remove_nodes = []
        for b in self.remove_nodes:
            if b in self.homes:
                self.remove_nodes += [b]
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
        if list[0] == list[len(list) - 1]:
            list.pop()
        for i in range(len(list)):
            if list[i] == start:
                place = i
                break
        for i in range(place, len(list)):
            result += [list[i]]
        for i in range(place):
            result += [list[i]]
        if result[len(result) - 1] != start:
            return result + [start]
        return result

    def add_back_removed_nodes(self, path, nodes):
        path = path + [path[0]]
        nodes = np.asarray(nodes)
        path = np.asarray(path)
        # print(nodes)
        # print(path)
        for i in nodes:
            min = float("inf")
            ind = 0
            for j in range(len(path) - 1):
                total_dist = self.length[path[j]][i] + self.length[i][path[j+1]]
                if total_dist < min:
                    min = total_dist
                    ind = j
            #print("index",ind+1, "element", path[ind], "node", i)
            path = np.insert(path, ind + 1, i)
            path = np.delete(path, path.size - 1)
            #print(path)
        return path.tolist()
