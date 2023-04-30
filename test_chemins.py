
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

    def marking_phase(self):
        visited = [False]*(self.V)     
        queue = []

        queue.append((self.sink, float("inf")))  # Marquer s par [0, ∞], L = {s}
        visited[self.source] = True  

        while queue and visited[self.sink]:  # Tant que L ̸= ∅ et t non marqué :

            node = queue.pop(0)  # Sélectionner i dans L et le retirer de L
            i = node[0]
            ai = node[1]

            # Pour tout j non marqué tel que (i, j) ∈ A et fij < uij
                # , marquer j par [i, αj] avec αj = min(αi, uij − fij) et ajouter j dans L.

            # Pour tout j non marqué tel que (j, i) ∈ A et fij > 0
                # , marquer j par [i, αj] avec αj = min(αi, fji) et ajouter j dans L.


        # si t est non marque, Stop (plus de chemin augmentant)           
        if not visited[self.sink]:
            return False
        return True
    
    def augmenting_phase(self):
        pass
    
        #j = t.
        
        # Tant que j ̸= s :
            # ▶ Soit [i, αj] la marque de j.
            # Si (i, j) est en avant, fij = fij + αt .
            # Si (i, j) est en arrière, fji = fji − αt .
            # ▶ j = i.

    def FordFulkerson(self) -> int:
        F = 0  # initial flowwhile True:

        s = self.source
        t = self.sink
        L = [(0,0) * self.V]  # (parent, flow)

        while True:
            break

        return F