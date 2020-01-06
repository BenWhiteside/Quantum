import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ, compile
from qiskit.circuit import QuantumRegister, QuantumCircuit, Qubit, ClassicalRegister
from qiskit import (Aer, execute)
from qiskit.visualization import plot_histogram

def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)

def nBitQFT(q,c,n):
    circuit = QuantumCircuit(q,c)
    for k in range(n):
        j = n-k
        # Perform Hadamard on qubit j-1
        circuit.h(q[j-1])
        for i in reversed(range(j-1)):
            circuit.cu1(2 * np.pi / 2**(j-i), q[i], q[j-1])
    # Finally we need to swap the qubits
    for i in range(n//2):
        circuit.swap(q[i],q[n-i-1])

    return circuit

def qftMatrix(n):
    qft = np.zeros([2**n,2**n], dtype=complex)
    for i in range(2**n):
        for j in range(2**n):
            qft[i,j] = np.exp(i*j*2*1j*np.pi/(2**n))

    return 1/np.sqrt(2**n)*qft

def testCircuit(n):
    q = QuantumRegister(n,"x")
    c = ClassicalRegister(n,"c")
    circuit = nBitQFT(q,c,n)
    backend = Aer.get_backend('unitary_simulator')
    job = execute(circuit,backend)
    actual = job.result().get_unitary()
    expected = qftMatrix(n)
    delta = actual - expected

    print("Deviation: ", round(np.linalg.norm(delta),10))

    return circuit


''' Main Program '''
circuit = testCircuit(n=4)

n=4
q = QuantumRegister(n,"x")
c = ClassicalRegister(n,"c")
qftCircuit = nBitQFT(q,c,n)
initCircuit = QuantumCircuit(q,c)
for i in range(n):
    initCircuit.h(q[i])
initCircuit.barrier(q)
circuit = initCircuit+qftCircuit
circuit.barrier(q)
circuit.measure(q,c)

# Execute the circuit on the QASM Simulator
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)

# Get Results
result = job.result()

# Plot Results
counts = job.result().get_counts()
plot_histogram(counts);
show_figure(plot_histogram(result.get_counts(circuit)))
show_figure()

# Test on real hardware
IBMQ.load_accounts()
backend = IBMQ.get_backend('ibmq_16_melbourne')
print("Status of backend: ", backend.status())
from qiskit import compile
qobj = compile(circuit, backend=backend, shots=1024)

