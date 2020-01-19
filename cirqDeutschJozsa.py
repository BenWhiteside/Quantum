""" The Deutsch-Josza Algorithm on 3 qubits """
import cirq

""" Pg 103, Section 8.1 of Hidary """

# Get 3 qubits, two for data and one for target
q0, q1, q2 = cirq.LineQubit.range(3)

# Oracles for constant functions
constant = ([], [cirq.X(q2)])

# Oracles for balanced functions
balanced = ([cirq.CNOT(q0, q2)],
            [cirq.CNOT(q1, q2)],
            [cirq.CNOT(q0, q2)],
            [cirq.CNOT(q1, q2)],
            [cirq.CNOT(q0, q2)],
            [cirq.X(q2)],
            [cirq.CNOT(q1, q2)],
            [cirq.X(q2)],
            [cirq.CNOT(q0, q2)],
            [cirq.CNOT(q1, q2)],
            [cirq.X(q2)])


def your_circuit(oracle):
    # Phase kickback
    yield cirq.X(q2), cirq.H(q2)

    # Superposition over input bits
    yield cirq.H(q0), cirq.H(q1)

    # Query the function
    yield oracle

    # Interference to get result,
    # put last qubit in to |1> state
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2)

    # A final OR gate to put the result
    # in to the final qubit
    yield cirq.X(q0), cirq.X(q1), cirq.CCX(q0, q1, q2)

    # Perform measurement
    yield cirq.measure(q2)


# Get a backend
simulator = cirq.Simulator()

# Execute circuit for oracles of constant functions
print('Your result on constant functions:')
for oracle in constant:
    result = simulator.run(cirq.Circuit.from_ops(your_circuit(oracle)),
                           repetitions=10)
    print(result)

# Execute circuit for oracles of balanced functions
print('Your result on balanced functions')
for oracle in balanced:
    result = simulator.run(cirq.Circuit.from_ops(your_circuit(oracle)),
                           repetitions=10)
    print(result)
