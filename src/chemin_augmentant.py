class FordFulkersonSolver:

	def __init__(self, file_name:str):
		

		with open(file_name) as f:
			V = int(f.readline().strip().split()[1])
			source = int(f.readline().strip().split()[1])
			sink = int(f.readline().strip().split()[1])
			E = int(f.readline().strip().split()[1])

			
			self.matrix = [[[0, 0] for _ in range(V)] for _ in range(V)]  # adj matrix graph (fij, uij)
			self.min_cut = []  # list of the minimum cut nodes

			while True:
				line = f.readline().strip().split()
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])

				self.matrix[i][j][0] += w  # sum capacities of dup edges
				self.matrix[i][j][1] += w  # sum capacities of dup edges

		self.source = source
		self.sink = sink
		self.V = V
		self.E = E
				
	def BFS(self, parent):
	
			visited = [False]*(self.V)
			visited[self.source] = True
			queue = []
			queue.append(self.source)
	
			# Standard BFS Loop
			while queue:
	
				u = queue.pop(0)
	
				for ind, e in enumerate(self.matrix[u]):

					if not visited[ind] and e[0] > 0:

						queue.append(ind)
						visited[ind] = True
						parent[ind] = u
						if ind == self.sink:
							return True

			# no more augmanting path (t not marked)
			self.min_cut = [i for i, v in enumerate(visited) if v]  # save last iteration marked nodes (min cut)
			return False
				
		
	def FordFulkerson(self):

		parent = [-1]*(self.V)
		max_flow = 0

		while self.BFS(parent) :

			path_flow = float("Inf")
			s = self.sink
			while(s !=  self.source):
				path_flow = min (path_flow, self.matrix[parent[s]][s][0])
				s = parent[s]

			max_flow +=  path_flow

			v = self.sink
			while(v !=  self.source):
				u = parent[v]
				self.matrix[u][v][0] -= path_flow
				self.matrix[v][u][0] += path_flow
				v = parent[v]

		return max_flow
	
	def min_cut_value(self) -> int:
		cut_value = 0
		for i in self.min_cut:
			capacity_sum = 0
			for j, e in enumerate(self.matrix[i]):
				uij = e[1]
				if j in self.min_cut: continue  # not cross edge
				capacity_sum += uij  # capacity

			cut_value += capacity_sum
		
		return cut_value
	
def inst_test():
	import time
	
	n_max = 15
	for n in range(1,n_max+1, 2):
		for p in range(1,4):
			
			inst = f"instances/inst-{n}00-0.{p}.txt"
			
			print("inst = " + inst + "-----------------------")
			
			# graph parse -------------------------
			g = FordFulkersonSolver(inst)

			# solving -----------------------------
			start_time = time.time()	
			max_flow = g.FordFulkerson()
			elapsed_time = time.time() - start_time
			print(f"max flow = {max_flow} in : {elapsed_time:.4f}")
			

def main():
	import time
	
	instance_file = "instances/inst-1300-0.2.txt"
	g = FordFulkersonSolver(instance_file)

	start_time = time.time()
	max_flow = g.FordFulkerson()
	elapsed_time = time.time() - start_time
	print(f"max flow = {max_flow} / min cut = {g.min_cut_value()}, in : {elapsed_time:.4f}")

	# inst_test()
	
if __name__ == '__main__':
	main()