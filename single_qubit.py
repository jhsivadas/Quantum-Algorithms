from parent_qubit import ParentQubit
import numpy as np

class SingleQubit(ParentQubit):

    def __init__(self, num_qubits = 1):
        super().__init__(num_qubits)