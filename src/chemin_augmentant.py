"""
error: self.matrix[i][j][0] += at (line 91)
        TypeError: 'tuple' object does not support item assignment

correction: replace tuple with assignable list : [fij, uij]
"""

class FordFulkersonSolver:

    def __init__(self, file_name:str):
        self.matrix = []  # adj matrix graph
        self.marks = []  # list of the graph's nodes (parent node, alpha)
        self.min_cut = []  # list of the minimum cut nodes

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
        
    def inc_edges(self, i):
        res = [row[i] for row in self.matrix]  # i column
        return res
    
    def out_edges(self, i):
        res = self.matrix[i]
        return res

    def marking_phase(self) -> bool:
        """
        marking phase
        return: boolean indicating if are no more aumenting paths
        """

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
            for j, t in enumerate(self.out_edges(i)):
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
            for j, t in enumerate(self.inc_edges(i)):  # TODO: enumerate(x for x in inc_edges if x not None)
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
            self.min_cut = [i for i, v in enumerate(visited) if v]  # save last iterations marked nodes (min cut)
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

    def ford_fulkerson(self) -> int:
        F = 0  # initial flowwhile True:

        while self.marking_phase():
            at = self.augmenting_phase()
            F += at

        return F
    
    def min_cut_value(self) -> int:
        cut_value = 0
        for i in self.min_cut:
            capacity_sum = 0
            for j, t in enumerate(self.out_edges(i)):
                if t is None: continue  # (j,i) ∉ A
                if j in self.min_cut: continue  # backward edge

                uij = t[1]
                capacity_sum += uij  # capacity

            cut_value += capacity_sum
        
        return cut_value

    def write_sol(self):
        p = self.E / (self.V ** 2)
        sol_file = "model-{}-{:.1f}.path".format(self.V, p)
        sol = self.ford_fulkerson()

        with open(sol_file, "w") as f:
            f.write(f"Max flow = {sol}\n")

            for i in range(self.V):
                for j in range(self.V):
                    t = self.matrix[i][j]
                    if t is None: continue

                    fij, uij = t
                    f.write(f"edge ({i},{j}): {fij}/{uij}\n")

"""
----------- Main -----------
"""

def main():
    # TODO: command line parametre !!!!!

    instance_file = "instances/inst-100-0.1.txt"
    g = FordFulkersonSolver(instance_file)
    # g.write_sol()
    
    print("(F&F) max flow = " + str(g.ford_fulkerson()))
    print("(min cut) max flow = " + str(g.min_cut_value()))

if __name__ == '__main__':
	main()