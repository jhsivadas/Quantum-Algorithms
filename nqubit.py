from parent_qubit import ParentQubit
import numpy as np

class NQubit(ParentQubit):

    def __init__(self, numqubits):
        super().__init__(numqubits)
        self.state = np.zeros(2**numqubits)
        self.state[0] = 1