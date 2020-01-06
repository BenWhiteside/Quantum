# cirq.readthedocs.io/en/stable/tutorial/html

import cirq

# define the length of the grid
length = 3

# define the number of qubits on the grid
qubits = [cirq.GridQubit(i,j) for i in range(length) for j in range(length)]

# Create a quantum circuit
circuit = cirq.Circuit()
circuit.append([cirq.H(q) for q in qubits if (q.row + q.col) % 2 == 0],
               strategy=cirq.InsertStrategy.EARLIEST)
circuit.append([cirq.X(q) for q in qubits if (q.row + q.col) % 2 == 1],
               strategy=cirq.InsertStrategy.NEW_THEN_INLINE)

# print circuit
print(circuit)

