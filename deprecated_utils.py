class Deprecated:
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
        return paths 
        
# 2) Remove all entries with values < 2.
    def _filterFeet(self, paths):
        filteredPaths = Counter()
        for edge in paths:
            if paths[edge] >= 2:
                filteredPaths[edge] = paths[edge]
        return filteredPaths

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

def smarterOutputOld(graph, homeOrder, allPairsLengths, homes, version=0, saturated=set()):
    if homeOrder is None or len(homeOrder) == 0:
        raise Exception("<-- CUSTOM ERROR --> Invalid smart solver output.")
    
    # 1) Create path
    path = []
    for i in range(len(homeOrder) - 1):
        path = path + nx.dijkstra_path(graph.nxG, homeOrder[i], homeOrder[i+1])[:-1]
    path = path + nx.dijkstra_path(graph.nxG, homeOrder[-1], graph.start)

    # 2) Figure out which homes we make people walk
    walking = set()
    remainingHomeSet = set(graph.houses)
    collapsed = Counter()
    s = Stack()
    for v in path:
        if s.size() < 2:
            s.push(v)
        elif s.doublePeek() == v and collapsed[s.peek()] < 1 and s.peek():
            popped = s.pop()
            if popped in remainingHomeSet:
                collapsed[s.peek()] += 1 # Collapse v into the previous vertex
                walking.add(s.peek())
        else:
            s.push(v)
    path = s.list
    pathSet = set(path)
    
    
    if len(walking) > 0 and version == 0:
        newHomes = set(graph.houses).difference(walking) #- set(graph.houses).intersection(walking)
        newGraph = graph.copy()
        newGraph.houses = list(newHomes)
        newGraph.num_houses = len(newHomes)
        return newGraph, set()

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