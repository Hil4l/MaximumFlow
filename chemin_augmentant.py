""" 
--------------------------------------------------------------------------------------------
Author: Hilal Rachik 520550

Parametre (command line): instance file "inst-n-p.txt"
Generates: Finds optimal solution and saved in a file "model-n-p.path"
-------------------------------------------------------------------------------------------- 
""" 

from data_strcutures.adj_mat_digraph import Graph

class FordFulkersonSolver:
	
    def __init__(self, instance_file):
         self.instance_file = instance_file
         self.graph = Graph(instance_file)
         self.sol = -1;
    
    def modelName(self) -> str:
        p = self.graph.E / (self.graph.V ** 2)
        model_name = "model-{}-{:.1f}.lp".format(self.graph.V, p)
        return model_name

    def genSolFile(self) -> None:
        with open(self.modelName(), "w") as f:
            f.write("Max flow = " + self.sol)
    
    def findSol(self) -> None:
         self.sol = self.graph.FordFulkerson()
         print("solution calculated")
         self.genSolFile()
         print("solution file created")

"""
----------- Main -----------
"""

def main():
    g = FordFulkersonSolver("instances/instanceTest.txt")
    print(g.modelName())

if __name__ == '__main__':
	main()