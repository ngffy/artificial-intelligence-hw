from constraint import *

p = Problem()

variables = set("THAT") | set("HIT") | set("A") | set("NERVE")
p.addVariables(variables, range(0,10))

carries = ['X1','X2','X3']
p.addVariables(carries, [0,1,2])

p.addConstraint(lambda T,A,E,X1: 2*T+A == E+10*X1, ('T','A','E','X1'))
p.addConstraint(lambda A,I,X1,V,X2: A+I+X1 == V+10*X2, ('A','I','X1','V','X2'))
p.addConstraint(lambda H,X2,R,X3: 2*H+X2 == R+10*X3, ('H','X2','R','X3'))
p.addConstraint(lambda T,X3,E,N: T+X3 == E+10*N, ('T','X3','E','N'))
p.addConstraint(AllDifferentConstraint(), variables)

sols = p.getSolutions()

for sol in sols:
    print("Possible solution:")
    for var in sorted(variables):
        print(var, "=", sol[var])
    print()
