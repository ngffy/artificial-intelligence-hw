from constraint import *

p = Problem()

variables = set("BB") | set("I") | set("ILL")
p.addVariables(variables, range(0,10))

p.addVariable("X1", [0,1])

p.addConstraint(lambda B,I,L,X1: B+I == L+10*X1, ('B','I','L','X1'))
p.addConstraint(lambda B,X1,L,I: B+X1 == L+10*I, ('B','X1','L','I'))
p.addConstraint(AllDifferentConstraint(), variables)

sols = p.getSolutions()

for sol in sols:
    print("Possible solution:")
    for var in sorted(variables):
        print(var, "=", sol[var])
    print()
