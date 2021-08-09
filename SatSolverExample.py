from pysat.solvers import Glucose3

g = Glucose3()
## clauses corresponding to (~a or b) and (~a or c) and (a or b or d) and ~d and ~b
## The above sentence is not satisfiable. If you remove ~b, then it becomes satisfiable.
g.add_clause([-1, 2])
g.add_clause([-1, 3])
g.add_clause([1, 2, 4])
g.add_clause([-4])
#g.add_clause([-2])


print(g.solve(assumptions=[4]))


print(g.solve())

print(g.get_model())