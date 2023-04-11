from docplex.mp.model import Model

# Create a new model
model = Model()

# Define variables
x = model.integer_var(name='x', lb=2, ub=3)
y = model.integer_var(name='y', lb=0)
z = model.integer_var(name="z", lb=0)

# Define constraints
model.add_constraint(x + 2 * y <= 3)
model.add_constraint(2 * x + y <= 3)


# Define objective function
model.maximize(x + y + z)

# Write model to LP file
model.export_as_lp('my_lp.lp')