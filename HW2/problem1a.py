from constraint import *

p = Problem()

variables = set("DAYS") | set("TOO") | set("SHORT")
p.addVariables(variables, range(0,10))

carries = ['X1','X2','X3']
p.addVariables(carries, [0,1])

p.addConstraint(lambda S,O,T,X1: S+O == T+10*X1, ('S','O','T','X1'))
p.addConstraint(lambda Y,O,X1,R,X2: Y+O+X1 == R+10*X2, ('Y','O','X1','R','X2'))
p.addConstraint(lambda A,T,X2,O,X3: A+T+X2 == O+10*X3, ('A','T','X2','O','X3'))
p.addConstraint(lambda D,X3,H,S: D+X3 == H+10*S, ('D','X3','H','S'))
p.addConstraint(AllDifferentConstraint(), variables)

sols = p.getSolutions()

for sol in sols:
    print("Possible solution:")
    for var in sorted(variables):
        print(var, "=", sol[var])
    print()
