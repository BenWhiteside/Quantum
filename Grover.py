from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show()

n=2 # Set the number of qubits

#initialise a quantum circuit with (n) qubits
grover_circuit = QuantumCircuit(n)

def initialise_state(qc, qubits):
    for q in qubits:
        qc.h(q)
    return qc

grover_circuit = initialise_state(grover_circuit, [0,1])

#apply the oracle
grover_circuit.cz(0,1)

#apply Grover's Diffusion Operator
grover_circuit.h([0,1])
grover_circuit.z([0,1])
grover_circuit.cz(0,1)
grover_circuit.h([0,1])

# Plot Circuit
diagram = grover_circuit.draw(output='mpl')  # output='mpl', output='latex', scale=0.5
show_figure(diagram)

# SIMULATION
sim = Aer.get_backend('statevector_simulator')
job = execute(grover_circuit, sim)
psi = job.result().get_statevector()
