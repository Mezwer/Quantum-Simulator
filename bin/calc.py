import numpy as np
from gates import choose_gate, create_cnot

def combine_gates(gates: list):
    """
    combines all the gates from a given list of gates, returning the final fully combined gate\n
    kronecker tensors all gates in each column, then multiplies them together

    args:
        gates - list of all gates
    returns:
        final "gate" as an NDArray
    """
    final_gate = None
    for i in range(len(gates[0])):
        init_gate = None
        j = 0
        while j < len(gates):
            gate = None          
            if gates[j][i] and gates[j][i][0] in ["cxc", "cx"]:
                control, target = 0, 0
                if gates[j][i][0] == "cxc": 
                    control = j
                else: 
                    target = j

                for k in range(j + 1, len(gates)):
                    j += 1
                    if gates[k][i][0] in ["cxc", "cx"]:
                        if gates[j][i][0] == "cxc": 
                            control = k
                        else: 
                            target = k
                        break
                gate = create_cnot(control, target)
            else: 
                gate = choose_gate(gates[j][i])

            init_gate = gate if init_gate is None else np.kron(gate, init_gate)
            j += 1

        final_gate = init_gate if final_gate is None else np.matmul(init_gate, final_gate)

    return final_gate

def create_final_state(gates: list, qubits: int):
    """
    returns the final state of a quantum circuit given a list of gates and number of qubits

    args:
        gates - list of gates in the quantum circuit
        qubits - number of qubits
    returns:
        final state as an NDArray
    """
    comp_zero, state = np.array([[1], [0]]), np.array([[1], [0]])
    for _ in range(qubits - 1):
        state = np.kron(state, comp_zero)

    return np.matmul(combine_gates(gates), state)