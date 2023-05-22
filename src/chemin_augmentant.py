""" 
--------------------------------------------------------------------------------------------
Author: Hilal Rachik / Nadim Rachik

Parametre: instance file "inst-n-p.txt"
Generates: Max flow solution "model-n-p.path"
-------------------------------------------------------------------------------------------- 
""" 

from collections import deque
import sys
import copy

class FordFulkersonSolver:

	def __init__(self, file_name:str):
		
		with open(file_name) as f:
			V = int(f.readline().strip().split()[1])
			source = int(f.readline().strip().split()[1])
			sink = int(f.readline().strip().split()[1])
			E = int(f.readline().strip().split()[1])

			self.graph = {u: {} for u in range(V)}
			self.min_cut = set()  # minimum cut set
			
			while True:
				line = f.readline().strip().split()
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])

				self.graph[i][j] = w  # save last capacity
		
		self.original_capacities = copy.deepcopy(self.graph)

		self.source = source
		self.sink = sink
		self.V = V
		self.E = E

	def _bfs(self, parent):
	
			visited = {self.source}
			queue = deque([self.source])
			
			# Standard BFS Loop
			while queue:
				u = queue.popleft()
				for v, w in self.graph[u].items():

					if v not in visited and w > 0:  # (w > o) -> only edges with flow available

						queue.append(v)
						visited.add(v)
						parent[v] = u
						if v == self.sink:
							return True

			# no more augmanting path (t not marked)
			self.min_cut = visited  # save last iteration marked nodes (min cut)
			return False
				
		
	def _ford_fulkerson(self):

		parent = [-1]*(self.V)
		max_flow = 0

		while self._bfs(parent):  # while there is augmenting path
			
			# find maximal maximal flow alomg path
			path_flow = float("Inf")
			s = self.sink
			while(s !=  self.source):
				path_flow = min (path_flow, self.graph[parent[s]][s])
				s = parent[s]

			max_flow +=  path_flow  # add path flow to overall flow

			# update residual graph
			v = self.sink
			while(v !=  self.source):
				u = parent[v]
				self.graph[u][v] -= path_flow
				v = parent[v]

		return max_flow
	
	def min_cut_value(self) -> int:
		cut_value = 0
		for u in self.min_cut:
			capacity_sum = 0
			for v, w in self.original_capacities[u].items():
				if v in self.min_cut: continue  # not cross edge
				capacity_sum += w  # capacity

			cut_value += capacity_sum
		
		return cut_value
	
	def write_sol(self, flow, min_cut_val, edge_flows):
		p = self.E / (self.V ** 2)
		sol_file = "model-{}-{:.1f}.path".format(self.V, p)

		with open(sol_file, "w") as f:
			f.write(f"Max flow = {flow}\n")
			f.write(f"Min cut value = {min_cut_val}\n")

			for i, edges in edge_flows.items():
				for j, fij in edges.items():
					if(fij > 0):
						f.write(f"edge ({i}, {j}): {fij}\n")

	def compute(self):
		flow = self._ford_fulkerson()
		min_cut_val = self.min_cut_value()	
		edge_flows = {u: {v: self.original_capacities[u][v] - self.graph[u][v] for v in edges.keys()} for u, edges in self.graph.items()}  # original capacities - end available capacity = flow
		self.write_sol(flow, min_cut_val, edge_flows)

"""
----------- Main ----------------------------------
"""

def main():
	if len(sys.argv) != 2:
		print("Usage: python chemin_augmentant.py instance.txt")
		sys.exit(1)

	instance_file = sys.argv[1]
	g = FordFulkersonSolver(instance_file)
	g.compute()

if __name__ == '__main__':
	main()