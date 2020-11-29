from qiskit import Aer
from qiskit import IBMQ

for backend in Aer.backends():
    print(backend.name())


for backend in IBMQ.providers():
    print(backend.name())