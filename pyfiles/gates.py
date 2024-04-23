import numpy as np

# basic gates, no input required
s_gates = {
    "h": (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]]),
    "x": np.array([[0, 1], [1, 0]]),
    "id": np.array([[1, 0], [0, 1]]),
    "s": np.array([[1, 0], [0, 0+1j]]),
    "t": np.array([[1, 0], [0, np.power(np.e, np.pi/4 * 1j)]]),
    "z": np.array([[1, 0], [0, -1]]),
    "y": np.array([[0, -1j], [1j, 0]]),
    "tdg": np.array([[1, 0], [0, np.power(np.e, -1j * np.pi / 4)]]),
    "sdg": np.array([[1, 0], [0, -1j]])
} 

# gates where input is required (cx is special case)
var_gates = {"rz", "p", "rx", "u", "ry", "cx"}


def make_var_gate(inputs: list) -> None: 
    """
    given a list input, returns the respective gate (this method is for gates that require inputs)

    args:
        inputs: list following the format [gateName, [args]], where gateName is a string and args is a list
                    for a unitary matrix, args = [theta, phi, lambda]
    """
    gate = inputs[0]
    theta = inputs[1][0]
    if gate == "u": 
        phi, lamb = inputs[1][1], inputs[1][2]
        return np.array([
            [np.cos(theta / 2), np.sin(theta / 2) * -np.power(np.e, 1j * lamb)],
            [np.sin(theta / 2) * np.power(np.e, 1j * phi), np.cos(theta / 2) * np.power(np.e, 1j * (lamb + phi))]
        ])
    elif gate == "rx":
        return np.array([
            [np.cos(theta / 2), -1j * np.sin(theta / 2)], 
            [-1j * np.sin(theta / 2), np.cos(theta / 2)]
        ])
    elif gate == "ry":
        return np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)], 
            [np.sin(theta / 2), np.cos(theta / 2)]
        ])
    elif gate == "rz":
        return np.array([
            [np.power(np.e, -1j * theta / 2), 0], 
            [0, np.power(np.e, 1j * theta / 2)]
        ])
    elif gate == "p":
        return np.array([
            [1, 0], 
            [0, np.power(np.e, 1j * theta)]
        ])

def create_cnot(control: int, target: int):
    """
    returns the corresponding cnot gate matrix given a control and target

    pre:
        target != control
    args:
        control: position of the control qubit
        target: position of the target qubit
    return:
        cnot gate as an NDArray
    """
    if target == control:
        raise ValueError
    
    n = np.abs(target - control)
    h1, h2 = np.array([[1], [0]]), np.array([[1, 0]])
    houter = np.outer(h1, h2)

    v1, v2 = np.array([[0], [1]]), np.array([[0, 1]])
    vouter = np.outer(v1, v2)

    size = np.power(2, n)
    id1 = np.identity(size)
    id2 = np.identity(int(size / 2))
    
    if target < control:
        term1 = np.kron(houter, id1)
        term2 = np.kron(vouter, np.kron(id2, s_gates['x']))
        return term1 + term2

    term1 = np.kron(id1, houter)
    term2 = np.kron(np.kron(s_gates['x'], id2), vouter)
    return term1 + term2

def parse_cnot(instruction: str, instr_list: list) -> None:
    """
    parses a cnot gate instruction from a qasm file, adding the result to a given instruction list

    args:
        instruction: a given cnot instruction
        instr_list: a given instruction list (will be modified)
    """
    parts = instruction.split(" ")

    control, target = int(parts[1][2:][:-2]), int(parts[2][2:][:-1])
    start, fin = min(control, target), max(control, target)
    index = max(len(instr_list[control]), len(instr_list[target]))
    for i in range(start, fin + 1):
        padding = index - len(instr_list[i]) if index - len(instr_list[i]) > 0 else 0
        for _ in range(padding): 
            instr_list[i].append([])
            
        instr_list[i].append([]) if i == start or i == fin else instr_list[i].append(["cxb"])

    instr_list[control][-1] = ["cxc"]
    instr_list[target][-1] = ["cx"]

def choose_gate(gate_arr: str):
    """
    given an instruction, returns the corresponding gate as a matrix
    
    args:
        gate_arr = [gateName, [args] (if applicable)] where gateName is a string, and args contains the arguments of the gate, if there are any
    returns:
        gate as an NDArray
    """
    if not gate_arr:
        return s_gates['id']
    elif gate_arr[0] in s_gates:
        return s_gates[gate_arr[0]]
    else:
        return make_var_gate(gate_arr)
