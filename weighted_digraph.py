class Graph:
    def __init__(self):
        self.E = 0  # number of edges
        self.V = 0  # number of vertices
        self.nodes = set()
        self.edges = {}
    
    def add_vertice(self, u):
        if u not in self.nodes:
            self.nodes.add(u)
            self.edges[u] = []
            self.V += 1

    def add_edge(self, u: int, v: int, w: int) -> None:
        self.add_vertice(u)
        self.add_vertice(v)
        
        self.edges[u].append((v, w))
        self.E += 1
    
    def out_edges(self, u):
        return self.edges[u]