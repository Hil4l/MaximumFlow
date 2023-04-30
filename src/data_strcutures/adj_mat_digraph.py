
class Graph:

    def __init__(self, file_name):
        self.matrix = []

        with open(file_name) as f:
            V = int(f.readline().strip().split()[1])
            source = int(f.readline().strip().split()[1])
            sink = int(f.readline().strip().split()[1])
            E = int(f.readline().strip().split()[1])

            for i in range(V):
                self.matrix.append([0] * V)
            for i in range(E):
                x, y, z = map(int, f.readline().strip().split())
                self.add_edge(x,y,z)

        self.source = source
        self.sink = sink
        self.V = V
        self.E = E

    def add_edge(self, x, y, z):
        self.matrix[x][y] = z

    def BFS(self, s, t, parent):
        """
        Returns true if there is a path from source 's' to sink 't' in residual graph. 
        Also fills parent[] to store the path
        """
        visited = [False]*(self.V)  # Mark all the vertices as not visited    
        queue = []  # BFS queue


        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # BFS Loop
        while queue:

            u = queue.pop(0)

            # Get all adjacent vertices of u
            # If not visited, then mark it visited and enqueue it
            for ind, val in enumerate(self.matrix[u]):
                if visited[ind] == False and val > 0:  # val > 0 --> flow < capacity
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    
                    if ind == t:  # path to the sink -> return true
                        return True

        # no path to the sink found -> return false
        return False
    

    def FordFulkerson(self) -> int:
 
        # filled by BFS, store the augmanting path
        parent = [-1]*(self.V)
 
        max_flow = 0 # There is no flow initially
 
        # Augment the flow while there is path from source to sink
        while self.BFS(self.source, self.sink, parent) :
 
            # Find minimum residual capacity through the path.
            path_flow = float("Inf")
            s = self.sink
            while(s !=  self.source):
                path_flow = min (path_flow, self.matrix[parent[s]][s])
                s = parent[s]
 
            # Add path flow to overall flow
            max_flow +=  path_flow
    
            # Augmanting phase
            v = self.sink
            while(v != self.source):
                u = parent[v]
                self.matrix[u][v] -= path_flow  # forward edge (flow used)
                self.matrix[v][u] += path_flow  # backward edge (reverse flow "gained")
                v = parent[v]
        
        return max_flow