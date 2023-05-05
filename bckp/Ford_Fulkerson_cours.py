"""
error: self.matrix[i][j][0] += at (line 91)
        TypeError: 'tuple' object does not support item assignment

correction: replace tuple with assignable list : [fij, uij]
"""

class Graph:

    def __init__(self, file_name):
        self.matrix = []
        self.marks = []

        with open(file_name) as f:
            V = int(f.readline().strip().split()[1])
            source = int(f.readline().strip().split()[1])
            sink = int(f.readline().strip().split()[1])
            E = int(f.readline().strip().split()[1])

            for i in range(V):
                self.matrix.append([None] * V)
                self.marks.append(None)
            
            for i in range(E):
                x, y, z = map(int, f.readline().strip().split())
                self.matrix[x][y] = [0, z]  # (flow = 0, capacity = z)

        self.source = source
        self.sink = sink
        self.V = V
        self.E = E
        
    def marking_phase(self) -> bool:

        # Marquer s par [0, ∞]
        visited = [False]*(self.V)     
        visited[self.source] = True  
        self.marks[self.source] = [0, float('inf')]  
        
        # L = {s}
        queue = []
        queue.append(self.source)

        while queue and not visited[self.sink]:  # Tant que L ̸= ∅ et t non marqué :

            i = queue.pop(0)  # Sélectionner i dans L et le retirer de L

            # Pour tout j non marqué tel que (i, j) ∈ A et fij < uij
            for j, t in enumerate(self.matrix[i]):
                if t is None: continue  # (i,j) ∉ A
                fij, uij = t

                if not visited[j] and fij < uij:
                    # marquer j par [i, αj] avec αj = min(αi, uij − fij) et ajouter j dans L
                    ai = self.marks[i][1]
                    aj = min(ai, uij - fij)
                    self.marks[j] = [i, aj]
                    queue.append(j)
                    visited[j] = True


            # Pour tout j non marqué tel que (j, i) ∈ A et fij > 0
            mat = [row[i] for row in self.matrix]  # i column
            for j, t in enumerate(mat):
                if t is None: continue  # (j,i) ∉ A
                fij, uij = t

                if not visited[j] and fij > 0:
                    # marquer j par [i, αj] avec αj = min(αi, fji) et ajouter j dans L.
                    ai = self.marks[i][1]
                    aj = min(ai, fij)
                    self.marks[j] = [i, aj]
                    queue.append(j)
                    visited[j] = True

        # si t est non marque, Stop (plus de chemin augmentant)           
        if not visited[self.sink]:
            return False
        return True
    
    def augmenting_phase(self):
        """
        update flow along the path
        return: max flow augmenting value (αt)
        """

        at = self.marks[self.sink][1]

        j = self.sink
        while j != self.source:  # Tant que j ̸= s :
            i, aj = self.marks[j]  # ▶ Soit [i, αj] la marque de j.
            
            # Si (i, j) est en avant
            if self.matrix[i][j] is not None:
                self.matrix[i][j][0] += at # fij = fij + αt
            
            # Si (i, j) est en arrière
            else:
                self.matrix[j][i][0] -= at # fji = fji − αt .

            j = i # ▶ j = i.
        
        return at

    def FordFulkerson(self) -> int:
        F = 0  # initial flowwhile True:

        while self.marking_phase():
            at = self.augmenting_phase()
            F += at

        return F
    

"""
----------- Main -----------
"""

def main():

    instance_file = "instances/inst-100-0.1.txt"
    g = Graph(instance_file)
    print("max flow = " + str(g.FordFulkerson()))

if __name__ == '__main__':
	main()