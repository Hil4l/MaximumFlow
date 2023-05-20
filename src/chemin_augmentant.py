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

			for _ in range(V):
				self.matrix.append([0] * V)
				self.marks.append(None)
			
			while True:
				line = f.readline().strip().split()
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])

				self.matrix[i][j] += w  # sum capacities of dup edges

		self.source = source
		self.sink = sink
		self.V = V
		self.E = E
				
	def BFS(self, s, t, parent):
	
			visited = [False]*(self.V)
			visited[s] = True
			queue = []
			queue.append(s)
	
			# Standard BFS Loop
			while queue:
	
				u = queue.pop(0)
	
				for ind, val in enumerate(self.matrix[u]):
					if visited[ind] == False and val > 0:

						queue.append(ind)
						visited[ind] = True
						parent[ind] = u
						if ind == t:
							return True
	
			return False
				
		
	def FordFulkerson(self):

		parent = [-1]*(self.V)
		max_flow = 0

		source = self.source
		sink = self.sink

		while self.BFS(source, sink, parent) :

			path_flow = float("Inf")
			s = sink
			while(s !=  source):
				path_flow = min (path_flow, self.matrix[parent[s]][s])
				s = parent[s]

			max_flow +=  path_flow

			v = sink
			while(v !=  source):
				u = parent[v]
				self.matrix[u][v] -= path_flow
				self.matrix[v][u] += path_flow
				v = parent[v]

		return max_flow
	
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
	
	instance_file = "instances/inst-1500-0.3.txt"
	g = FordFulkersonSolver(instance_file)

	start_time = time.time()
	max_flow = g.FordFulkerson()
	elapsed_time = time.time() - start_time
	print(f"max flow = {max_flow} in : {elapsed_time}")

	# inst_test()
	
if __name__ == '__main__':
	main()