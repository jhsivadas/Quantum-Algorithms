from parent_qubit import ParentQubit
import numpy as np

class QOracle():

    def __init__(self):
        self.pq = ParentQubit(4) 
        self.bernvaz = None 
        self.archimedes = None

    def set_bernvaz(self, code):
        bin = format(code, 'b').zfill(3)
        oracle = np.identity(16)
        for b in range(len(bin)):
            if int(bin[b]) > 0:
                oracle = np.dot(oracle, self.pq.apply_cnot_gate(b, 3))
            else:
                np.dot(oracle, np.identity(16))
        self.bernvaz = oracle
        return oracle
    
    def probe_bernvaz(self, nq):
        nq.state = np.dot(self.bernvaz, nq.state)


    def set_archimedes(self, codes):

        oracle = np.identity(16)
        bin = []
        for code in codes:
            code_bin = format(code, 'b').zfill(3)
            code_bin_0 = code_bin + "0"
            code_bin_1 = code_bin + "1"
            bin.append(code_bin_0)
            bin.append(code_bin_1)

        for code in bin:
            for i in range(len(self.pq.state)):
                if format(i, 'b').zfill(4) == code:
                    code_list = list(code)
                    code_list[-1] = "1" if code_list[-1] == "0" else "0"
                    location = int(''.join(code_list), 2)
                    oracle[i][location] = 1
                    oracle[i][i] = 0
        self.archimedes = oracle
        return oracle

    
    def probe_archimedes(self, nq):
        nq.state = np.dot(self.archimedes, nq.state)