#coding: utf-8
import sys
import math
import random
import collections
import instance
from gurobipy import *

(s, c, h, M, T, d) = instance.leitura()

io = 0

model = Model('lot sizing problem')

x = model.addVars(T, vtype = GRB.CONTINUOUS, name = 'x')
y = model.addVars(T, vtype = GRB.BINARY, name = 'y')
i = model.addVars(T, vtype = GRB.CONTINUOUS, name = 'i')

model.update()

model.setObjective(quicksum(s[t] * y[t] + c[t] * x[t] + h * i[t] for t in T), GRB.MINIMIZE)

model.addConstrs(x[t] + io - i[t] == d[t] for t in T if t < 2)
model.addConstrs(x[t] + i[t - 1] - i[t] == d[t] for t in T if t > 1)
model.addConstrs(x[t] <= M * y[t] for t in T)

model.write('lot_sizing.lp')

model.optimize()

model.reset()
model.remove(model.getConstrs())
model.remove(model.getVars())
