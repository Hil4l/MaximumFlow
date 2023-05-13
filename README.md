# INFO-F-310: Maximum Flow Project

Dependencies:
===========
- glpk

Run:
===
- Lp model generator
  	python3 generate_model.py "inst-n-p.txt"
  generates: model-n-p.lp
  - glpk solve: 
  		glpsol --lp "model-n-p.lp" -o "model-n-p.sol"

- Ford Fulkerson solver
  	python3 chemin_augmentant.py "inst-n-p.txt"
  generates: model-n-p.path