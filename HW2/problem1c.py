from constraint import *

p = Problem()

variables = set("ELVIS") | set("PRESLEY") | set("POSTERS")
p.addVariables(variables, range(0,10))

carries = ['X1','X2','X3','X4','X5','X6']
p.addVariables(carries, [0,1])

p.addConstraint(lambda Y,S,X1: Y+S == S+10*X1, ('Y','S','X1'))
p.addConstraint(lambda E,I,X1,R,X2: E+I+X1 == R+10*X2, ('E','I','X1','R','X2'))
p.addConstraint(lambda L,V,X2,E,X3: L+V+X2 == E+10*X3, ('L','V','X2','E','X3'))
p.addConstraint(lambda S,L,X3,T,X4: S+L+X3 == T+10*X4, ('S','L','X3','T','X4'))
p.addConstraint(lambda E,X4,S,X5: 2*E+X4 == S+10*X5, ('E','X4','S','X5'))
p.addConstraint(lambda R,X5,O,X6: R+X5 == O+10*X6, ('R','X5','O','X6'))
p.addConstraint(lambda P,X6: P+X6 == P, ('P','X6'))
p.addConstraint(AllDifferentConstraint(), variables)

sols = p.getSolutions()

for sol in sols:
    print("Possible solution:")
    for var in sorted(variables):
        print(var, "=", sol[var])
    print()
