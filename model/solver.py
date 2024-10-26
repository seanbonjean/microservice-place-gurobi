import sys
import math
from input import Data
from gurobipy import *

if len(sys.argv) != 2:
    print("invalid options")
    print("example of use: ./solver.py input.txt")
    exit(1)

# Read input file
data = Data(sys.argv[1])
# nodes = range(data.size)
model = Model("microservice-placement")
# model.setParam(GRB.Param.TimeLimit, 60 * 60 * 10.0) # 10 hour

# Variables
x = {}  # x(i, k)在第k个节点放置第i个微服务
y = {}  # y(i, k)路径中使用了第k个节点上的第i个微服务

# x(i, k)
for i in range(data.microservice_count):
    for k in range(data.edgenode_count):
        x[(i, k)] = model.addVar(vtype=GRB.BINARY, name="x_%d_%d" % (i, k))

# y(i, k, h)
for i in range(data.microservice_count):
    for k in range(data.edgenode_count):
        for h in range(data.task_count):
            y[(i, k, h)] = model.addVar(
                vtype=GRB.BINARY, name="y_%d_%d_%d" % (i, k, h))

# Update model
model.update()

# Add constraints

# y(i, k)

# 一个f中，每个微服务只能指定一个节点提供
for h, f in enumerate(data.task_dependency):
    for i in f:
        model.addConstr(quicksum(y[(i, k, h)]
                        for k in range(data.edgenode_count)) == 1)
"""
    # 不能去找不需要的微服务
    for i in range(data.microservice_count):
        if i not in f:
            model.addConstr(quicksum(y[(i, k, h)]
                            for k in range(data.edgenode_count)) == 0)
"""

# Th < Th_max
"""
# 前置工作，大M法引入辅助变量
k_value = {}
for h, f in enumerate(data.task_dependency):
    for i in f:
        # 添加辅助变量 k(i)，这是一个整数变量，表示满足 y(i, k) = 1 时的 k
        k_value[(i, h)] = model.addVar(vtype=GRB.INTEGER,
                                       name=f"k_{i}_{h}", lb=0, ub=data.edgenode_count-1)
    # 关联 y(i, k) 和 k_value(i)：k_value(i) 必须等于使得 y(i, k) = 1 的 k
    for i in f:
        for k in range(data.edgenode_count):
            model.addConstr(k_value[(i, h)] >= k -
                            (1 - y[(i, k, h)]) * data.edgenode_count)
            model.addConstr(k_value[(i, h)] <= k +
                            (1 - y[(i, k, h)]) * data.edgenode_count)
model.update()
"""
# 添加约束 Th < Th_max
Ttime = [0] * data.task_count
for h, f in enumerate(data.task_dependency):
    Ttime[h] = quicksum(y[(f[0], k, h)] * (data.data_size_user / data.r_uovk_user[(k, h)] + data.request_resource[f[0]] / data.c_vk[k]) for k in range(data.edgenode_count)) + quicksum(
        y[(f[i+1], k, h)] * (data.data_size[f[i]] * quicksum(y[(f[i], k_prev, h)] * (1 / (data.r_uovk[(k_prev, k)] if data.r_uovk[(k_prev, k)] != 0 else 1e7)) for k_prev in range(data.edgenode_count)) + data.request_resource[f[i+1]] / data.c_vk[k]) for i in range(len(f) - 1) for k in range(data.edgenode_count))
    model.addConstr(Ttime[h] - data.T_h_max <= 0)
# k_value[(f[i], h)]

# x(i, k)

# C < C_max
Cost = quicksum(x[(i, k)] * data.place_cost[i] for i in range(data.microservice_count) for k in range(data.edgenode_count))
model.addConstr(Cost - data.C_max <= 0)

# 边缘节点上的微服务总量不超过节点上限
for k in range(data.edgenode_count):
    model.addConstr(quicksum(x[(i, k)] for i in range(
        data.microservice_count)) - data.node_capacity[k] <= 0)

# y(i, k) <= x(i, k)
for i in range(data.microservice_count):
    for k in range(data.edgenode_count):
        for h in range(data.task_count):
            model.addConstr(y[(i, k, h)] - x[(i, k)] <= 0)

# Objective function
model.setObjective(Cost + quicksum(Ttime[h] for h in range(data.task_count)))

# Save LP model and run
model.write('model.rlp')

model.modelSense = GRB.MINIMIZE
model.optimize()

# Print results
if model.status != GRB.OPTIMAL:
    print('No optimum solution found. Status: %i' % (model.status))
else:
    print("Optimal solution found")
    x_result = [(i, k) for i in range(data.microservice_count) for k in range(data.edgenode_count) if x[(i, k)].X > 0.9]
    y_result = [(i, k, h) for i in range(data.microservice_count) for k in range(data.edgenode_count) for h in range(data.task_count) if y[(i, k, h)].X > 0.9]
    print("Result = %.4f" % model.objVal)
    print("GAP = %.4f %%" % model.MIPGap)
    print("Time = %.4f seg" % model.Runtime)

    print("x(i, k): ")
    print(x_result)
    print("y(i, k, h): ")
    print(y_result)
