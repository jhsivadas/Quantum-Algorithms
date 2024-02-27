from parent_qubit import ParentQubit

class QCircuit:

    def same_entangle(qa, i, j):
        qa.apply_hadamard_gate(i)
        qa.apply_cnot_gate(i, j)

    def bernvaz(qa, qo):
        for i in range(4):
            qa.apply_hadamard_gate(i)

        qo.probe_bernvaz(qa)

        for i in range(4):
            qa.apply_hadamard_gate(i)

    
    def archimedes(qa, qo):
        for i in range(4):
            qa.apply_hadamard_gate(i)

        qo.probe_archimedes(qa)

        for i in range(4):
            qa.apply_hadamard_gate(i)