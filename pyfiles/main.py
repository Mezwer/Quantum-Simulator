#%%
import numpy as np
import matplotlib.pyplot as plt
import random
from gates import s_gates, parse_cnot
from calc import create_final_state

# get all lines from QASM File
instructions = []
q_reg = []
with open("Untitled circuit.qasm", "r") as f:
    for line in f:
        if "barrier" not in line and line != "\n": 
            if line[0] == "u":
                n = len(line)
                instructions.append(line[:n - 7].replace(" ", "") + " " + line[n - 6:n - 2])
            else: 
                instructions.append(line[:-2])

# parse all QASM File lines into instructions to be computed
instructions = instructions[2:]
for i in range(int(instructions[0][7:][:-1])):
    q_reg.append([])

for i in range(2, len(instructions)):
    op, n = instructions[i].split(), ""
    gateName, inputs = op[0], []

    # for gates with inputs
    if gateName not in s_gates and gateName != "cx":
        gateName = gateName[:1] if "(" in gateName[:2] else gateName[:2]

        inputs = (op[0][len(gateName) + 1: len(op[0]) - 1]).split(",")
        for i, v in enumerate(inputs): 
            inputs[i] = v.replace("pi", "np.pi")
            inputs[i] = eval(inputs[i])            

    if gateName == "cx": 
        parse_cnot(instructions[i], q_reg)
    else:
        for i in range(2, len(op[1]) - 1):
            n += op[1][i]

        n = int(n)
        operations = [gateName]
        if len(inputs): 
            operations.append(inputs)

        if not len(q_reg[n]) or q_reg[n][-1] != ["cxb"]: 
            q_reg[n].append(operations)
            continue

        placed = False
        for i in range(len(q_reg[n])):
            if not q_reg[n][i]:
                q_reg[n][i] = operations
                placed = True
                break
        
        if not placed: 
            q_reg[n].append(operations) 
    
max_len = max([len(i) for i in q_reg])
for i in q_reg:
    for _ in range(max_len - len(i)):
        i.append([])

# get final state and results
state = create_final_state(q_reg, len(q_reg)).ravel()
y_axis, chances = [], []
x_axis = []
for i in range(len(state)):
    formatter = format(i, f'0{int(np.log2(len(state)))}b')
    percentage = np.power(np.abs(state[i]), 2)

    chances.append(percentage)
    y_axis.append(percentage * 100)
    x_axis.append(formatter)

#%%
# show result of simulating quantum circuit with x number of shots (default 8192)
shots = 8192
sim_results = [0] * len(chances)
while shots != 0:
    for i, v in enumerate(chances):
        if random.random() < v:
            sim_results[i] += 1
            shots -= 1
        
        if shots == 0: break

fig = plt.figure(figsize=(len(x_axis), 5))
plt.bar(x_axis, sim_results, color="green")
plt.xlabel("State")
plt.ylabel("Times Detected")

#%%
# show final state probabilites
fig = plt.figure(figsize=(len(x_axis), 5))
plt.bar(x_axis, y_axis, color="blue")
plt.xlabel("State")
plt.ylabel("Probability (%)")
plt.ylim(0, 100)