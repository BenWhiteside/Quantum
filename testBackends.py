from qiskit import Aer

for backend in Aer.backends():
    print(backend.name())

