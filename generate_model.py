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
			self.graph.add_edge(self.source, self.sink)


	# Model name
	def modelName(self) -> str:
		p = self.graph.V / self.graph.E ** 2
		model_name = "model-{}-{:.1f}.lp".format(self.graph.V, p)
		return model_name

	def generateModel(self):
		
		# Conservation constraints: x_i_j = sum(x_j_k) Vk
		for i in self.graph.nodes:
			for t1 in self.graph.out_edges(i):
				j = t1[0]
				constr = "x_{}_{} = ".format(i,j)  

				for t2 in self.graph.out_edges(j):
					k = t2[0]
					constr += "x_{}_{} + ".format(j,k)

				constr = constr[:-3]  # remove last "+ "
				self.conserv_cnt.append(constr)

		# maximise: x_source_sink
		maximise = "x_{}_{}".format(self.source, self.sink)


def main():
	g = LPModelGenerator("instanceTest.txt")
	g.parseInstanceFile()
	g.generateModel()

	print(g.conserv_cnt)


if __name__ == '__main__':
	main()