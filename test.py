# import numpy as np
# from gates import s_gates, create_cnot

# np.set_printoptions(threshold=np.inf, linewidth=np.inf)
# # hstate = np.array()
# # state = np.matmul(gates['x'], np.array([[1], [0]]))
# # print(np.matmul(gates['h'], state))

# # s1, s2 = np.array([[1], [0], [0], [0]]), np.array([[1], [0]])
# # a = np.tensordot(s1, s2, 0)
# # for i in a:
# #     print(i[0])

# h1, h2 = np.array([[1], [0]]), np.array([[1, 0]])
# houter = np.outer(h1, h2)

# v1, v2 = np.array([[0], [1]]), np.array([[0, 1]])
# vouter = np.outer(v1, v2)

# target = 2
# control = 0
# qubits = 5

# id1 = np.identity(np.power(2, target - control))
# id2 = np.identity(target - control)

# u = np.kron(id2, s_gates['x'])
# # print(u)
# # print()
# # print(id1)
# term1 = np.kron(houter, id1)
# term2 = np.kron(vouter, u)
# cx = term1 + term2

# print(cx)
# print()
# cx = create_cnot(4, 0)

# hstate = np.array([[1], [0]])
# state = np.array([[1], [0]])
# for i in range(qubits - 1):
#     state = np.kron(state, hstate)

# ops_b = np.kron(s_gates['h'], np.kron(s_gates['id'], np.kron(s_gates['h'], np.kron(s_gates['h'], s_gates['id']))))
# # print(ops_b.shape)
# # print(ops_b)
# ops_m = np.matmul(cx, ops_b)
# # print(ops_m)
# # print()
# # print(state)
# # print(ops_b)
# print(np.matmul(ops_m, state))

print([])