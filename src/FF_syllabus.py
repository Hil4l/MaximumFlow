"""
error: self.matrix[i][j][0] += at (line 91)
		TypeError: 'tuple' object does not support item assignment

correction: replace tuple with assignable list : [fij, uij]
"""
from collections import defaultdict

class FordFulkersonSolver:

	def __init__(self, file_name:str):
		self.marks = []  # list of the graph's nodes (parent node, alpha)
		self.min_cut = []  # list of the minimum cut nodes
		
		# graph
		self.out_edges = defaultdict(list)  # outgoing edges
		self.inc_edges = defaultdict(list)  # incoming edges

		with open(file_name) as f:
			V = int(f.readline().strip().split()[1])
			source = int(f.readline().strip().split()[1])
			sink = int(f.readline().strip().split()[1])
			E = int(f.readline().strip().split()[1])
			
			self.flow = [[0] * V for _ in range(V)]

			while True:
				line = f.readline().strip().split()
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])
				
				if not self.dup_edge(i, j, w):  # not dup edge
					self.out_edges[i].append([j, w])  # (node, capacity)
					self.inc_edges[j].append([i, w])

		self.source = source
		self.sink = sink
		self.V = V
		self.E = E

	def dup_edge(self, i, j, w):
		"""
		returns true and sum capacities if edge (i,j) already exists
		"""
		if i not in self.out_edges:
			return False
		
		for t in self.out_edges[i]:
			if t[0] == j:
				t[1] += w  # if dup edge -> sum capacities
				return True
		return False

	def marking_phase(self) -> bool:
		"""
		marking phase
		return: boolean indicating if are no more aumenting paths
		"""

		# Marquer s par [0, ∞]
		visited = [False]*(self.V)     
		visited[self.source] = True

		self.marks = [None] * self.V
		self.marks[self.source] = [0, float('inf')]  # (parent node, α, way)
		
		# L = {s}
		queue = []
		queue.append(self.source)

		while queue and not visited[self.sink]:  # Tant que L ̸= ∅ et t non marqué :

			i = queue.pop(0)  # Sélectionner i dans L et le retirer de L

			# Pour tout j non marqué tel que (i, j) ∈ A et fij < uij
			for j, uij in self.out_edges[i]:
				fij = self.flow[i][j]

				if not visited[j] and fij < uij:

					# marquer j par [i, αj] avec αj = min(αi, uij − fij) et ajouter j dans L
					ai = self.marks[i][1]
					aj = min(ai, uij - fij)
					self.marks[j] = [i, aj, True]
					visited[j] = True

					queue.append(j)

			# Pour tout j non marqué tel que (j, i) ∈ A et fji > 0
			for j, uji in self.inc_edges[i]:
				fji = self.flow[j][i]
				if not visited[j] and fji > 0:

					# marquer j par [i, αj] avec αj = min(αi, fji) et ajouter j dans L.
					ai = self.marks[i][1]
					aj = min(ai, fji)
					self.marks[j] = [i, aj, False]
					visited[j] = True

					queue.append(j)

		# si t est non marque, Stop (plus de chemin augmentant)           
		if not visited[self.sink]:
			self.min_cut = [i for i, v in enumerate(visited) if v]  # save last iteration marked nodes (min cut)
			return False
		return True
	
	def augmenting_phase(self) -> int:
		"""
		update flow along the path
		return: max flow augmenting value (αt)
		"""

		at = self.marks[self.sink][1]

		j = self.sink
		while j != self.source:  # Tant que j ̸= s :
			i, aj, way = self.marks[j]  # ▶ Soit [i, αj] la marque de j.
			
			# Si (i, j) est en avant: # fij = fij + αt
			if way:
				self.flow[i][j] += at

			# Si (i, j) est en arrière: # fji = fji − αt
			else:
				self.flow[j][i] -= at
				
			j = i # ▶ j = i.
		
		return at

	def ford_fulkerson(self) -> int:
		F = 0  # initial flow

		while self.marking_phase():
			at = self.augmenting_phase()
			F += at

		return F
	
	def min_cut_value(self) -> int:
		cut_value = 0
		for i in self.min_cut:
			capacity_sum = 0
			for j, uij in self.out_edges[i]:
				if j in self.min_cut: continue  # not cross edge
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
				for j, uij in self.out_edges[i]:
					fij = self.flow[i][j]
					f.write(f"edge ({i}, {j}): {fij}/{uij}\n")


"""
----------- Main -----------
"""

def inst_test():
	import time
	n_max = 13
	for n in range(5,n_max+1,2):
		for p in range(1,4):
			inst = f"instances/inst-{n}00-0.{p}.txt"
			
			g = FordFulkersonSolver(inst)
			
			start_time = time.time()	
			max_flow = g.ford_fulkerson()
			elapsed_time = time.time() - start_time
			print(f"inst {n}-{p}: F = {max_flow} in : {elapsed_time:.4f}")
			print("--------------------------------")


def main():
	# TODO: command line parametre !!!!!

	instance_file = "instances/inst-1300-0.2.txt"
	g = FordFulkersonSolver(instance_file)

	
	import time
	start_time = time.time()	
	max_flow = g.ford_fulkerson()
	elapsed_time = time.time() - start_time
	print(f"max flow = {max_flow} / min cut = {g.min_cut_value()}, in : {elapsed_time:.4f}")
	# g.write_sol()

	
if __name__ == '__main__':
	main()