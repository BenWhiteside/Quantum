# diva-portal.org/smash/get/diva2:1214481/FULLTEXT01.pdf
import matplotlib as mpl
import matplotlib.pyplot as plt

from qiskit import *
from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr

import math
pi = math.pi

from qiskit import IBMQ
IBMQ.enable_account('f449711b0c038b51fffe0850b50458ef02b0acf732f2baa66e1209cf870de445b9480c56065e37b79f8920e7e063e2656ad76b1ed32e5271f1c9af8fbd04d80e')
provider = IBMQ.get_provider(hub='ibm-q')

mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show()


# Use Aer
#backend = Aer.get_backend('qasm_simulator')
backend = IBMQ.get_backend('ibmqx2')
print('Provider: ', backend)
shots = 16 # 8192

# Create a Quantum Register of 4 qubits:
qr = qiskit.QuantumRegister(4, 'qr')
cr = qiskit.ClassicalRegister(4, 'cr')
qc = qiskit.QuantumCircuit(qr, cr)


# Initialisation in to superposition:
for i in [0, 1, 2, 3]:
    qc.h(qr[i])


# Oracle for 0010
qc.x(qr[0])
qc.x(qr[2])
qc.x(qr[3])
qc.barrier()

qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.barrier()

qc.x(qr[0])
qc.x(qr[2])
qc.x(qr[3])
qc.barrier()

# Amplitude Amplification
for i in [0, 1, 2, 3]:
    qc.x(qr[i])
qc.barrier()

# START cccZ
qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.barrier()
# END cccZ

# Amplitude Amplification
for i in [0, 1, 2, 3]:
    qc.x(qr[i])

# Initialisation in to superposition:
for i in [0, 1, 2, 3]:
    qc.h(qr[i])

# Measure
qc.barrier()
for i in [0, 1, 2, 3]:
    qc.measure(qr[i], cr[i])

# Plot Circuit
diagram = qc.draw(output='mpl')  # output='mpl', output='latex', scale=0.5
show_figure(diagram)

# Submit job
#job = execute(qc, backend, shots=shots)
job = execute(qc, backend, shots=shots, max_credits=5)

print('Executing Job...\n')
result = job.result()
counts = result.get_counts(qc)
print('RESULT: ', counts, '\n')
