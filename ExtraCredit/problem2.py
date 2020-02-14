from constraint import *

p = Problem()

variables = ['A','B','C','D']
p.addVariables(variables, range(1,13))

p.addConstraint(lambda A,B: B == A+3, ('A','B'))
p.addConstraint(lambda B,C: C < B-1, ('B','C'))
p.addConstraint(lambda C,D: D > 2*C, ('C','D'))
p.addConstraint(lambda A,D: D > A+4, ('A','D'))
# p.addConstraint(AllDifferentConstraint(), variables)

sols = p.getSolutions()

for sol in sols:
    print("Possible solution:")
    for var in sorted(variables):
        print(var, "=", sol[var])
    print()
