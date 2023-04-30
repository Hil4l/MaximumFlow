# Maximum Flow (linear problem) Project

Dependencies: glpk

script: Lp model generator
run: python3 generate_model.py "inst-n-p.txt"
generates: model-n-p.lp
solve: glpsol --lp model.lp -o model.sol

script: Ford Fulkerson solver
run: python3 chemin_augmentant.py "inst-n-p.txt"
generates: model-n-p.path