import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import student_utils as su
from data_structures import *

SMART = True

class Graph:
    def __init__(self, data):
        # [number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix]
        if data is None:
            return
        self.num_locations = data[0]
        self.num_houses = data[1]
        self.locations = data[2]
        self.houses = su.convert_locations_to_indices(data[3], self.locations)
        self.start = self.index(data[4])
        self.G = data[5]
        self.edge_list = self._edgeList()
        self.adjacency_list = self._adjacencyList()
        nparray = np.matrix(data[5])
        nparray[nparray == 'x'] = 0.0
        self.nxG = nx.from_numpy_matrix(nparray.astype(float))
        #self.visualize()

    def copy(self):
        g = Graph(None)
        g.num_locations = self.num_locations
        g.num_houses = self.num_houses
        g.locations = self.locations
        g.houses = self.houses
        g.start = self.start
        g.G = self.G
        g.edge_list = self.edge_list
        g.adjacency_list = self.adjacency_list
        g.nxG = self.nxG
        return g

    def visualize(self):
        nx.draw(self.nxG, with_labels=True, layout=nx.spiral_layout(self.nxG, scale=4))
        #nx.spiral_layout(self.nxG)
        plt.show()

    def cost(self, car_cycle, dropoff_mapping):
        return su.cost_of_solution(self.G, car_cycle, dropoff_mapping)

    def index(self, vertex):
        return self.locations.index(vertex)

    def _edgeList(self):
        adjacency_matrix = self.G
        edge_list = []
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix[0])):
                if adjacency_matrix[i][j] != 'x':
                    edge_list.append((i, j))
        return edge_list

    def _adjacencyList(self):
        adjacency_matrix = self.G
        adjacencyList = []
        for i in range(len(adjacency_matrix)):
            temp = []
            for j in range(len(adjacency_matrix[0])):
                if adjacency_matrix[i][j] != 'x':
                    temp.append((i, j))
            adjacencyList.append(temp)
        return adjacencyList

    def __str__(self):
        data = [self.num_locations, self.num_houses, self.locations, self.houses, self.start]
        return "\n".join([str(d) for d in data])

def output(G, path, dropoffs):
    if path is None or len(dropoffs) == 0:
        raise Exception("<-- CUSTOM ERROR --> Invalid solver output.")
    indexPath = su.convert_locations_to_indices(path, G.locations)
    indexDropoffs = {}
    for key in dropoffs:
        k = G.locations.index(k) if k in G.locations else None
        v = G.locations.index(dropoffs[k]) if dropoffs[k] in G.locations else None
        if k is None or v is None:
            raise Exception("<-- CUSTOM ERROR --> Invalid location in output.")
        indexDropoffs[k] = v
    return indexPath, indexDropoffs

def smartOutput(G, path, allPairsLengths, homes):
    if path is None or len(path) == 0:
        raise Exception("<-- CUSTOM ERROR --> Invalid smart solver output.")

    if SMART:
        remainingHomeSet = set(G.houses)
        collapsed = Counter()
        s = Stack()
        for v in path:
            if s.size() < 2:
                s.push(v)
            elif s.doublePeek() == v and collapsed[s.peek()] < 1:
                popped = s.pop()
                if popped in remainingHomeSet:
                    collapsed[s.peek()] += 1 # Collapse v into the previous vertex
            else:
                s.push(v)
        path = s.list
    pathSet = set(path)
    #print("Final path:", path)
    dropoffs = {}
    for h in homes:
        if h in pathSet:
            _dictAdd(dropoffs, h, h)
            continue
        bestHome = None
        bestHomeDist = float('inf')
        shortestPaths = allPairsLengths[h][1]
        for v in shortestPaths:
            if shortestPaths[v] < bestHomeDist and v in pathSet:
                bestHome = v
                bestHomeDist = shortestPaths[v]
        _dictAdd(dropoffs, bestHome, h) # Drop off person who lives at h at closest vertex on path
    return path, dropoffs

def smarterOutput(graph, homeOrder, allPairsLengths, homes, version=0, saturated=None):
    if saturated is None:
        saturated = set()
    if homeOrder is None or len(homeOrder) == 0:
        raise Exception("<-- CUSTOM ERROR --> Invalid smart solver output.")
    
    # 1) Create path
    path = []
    for i in range(len(homeOrder) - 1):
        path = path + nx.dijkstra_path(graph.nxG, homeOrder[i], homeOrder[i+1])[:-1]
    path = path + nx.dijkstra_path(graph.nxG, homeOrder[-1], graph.start)

    #print(path, saturated)

    newTargets = set()
    # 2) Figure out which homes we make people walk
    remainingHomeSet = set(graph.houses)
    collapsed = Counter()
    s = Stack()
    for v in path:
        if s.size() < 2:
            s.push(v)
        elif s.doublePeek() == v and collapsed[s.peek()] < 1 and s.peek() not in saturated:
            popped = s.pop()
            if popped in remainingHomeSet:
                collapsed[s.peek()] += 1 # Collapse v into the previous vertex
                saturated.add(s.peek())
        else:
            s.push(v)
    path = s.list
    pathSet = set(path)
    
    walking = set()
    dropoffs = {}
    for h in homes:
        if h in pathSet:
            _dictAdd(dropoffs, h, h)
            continue
        walking.add(h)
        bestHome = None
        bestHomeDist = float('inf')
        shortestPaths = allPairsLengths[h][1]
        for v in shortestPaths:
            if shortestPaths[v] < bestHomeDist and v in pathSet:
                bestHome = v
                bestHomeDist = shortestPaths[v] 
        _dictAdd(dropoffs, bestHome, h) # Drop off person who lives at h at closest vertex on path

    #print(path, saturated, walking)

    if len(walking) > 0 and version == 0:
        newHomes = set(graph.houses).difference(walking).union(saturated)
        newGraph = graph.copy()
        newGraph.houses = list(newHomes)
        newGraph.num_houses = len(newHomes)
        return newGraph, saturated
        
    return path, dropoffs

def baselineOutput(graph):
    path = [graph.start]
    dropoffs = {}
    dropoffs[graph.start] = graph.houses
    return path, dropoffs

def _dictAdd(d, key, value):
    if d.get(key) is None:
        d[key] = [value]
    else:
        d[key].append(value)
