' Reference: github.com/christianb93/QuantumComputing/blob/master/Qiskit/QiskitQuantumTeleportation.ipynb'

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ
from qiskit.circuit import QuantumRegister, QuantumCircuit, Qubit, ClassicalRegister
from qiskit import (Aer, execute)
from qiskit.visualization import plot_histogram

mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)


''' Transform the computational basis in to the Bell basis'''


def compToBellBasis(q, *c):
    circuit = QuantumCircuit(q, *c)
    circuit.h(q[1])
    circuit.cx(q[1], q[0])

    return circuit


def stateVectorToString(vector, places=3):
    s = ""
    count = 0
    for i in range(len(vector)):
        x = round(vector[i], places)
        if x.imag != 0:
            coeff = "(" + format(x.real, '+') + format(x.imag, '+') + "i)"
        else:
            coeff = format(x.real, '+')
        if (x != 0):
            s = s + coeff + "|" + format(i, '02b') + ">"
            count = count + 1
    return s


def testBellBasis():
    backend = Aer.get_backend('statevector_simulator')
    for x in range(4):
        q = QuantumRegister(2, "q")
        transform_circuit = compToBellBasis(q)
        init_circuit = QuantumCircuit(q)
        initial_state = np.zeros(4, dtype=complex)
        initial_state[x] = 1.0
        init_circuit.initialize(initial_state, q)
        circuit = init_circuit + transform_circuit

        job = execute(circuit, backend)
        out = job.result().get_statevector()

        print("|" + format(x, '02b') + ">" + " ---->" + stateVectorToString(out))


''' Main Program '''
# testBellBasis()

q = QuantumRegister(3, "q")
c0 = ClassicalRegister(1, "c0")
c1 = ClassicalRegister(1, "c1")
c2 = ClassicalRegister(1, "c2")

init_circuit = QuantumCircuit(q, c0, c1, c2)
init_state = np.zeros(2 ** 3, dtype=complex)
init_state[0] = 1.0
init_circuit.initialize(init_state, [q[0], q[1], q[2]])

' Build the Teleportation Circuit '
tc = compToBellBasis(q, c0, c1)
tc.barrier()
tc.cx(q[1], q[2])
tc.h(q[1])
tc.barrier()
tc.measure(q[2], c0[0])
tc.measure(q[1], c1[0])
tc.barrier()
tc.x(q[0]).c_if(c0, 1)
tc.z(q[0]).c_if(c1, 1)
tc.barrier()
mc = QuantumCircuit(q, c2)
mc.measure(q[0], c2[0])
circuit = tc + mc

' Set up Quantum Computer '
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
counts = result.get_counts()

' Plot the results '
plot_histogram(counts);
show_figure(plot_histogram(result.get_counts(circuit)))
show_figure()

' Misc '
prep = QuantumCircuit(q)
prep.x(q[2])
prep.barrier()
tc = prep + tc + mc
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
counts = result.get_counts()
plot_histogram(counts);
show_figure(plot_histogram(result.get_counts(circuit)))
show_figure()
