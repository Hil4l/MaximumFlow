""" 
--------------------------------------------------------------------------------------------
Author: Hilal Rachik 520550

Parametre (command line): instance file "inst-n-p.txt"
Generates: CPLEX LP linear program of this instance saved in a file "model-n-p.lp"
Exemple: python3 generate_model.py "inst-300-0.3.txt"  --> generates "model-300-0.3.lp"
-------------------------------------------------------------------------------------------- 
""" 

class Graph:
	def __init__(self):
		self.nodes = set()
		self.out_edges = {}
		self.inc_edges = {}

	def add_vertice(self, u):
		if u not in self.nodes:
			self.nodes.add(u)
			self.out_edges[u] = []
			self.inc_edges[u] = []

	def add_edge(self, u: int, v: int, w: int) -> None:
		self.add_vertice(u)
		self.add_vertice(v)
		
		# ignore self loop (cancel itself in constraints) and duplicate edges
		if u != v and not self.is_dup_edge(u,v): 
			self.out_edges[u].append((v, w))
			self.inc_edges[v].append((u, w))
	
	def get_out_edges(self, u: int):
		return self.out_edges[u]
	
	def get_inc_edges(self, u: int):
		return self.inc_edges[u]
	
	def is_dup_edge(self, u: int, v: int) -> bool:
		# return true if an edge (u,v) already exists
		return any(x[0] == v for x in self.out_edges[u])
		
	

# ----------------------------------------------------------------

class LPModelGenerator:

	def __init__(self, instance_file:str):
		self.instance_file = instance_file
		self.capacity_cnt = []
		self.conserv_cnt = []
		self.graph = Graph()

	# Graph from instance file
	def parseInstanceFile(self) -> None:
		with open(self.instance_file, 'r') as in_file:
			V = int(in_file.readline().strip().split()[1])
			source = int(in_file.readline().strip().split()[1])
			sink = int(in_file.readline().strip().split()[1])
			E = int(in_file.readline().strip().split()[1])

			# edges
			while True:
				line = in_file.readline().strip().split()  # ['a', 'b', 'c']
				if not line: break

				i, j, w = int(line[0]), int(line[1]), int(line[2])
				self.graph.add_edge(i,j,w)
		
		self.source = source
		self.sink = sink
		self.E = E
		self.V = V

	# Model name
	def modelName(self) -> str:
		p = self.E / (self.V ** 2)
		model_name = "model-{}-{:.1f}.lp".format(self.V, p)
		return model_name

	def genCapacityConstr(self) -> None:
		"""
		Capacity constraints: edge flow <= edge capacity
		x_i_j <= capacity
		"""

		for i in self.graph.nodes:
			for ou_edge in self.graph.get_out_edges(i):
				j = ou_edge[0]
				w = ou_edge[1]
				constr = "x_{}_{} <= {}".format(i, j, w)  
				self.capacity_cnt.append(constr)

	def genConservConstr(self) -> None:
		
		for i in self.graph.nodes:
			constr = ""
			for ou_edge in self.graph.get_out_edges(i):
				j = ou_edge[0]
				constr += "x_{}_{} + ".format(i,j)

			# reformat string
			constr = constr[:-2]

			for in_edge in self.graph.get_inc_edges(i):
				j = in_edge[0]
				constr += "- x_{}_{} ".format(j,i)

			# reformat string
			if i == self.source:
				constr += "- v_0 = 0"
			elif i == self.sink:
				constr += "+ v_0 = 0"
			else:
				constr += "= 0"

			# save node i constraints
			self.conserv_cnt.append(constr)

	def genModelFile(self) -> None:
		with open(self.modelName(), "w") as f:
			f.write("Maximize\n")
			f.write("\t obj: v_0\n")
			f.write("Subject To\n")
			for c in self.capacity_cnt:
				f.write("\t" + c + "\n")
			for c in self.conserv_cnt:
				f.write("\t" + c + "\n")
			f.write("End")

	def createModel(self) -> None:
		self.parseInstanceFile()
		print("File parsed")

		self.genCapacityConstr()
		self.genConservConstr()
		print("Constraints generated")
		
		self.genModelFile()
		print("Model file generated")


"""
----------- Main -----------
"""

def main():
	# TODO: command line parametre !!!!!

	instance_file = "instances/inst-700-0.3.txt"
	g = LPModelGenerator(instance_file)
	g.createModel()


if __name__ == '__main__':
	main()