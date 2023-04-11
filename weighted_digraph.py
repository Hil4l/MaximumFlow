class Graph:
    def __init__(self):
        self.E = 0  # number of edges
        self.V = 0  # number of vertices
        self.nodes = set()
        self.out_edges = {}
        self.inc_edges = {}

    def add_vertice(self, u):
        if u not in self.nodes:
            self.nodes.add(u)
            self.out_edges[u] = []
            self.inc_edges[u] = []
            self.V += 1

    def add_edge(self, u: int, v: int, w: int) -> None:
        self.add_vertice(u)
        self.add_vertice(v)
        
        # ignore self loop (because cancel itself in constraints)
        if u != v:
            self.out_edges[u].append((v, w))
            self.inc_edges[v].append((u, w))
        
        self.E += 1
    
    def get_out_edges(self, u: int) -> list[int]:
        return self.out_edges[u]
    
    def get_inc_edges(self, u: int):
        return self.inc_edges[u]