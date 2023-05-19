""" 
--------------------------------------------------------------------------------------------
Author: Hilal Rachik 520550

Parametre (command line): instance file "inst-n-p.txt"
Generates: CPLEX LP linear program of this instance saved in a file "model-n-p.lp"
Exemple: python3 generate_model.py "inst-300-0.3.txt"  --> generates "model-300-0.3.lp"
-------------------------------------------------------------------------------------------- 
""" 

class LPModelGenerator:

	def __init__(self, instance_file:str):
		self.instance_file = instance_file
		self.matrix = []  # adj matrix graph
		self.capacity_cnt = []
		self.conserv_cnt = []

	# Graph from instance file
	def parseInstanceFile(self) -> None:
		with open(self.instance_file, 'r') as in_file:
			V = int(in_file.readline().strip().split()[1])
			source = int(in_file.readline().strip().split()[1])
			sink = int(in_file.readline().strip().split()[1])
			E = int(in_file.readline().strip().split()[1])

			for _ in range(V):
				self.matrix.append([None] * V)
		
			# edges
			while True:
				line = in_file.readline().strip().split()  # ['a', 'b', 'c']
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])

				if i == j: continue  # ignore self loop (because cancel itself in constraints)

				if self.matrix[i][j] is not None: # dup edge -> sum capacities
					self.matrix[i][j] += w
				else:  # new edge
					self.matrix[i][j] = w  # capacity = w
		
		self.E = E
		self.V = V
		self.source = source
		self.sink = sink
		

	def inc_edges(self, i):
		# yield inc edges of node i: j, (fij,cij)
	
		ls = [row[i] for row in self.matrix]  # i column
		for j, t in enumerate(ls):
			if t is not None:  # (i,j) ∈ A
				yield j, t
	
	def out_edges(self, i):
		# yield out edges of node i: j, (fij,cij)
		ls = self.matrix[i]
		for j, t in enumerate(ls):
			if t is not None:  # (i,j) ∈ A
				yield j, t
		
	# ------------------------------------------------------------------------------------------

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

		for i in range(self.V):
			for j, w in self.out_edges(i):
				constr = "x_{}_{} <= {}".format(i, j, w)  
				self.capacity_cnt.append(constr)

	def genConservConstr(self) -> None:
		"""
		Conservation constraints: sum(out flows) - sum(inc flows) = v if S, -v if T, 0 else
		<=> sum(x_j_i) - sum(x_i_k) = 0 {v if S, -v if T, 0 else}
		"""

		for i in range(self.V):
			constr = ""
			for j, w in self.out_edges(i):  
				constr += "x_{}_{} + ".format(i,j)

			# reformat string
			constr = constr[:-2]

			for j, w in self.inc_edges(i):
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
		self.genCapacityConstr()
		self.genConservConstr()		
		self.genModelFile()

"""
----------- Main -----------
"""

def inst_test():
	import subprocess
	import os

	n_max = 7
	for n in range(7,n_max+1):
		for p in range(1,4):
			inst = f"instances/inst-{n}00-0.{p}.txt"
			
			g = LPModelGenerator(inst)
			g.createModel()
			
			model_file = f"model-{n}00-0.{p}.lp"
			sol_file = f"sol-{n}00-0.{p}.sol"
			command = ["glpsol", "--lp", model_file, "-o", sol_file]
			subprocess.run(command)

			os.remove(model_file)
			# os.remove(sol_file)
			print("--------------------------------")


def main():
	# TODO: command line parametre !!!!!

	# instance_file = "instances/inst-700-0.3.txt"
	# g = LPModelGenerator(instance_file)
	# g.createModel()

	inst_test()

if __name__ == '__main__':
	main()