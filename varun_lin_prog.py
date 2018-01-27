from pulp import *

n = [0,1,2,3,4,5]
t = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

i = n
j = n
k = t

prob = LpProblem("CVRPTW", LpMinimize)
x1 = LpVariable.dicts("x",(i,j,k),0,1,LpInteger)


