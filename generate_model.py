""" 
--------------------------------------------------------------------------------------------
Author: Hilal Rachik 520550

Parametre (command line): instance file "inst-n-p.txt"
Generates: CPLEX LP linear program of this instance saved in a file "model-n-p.lp"
Exemple: python3 generate_model.py "inst-300-0.3.txt"  --> generates "model-300-0.3.lp"
-------------------------------------------------------------------------------------------- 
""" 

from docplex.mp.model import Model
from weighted_digraph import Graph

class LPModelGenerator:

	def __init__(self, instance_file):
		self.instance_file = instance_file
		self.source = None
		self.sink = None
		self.capacity_cnt = []
		self.conserv_cnt = []
		self.objective = ""
		self.graph = Graph()

	# Graph from instance file
	def parseInstanceFile(self):
		with open(self.instance_file, 'r') as in_file:
			V = int(in_file.readline().strip().split()[1])
			self.source = int(in_file.readline().strip().split()[1])
			self.sink = int(in_file.readline().strip().split()[1])
			E = int(in_file.readline().strip().split()[1])

			# edges
			while True:
				line = in_file.readline().strip().split()  # ['a', 'b', 'c']
				if not line: break

				i, j, w = int(line[0]), int(line[1]), int(line[2])
				self.graph.add_edge(i,j,w)

				# Capacity constraints: x_i_j <= weight
				constr = "x_{}_{} <= {}".format(i, j, w)  
				self.capacity_cnt.append(constr)
			
			# logical solution edge
			self.graph.add_edge(self.sink, self.source, float('inf'))


	# Model name
	def modelName(self) -> str:
		p = self.graph.E / (self.graph.V ** 2)
		model_name = "model-{}-{:.1f}.lp".format(self.graph.V, p)
		return model_name

	def genConservConstr(self):
		# Conservation constraints: sum(inc edges) = sum(out edges)
		# sum(x_j_i) Vj = sum(x_i_k) Vk

		for i in self.graph.nodes:
			constr = ""
			for in_edge in self.graph.get_inc_edges(i):
				j = in_edge[0]
				constr += "x_{}_{} + ".format(j,i)

			# reformat string
			constr = constr[:-2]

			for ou_edge in self.graph.get_out_edges(i):
				k = ou_edge[0]
				constr += "- x_{}_{} ".format(i,k)

			# reformat string
			constr += "= 0"

			# save node i constraints
			self.conserv_cnt.append(constr)
		
		# maximise: x_source_sink
		self.objective = "x_{}_{}".format(self.sink, self.source)

	def genModelFile(self):
		with open(self.modelName(), "w") as f:
			f.write("Maximize\n")
			f.write("\t obj: " + self.objective + "\n")
			f.write("Subject To\n")
			for c in self.capacity_cnt:
				f.write("\t" + c + "\n")
			for c in self.conserv_cnt:
				f.write("\t" + c + "\n")
			f.write("End")

	def createModel(self):
		self.parseInstanceFile()
		self.genConservConstr()
		self.genModelFile()


"""
----------- Main -----------
"""

def main():
	g = LPModelGenerator("instances/inst-100-0.1.txt")
	g.createModel()


if __name__ == '__main__':
	main()