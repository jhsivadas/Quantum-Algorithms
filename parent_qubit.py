import numpy as np

class ParentQubit:
    def __init__(self, numqubits):
        self.numqubits = numqubits
        self.state = np.zeros(2**numqubits)
        self.state[0] = 1

    def set_value(self, v, i):
        self.state[i] = v

    def set_values(self, v):
        self.state = v

    def get_value(self, i):
        return self.state[i]
        

    def get_values(self):
        return self.state
    
    def set_phase(self, p, i):
        self.state[i] *= p 

    def set_phases(self, p):
        for i, phase in enumerate(p):
            self.state[i] *= phase
        
    def get_phase(self, i):
        return -1 if self.state[i] < 0 else 1

    def get_num_qubits(self):
        return self.numqubits
    
    def merge_qubits(self, pq):
        numqubits_new = self.numqubits + pq.numqubits
        state_new = np.kron(self.state, pq.state)
        new_pq = ParentQubit(numqubits_new)
        new_pq.set_values(state_new)
        return new_pq
    
    def to_bra_ket(self):
        bra_ket = ""
        sign = "-"
        for i in range(len(self.state)):
            
            binary = str(self.state[i]) + "|" + format(i, 'b').zfill(self.numqubits) + ">"
            if i < len(self.state) - 1:
                if self.state[i + 1] < 0:
                    sign = " - "
                else:
                    sign = " + "

                bra_ket += str(binary) + sign
            else:
                bra_ket += str(binary)

        return bra_ket
    
    def apply_not_gate(self, i = None):
        notgate = np.array([[0, 1], [1, 0]])
        if i is not None:
            new_gate = self.create_parallel(notgate, i)
            self.state = np.dot(new_gate, self.state)
        else:
            for j in range(self.numqubits):
                new_gate = self.create_parallel(notgate, j)
                self.state = np.dot(new_gate, self.state)

    def apply_hadamard_gate(self, i = None):
        hgate = np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)],
                          [1 / np.sqrt(2), -1 / np.sqrt(2)]])
        if i is not None:
            gate = self.create_parallel(hgate, i)
            self.state = np.dot(gate, self.state)
        else:
            for j in range(self.numqubits):
                gate = self.create_parallel(hgate, j)
                self.state = np.dot(gate, self.state)
    
    def apply_z_gate(self, i = None):
        zgate = np.array([[1, 0], [0, -1]])
        if i is not None:
            gate = self.create_parallel(zgate, i)
            self.state = np.dot(gate, self.state)
        else:
            for j in range(self.numqubits):
                gate = self.create_parallel(zgate, j)
                self.state = np.dot(gate, self.state)

    def apply_cnot_gate(self, ctrl, targ):
        bin = [format(k, 'b').zfill(self.numqubits) for k in range(len(self.state))]
        start = np.identity(2**self.numqubits)
        for index, b in enumerate(bin):
            if b[ctrl] == "1":
                temp_list = list(b)
                temp_list[targ] = "1" if temp_list[targ] == "0" else "0"
                location = int(''.join(temp_list), 2)
                start[index, location] = 1
                start[index, index] = 0
        self.state = np.dot(start, self.state)
        return start

                
    def apply_swap_gate(self, i, j):
        bin = [format(k, 'b').zfill(self.numqubits) for k in range(len(self.state))]
        start = np.identity(2**self.numqubits)
        for index, b in enumerate(bin):
            if b[i] != b[j]:
                temp = b[i]
                temp_list = list(b)
                temp_list[i] = b[j]
                temp_list[j] = temp 
                location = int(''.join(temp_list), 2)
                start[location, index] = 1
                start[index, index] = 0

        self.state = np.dot(start, self.state)
            
    def measure(self):
        probs = np.square(self.state)
        bin = range(len(self.state))
        output = np.random.choice(bin,p=probs)
        self.state = np.zeros(len(self.state))
        self.state[output] = 1
        return output

    """
    Helper Functions
    """
    # Creates vector from qubit representation 
    def create_parallel(self, gate, i):
        identity = np.array([[1, 0], [0, 1]])
        if i == 0:
            start = gate
        else:
            start = identity

        
        for j in range(1, self.numqubits):
            if j == i:
                start = np.kron(start, gate)
            else:
                start = np.kron(start, identity)
        return start