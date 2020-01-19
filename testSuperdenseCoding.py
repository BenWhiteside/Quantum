from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr
from qiskit import ClassicalRegister as cr
from qiskit import execute

# Create two registers: one quantum, one classical
q = qr(2)
c = cr(2)
circuit = qc(q, c)
