import student_utils as su

class Graph:
    def __init__(self, data):
        # [number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix]
        self.num_locations = data[0]
        self.num_houses = data[1]
        self.locations = data[2]
        self.houses = data[3]
        self.start = data[4]
        self.G = data[5]
    
    def edge_list(self):
        return su.adjacency_matrix_to_edge_list(self.G)
    
    def cost(self, car_cycle, dropoff_mapping):
        return su.cost_of_solution(self.G, car_cycle, dropoff_mapping)

    def __str__(self):
        data = [self.num_locations, self.num_houses, self.locations, self.houses, self.start]
        return "\n".join([str(d) for d in data])

def output(self, G, path, dropoffs):
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
