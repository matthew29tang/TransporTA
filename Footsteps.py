import networkx as nx
import numpy as np
from custom_utils import *
from data_structures import *

class Footsteps:
    def __init__(self, graph):
        # Graph(len(list_of_locations), len(list_of_homes), list_of_locations, list_of_homes, starting_car_location, adjacency_matrix) 
        self.graph = graph
        self.G = self.graph.G
        self.nxG = self.graph.nxG
        self.homes = set(self.graph.houses)
        self.droppedOff = set()
        self.numDroppedOff = 0
        self.homeOrder = []
        self.allPairsLengths = list(nx.all_pairs_dijkstra_path_length(self.nxG))
        
    def solve(self, version=0):
        v = self.graph.start
        self.homeOrder.append(v)
        while self.numDroppedOff < self.graph.num_houses:
            if v in self.homes and v not in self.droppedOff:
                self.numDroppedOff += 1
                self.droppedOff.add(v)
                self.homeOrder.append(v)
            if self.numDroppedOff == self.graph.num_houses:
                break
            v = self._closestHome(v)[1]

        if version == 2:
            return self.homeOrder
        newGraph, saturated = smarterOutput(self.graph, self.homeOrder, self.allPairsLengths, list(self.homes))
        if not isinstance(newGraph, Graph):
            return newGraph, saturated
        return smarterOutput(self.graph, Footsteps(newGraph).solve(version=2), self.allPairsLengths, list(self.homes), version=2, saturated=saturated)

    # Helper: Find closest path to a home from v
    def _closestHome(self, source):
        bestHome = None
        bestHomeDist = float('inf')
        dists = self.allPairsLengths[source][1]
        for v in dists:
            if v not in self.homes or v in self.droppedOff or v == source:
                continue
            if dists[v] < bestHomeDist:
                bestHomeDist = dists[v]
                bestHome = v
        path = nx.dijkstra_path(self.nxG, source, bestHome)
        return path if bestHome is not None else None