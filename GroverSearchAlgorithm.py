from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
#from qiskit.providers.ibmq import least_busy
#from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
#Initalise backends
S_simulator = Aer.backends(name='statevector_simulator')[0]
M_simulator = Aer.backends(name='qasm_simulator')[0]

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math as math
import re
import help as conundrum
#import Oracle as oracle
#import Diffusion as diffusion


mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)


N = 3 # Total number of qubits


# TEST HARNESS:

#qr    = QuantumRegister(N, name='qr')
#anc   = QuantumRegister(1, name='anc')
#n_anc = QuantumRegister(1, name='nanc')
#qc    = QuantumCircuit(qr, anc, n_anc, name='qc')

#marked = [1, 1, 0]

#qc.h(qr[0])
#qc.h(qr[1])
#qc.h(qr[2])
#qc.x(anc[0])

#print('--- Initial State ---')
#conundrum.Wavefunction(qc, systems=[3, 1, 1], show_systems=[True, False, False])

#iterations = 4

#for i in np.arange(iterations):
#    conundrum.Grover_Oracle(marked, qc, qr, anc, n_anc)
#    conundrum.Grover_Diffusion(marked, qc, qr, anc, n_anc)
#    print('\n____ ', int(i+1),'Grover Iteration ____')
#    conundrum.Wavefunction(qc, systems=[3, 1, 1], show_systems=[True, False, False])

# END OF TEST HARNESS

#Define Oracle
def oracle(qcc, q):
    qcc.x(q[1])
    qcc.h(q[2])
    qcc.ccx(q[0],q[1],q[2])
    qcc.h(q[2])
    qcc.x(q[1])

#Define Diffusion
def diffusion(qcc, q):
    qcc.h(q)
    qcc.x(q)
    qcc.h(q[2])
    qcc.ccx(q[0],q[1],q[2])
    qcc.h(q[2])
    qcc.x(q)
    qcc.h(q)

#Define Grover's Algorithm
def grover(iters, qubits):
    qr = QuantumRegister(qubits, name='qr')
    cr = ClassicalRegister(qubits, name='cr')
    anc = QuantumRegister(1, name='anc')
    n_anc = QuantumRegister(1, name='nanc')
    qc = QuantumCircuit(qr, cr, anc, n_anc, name='qc')
    # Set the secret marked element
    marked = [1, 1, 0]
    # Initialise the qubits in superposition:
    qc.h(qr)
    qc.barrier()
    # Calculate the required iteration count:
    for i in range(iters):
        qc.barrier()
        #oracle(qc, qr)
        conundrum.Grover_Oracle(marked, qc, qr, anc, n_anc)
        qc.barrier()
        #diffusion(qc, qr)
        conundrum.Grover_Diffusion(marked, qc, qr, anc, n_anc)
    return qc, qr, cr

#Calculate the required number of iterations:
iterations = round(math.pi/4*math.sqrt(N))

#Run the algorithm!
bucket_of_results = []
for i in range(1,10):
    qc, qr, cr = grover(i, N)
    qc.measure(qr, cr)
    run = execute(qc, M_simulator, shots=100)
    result = run.result()
    counts = result.get_counts(qc)
    s = conundrum.Measurement(qc, shots=100)
    pattern = "\d+\|\d+\>"
    result = re.findall(pattern, s)
    dct = {}
    for item in result:
        dct[item[item.index("|"):]] = int(item[:item.index("|")])
    bucket_of_results.append(dct)


show_figure(plot_histogram(bucket_of_results, bar_labels=False, figsize=(15,4)))
