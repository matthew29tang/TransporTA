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
        self.path = []
        self.pathSet = set()
        self.droppedOff = set()
        self.numDroppedOff = 0
        self.traversedEdges = set()

    def solve(self):
        "*** YOUR CODE HERE ***"
        self.footPaths = self.feet()
        self.allPairsLengths = self.allPairs()
        adjList = self.graph.adjacency_list
        v = self.graph.start
        self.path.append(v)
        self.pathSet.add(v)
        i = 0
        while self.numDroppedOff < self.graph.num_houses:
            if v in self.homes and v not in self.droppedOff:
                self.numDroppedOff += 1
                self.droppedOff.add(v)
            #print('Iteration ', i, v, self.droppedOff)
            if self.numDroppedOff == self.graph.num_houses:
                break
            bestEdge = self._mostFootsteps(v, adjList)
            #print("Best edge:", bestEdge)
            if bestEdge is None or True:
                path = self._closestHome(v)
                bestEdge = (path[0], path[1])
            else: # Only add to traversedEdges if we use from footsteps
                self.traversedEdges.add(bestEdge)
            self.path.append(bestEdge[1])
            self.pathSet.add(bestEdge[1])
            v = bestEdge[1]
            i += 1
        homePath = nx.dijkstra_path(self.nxG, v, self.graph.start)
        self.path = self.path + homePath[1:]
        return smartOutput(self.graph, self.path, self.allPairsLengths, list(self.homes))

    ### Helper Functions ###
    # 1) Return a dictionary F where the keys represent the edge(u,v) and values represent the frequency they are walked on.
    def feet(self):
        shortestPaths = nx.single_source_dijkstra_path(self.nxG, self.graph.start)
        self.mst = nx.minimum_spanning_tree(self.nxG)
        shortestMSTPaths = nx.single_source_dijkstra_path(self.mst, self.graph.start)
        paths = Counter() # Special dict, initializes with 0.
        for v in shortestPaths:
            path = shortestPaths[v]
            if len(path) == 1 or v not in self.homes:
                continue
            for i in range(1, len(path)):
                paths[(path[i-1], path[i])] += 1
                #paths[(path[i], path[i-1])] += 1
        for v in shortestMSTPaths:
            path = shortestMSTPaths[v]
            if len(path) == 1 or v not in self.homes:
                continue
            for i in range(1, len(path)):
                paths[(path[i-1], path[i])] += 1
                #paths[(path[i], path[i-1])] += 1
        #print(paths)
        return paths #self._filterFeet(paths)

    # 2) Remove all entries with values < 2.
    def _filterFeet(self, paths):
        filteredPaths = Counter()
        for edge in paths:
            if paths[edge] >= 2:
                filteredPaths[edge] = paths[edge]
        return filteredPaths

    # 3) Run all-pairs shortest paths on G
    def allPairs(self):
        return list(nx.all_pairs_dijkstra_path_length(self.nxG))

    # 4-6) Greedy step + DFS
    def greedy_step(self, v):
        # for each edge of v not already in the cycle
        # run BFS depth 5, appending all home vertices you visit in a list H
        pass

    # Helper: Find edge from F that is most traversed
    def _mostFootsteps(self, v, adjList):
        bestEdge = None
        bestEdgeWeight = 0
        skip = 0
        for edge in adjList[v]:
            #print(edge, edge in self.traversedEdges)
            if max(self.footPaths[edge],self.footPaths[(edge[1], edge[0])]) > bestEdgeWeight and edge not in self.traversedEdges:
                bestEdge = edge
                bestEdgeWeight = self.footPaths[edge]
            #print(self.footPaths)
            elif self.footPaths[(v, edge)] > bestEdgeWeight:
                skip += 1
            if skip >= 1:
                return None
        return bestEdge

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
            
            
