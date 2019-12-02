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