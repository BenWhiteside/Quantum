# REFERENCE:
# www.medium.com/analytics-vidhya/quantum-machine-learning-inference-on-bayesian-networks-351f242816e8
from numpy import arcsin, sqrt, pi

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer
from qiskit import execute


def probToAngle(prob):
    """
    Converts a given probability value into an equivalent angle (theta) value.
    :param prob:
    :return:
    """
    return 2 * arcsin(sqrt(prob))


qr = QuantumRegister(4, 'qreg')
cr = ClassicalRegister(3, 'creg')

circ = QuantumCircuit(qr, cr, name='circ')

"""
Evidence is given by: E = (P = 1). We aim to find P(H=0|P=1)?
Experimental data is given by the Probability Table:

    | P 
---------
P=0 | 0.65
P=1 | 0.35

P(E|P) | E=0   E=1
---------------------
P=0    | 0.73  0.27
P=1    | 0.24  0.76

P(H|E) | H=0   H=1
---------------------
E=0    | 0.61  0.39
E=1    | 0.18  0.82
 
"""

# The circuit to represent the probability p variable.
circ.u(probToAngle(0.35), 0, 0, qr[0])

# Since we have p=1, we use the second row of the probability table for the evidence variable E
circ.u(probToAngle(0.76), 0, 0, qr[1])

# Setting up the qubit representing H assuming that E = 0.
circ.u(probToAngle(0.39), 0, 0, qr[2])

"""
To make sure we sample from a state with correct Evidence, we use Quantum Amplitude
Amplification (QAA), designing the Oracle that flips the signs of states with evidence
that matches ours:
"""


def oracle(circuit):
    """
    Implements an oracle that flips the sign of states that contain P = 1.
    :param circuit:
    :return: circuit
    """
    circuit.cu(pi, pi, 0, 0, qr[0], qr[1])
    circuit.cu(pi, pi, 0, 0, qr[0], qr[1])

    return circuit


def u_gate(circuit):
    """
    Implements the unitary U gate that flips states about the average amplitude.
    :param circuit:
    :return: circuit
    """
    # Implements the quantum circuit that converts \psi -> |0...0> to the all-zeroes state:
    # circ.u3(theta, phi, lambda, label=None)
    circuit.u3(-1 * probToAngle(0.35), 0, 0, qr[0])
    circuit.u3(-1 * probToAngle(0.76), 0, 0, qr[1])
    circuit.u3(-1 * probToAngle(0.39), 0, 0, qr[2])

    # Flipping the all-zeroes state |0...0> using a triple-controlled Z-gate conditioned
    # on P, E and H, and applied to the ancilla.
    circuit.x(qr)
    circuit.cu1(pi / 4, qr[0], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(-pi / 4, qr[1], qr[3])
    circuit.cx(qr[0], qr[1])
    circuit.cu1(pi / 4, qr[1], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi / 4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi / 4, qr[2], qr[3])
    circuit.cx(qr[1], qr[2])
    circuit.cu1(-pi / 4, qr[2], qr[3])
    circuit.cx(qr[0], qr[2])
    circuit.cu1(pi / 4, qr[2], qr[3])
    circuit.x(qr)

    # Implements the quantum circuit that transforms back: |0...0> -> \psi
    circuit.u(probToAngle(0.35), 0, 0, qr[0])
    circuit.u(probToAngle(0.76), 0, 0, qr[1])
    circuit.u(probToAngle(0.39), 0, 0, qr[2])

    return circuit


"""
We now apply Grover's iterate twice, and then set up H - to do that we need to first
measure the Evidence E, and then rotate H conditionally. After that, we can sample
from our quantum register through a measurement.
"""
# Apply the Oracle and the U-gate twice:
circ = oracle(circ)
circ = u_gate(circ)
circ = oracle(circ)
circ = u_gate(circ)
circ.x(qr[0])

# Measure E, and rotate H to the p(1) value in the second row of P(H|E) table,
# conditioned on E.
circ.measure(qr[1], cr[1])
circ.u(probToAngle(0.82) - probToAngle(0.39), 0, 0, qr[2])

# Sample by measuring the rest of the qubits:
circ.measure(qr[0], cr[0])
circ.measure(qr[2], cr[2])

"""
Finally, the calculate P(H=0|P=1), we run the above job multiple times,
generating a new sample with every run, and throwing away samples with
incorrect Evidence.
"""
# Get the backend from the Aer provider.
backend = Aer.get_backend('qasm_simulator')

# Run the Job
samples_list = []
n_samples = 256

for i in range(n_samples):
    job = execute(circ, backend=backend, shots=1)
    result = list(job.result().get_counts(circ).keys())[0]
    if result[2] == '1':
        samples_list.append(result)

# Printing the number of useful samples and percentage of samples rejected.
print()
print(n_samples, 'samples drawn:', len(samples_list), 'samples accepted: ', n_samples - len(samples_list),
      'samples rejected.')
print('Percentage of samples rejected: ', 100 * (1 - (len(samples_list) / n_samples)), '%')

# Computing P(H=0|P=1)
p_H = 0

for i in samples_list:
    if i[0] == '0':
        p_H += 1

# Normalisation:
p_H /= len(samples_list)

print('P(H=0|P=1) =', p_H)
print()
