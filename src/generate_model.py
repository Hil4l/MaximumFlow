"""
--------------------------------------------------------------------------------------------
Author: Hilal Rachik / Nadim Rachik

Parametre: instance file "inst-n-p.txt"
Generates: linear program model "model-n-p.lp" and its resolution by glpk "model-n-p.sol"
-------------------------------------------------------------------------------------------- 
""" 

import subprocess
import sys


class LPModelGenerator:

	def __init__(self, instance_file:str):
		self.instance_file = instance_file
		self.capacity_cnt = []
		self.conserv_cnt = []

		with open(instance_file) as f:
			V = int(f.readline().strip().split()[1])
			source = int(f.readline().strip().split()[1])
			sink = int(f.readline().strip().split()[1])
			E = int(f.readline().strip().split()[1])

			self.out_edges = {u: {} for u in range(V)}
			self.inc_edges = {u: {} for u in range(V)}  # trade off space complexity for time complexity, better for conservation constraints
			
			while True:
				line = f.readline().strip().split()
				if not line: break
				i, j, w = int(line[0]), int(line[1]), int(line[2])

				if i == j: continue  # ignore self loop (cancel itself in constraints)

				# save last capacity
				self.out_edges[i][j] = w
				self.inc_edges[j][i] = w

		self.source = source
		self.sink = sink
		self.V = V
		self.E = E
		
	# ------------------------------------------------------------------------------------------

	# Model name
	def model_name(self) -> str:
		p = self.E / (self.V ** 2)
		name = "model-{}-{:.1f}.lp".format(self.V, p)
		return name

	def gen_capacity_constr(self) -> None:
		"""
		Capacity constraints: edge flow <= edge capacity
		x_i_j <= capacity
		"""

		for i, edges in self.out_edges.items():
			for j, w in edges.items():
				constr = "x_{}_{} <= {}".format(i, j, w)  
				self.capacity_cnt.append(constr)

	def gen_conserv_constr(self) -> None:
		"""
		Conservation constraints: sum(out flows) - sum(inc flows) = v if S, -v if T, 0 else
		<=> sum(x_j_i) - sum(x_i_k) = 0 {v if S, -v if T, 0 else}
		"""
		for i in range(self.V):
			constr = ""

			for j in self.out_edges[i].keys():
				constr += "x_{}_{} + ".format(i,j)

			# reformat string
			constr = constr[:-2]

			for j in self.inc_edges[i].keys():
				constr += "- x_{}_{} ".format(j,i)

			# constraint equality
			if i == self.source:
				constr += "- v_0 = 0"
			elif i == self.sink:
				constr += "+ v_0 = 0"
			else:
				constr += "= 0"

			# save node i constraints
			self.conserv_cnt.append(constr)

	def gen_model(self, model_file):
		with open(model_file, "w") as f:
			f.write("Maximize\n")
			f.write("\t obj: v_0\n")
			f.write("Subject To\n")
			for c in self.capacity_cnt:
				f.write("\t" + c + "\n")
			for c in self.conserv_cnt:
				f.write("\t" + c + "\n")
			f.write("End")

	def gen_sol(self, model_file, sol_file):
		command = ["glpsol", "--lp", model_file, "-o", sol_file]
		subprocess.run(command)

	def compute(self):
		p = self.E / (self.V ** 2)
		model_file = f"model-{self.V}-{p:.1f}.lp"
		sol_file = f"model-{self.V}-{p:.1f}.sol"

		self.gen_capacity_constr()
		self.gen_conserv_constr()
		self.gen_model(model_file)
		self.gen_sol(model_file, sol_file)

"""
----------- Main ----------------------------------
"""

def main():
	if len(sys.argv) != 2:
		print("Usage: python3 generate_model.py instance.txt")
		sys.exit(1)

	instance_file = sys.argv[1]
	g = LPModelGenerator(instance_file)
	g.compute()

if __name__ == '__main__':
	main()