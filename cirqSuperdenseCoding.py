# Superdense coding in cirq
# pg. 87 from Hidary

import cirq

# Helper function for visualising output
def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)

# Create two quantum and classical registers
qreqister = [cirq.LineQubit(x) for x in range(2)]
circ = cirq.Circuit()

# Dictionary of operations for each message
message = {"00": [],
           "01": [cirq.X(qreqister[0])],
           "10": [cirq.Z(qreqister[0])],
           "11": [cirq.X(qreqister[0]),
                  cirq.Z(qreqister[0])]}

# Alice creates a Bell pair:
circ.append(cirq.H(qreqister[0]))
circ.append(cirq.CNOT(qreqister[0], qreqister[1]))

# Alice picks a message to send:
m = "01"
print("Alice's sent message =", m)

# Alice encodes her message with the appropriate quantum operations:
circ.append(message[m])

# Bob measures in the Bell basis
circ.append(cirq.CNOT(qreqister[0], qreqister[1]))
circ.append(cirq.H(qreqister[0]))
circ.append([cirq.measure(qreqister[0]), cirq.measure(qreqister[1])],strategy=cirq.InsertStrategy.NEW_THEN_INLINE)

# Print the circuit
print("\nCircuit:")
print(circ)

# Run the quantum circuit on the Simulator backend
sim = cirq.Simulator()
res = sim.run(circ, repetitions=1)

# Print out Bob's received message
print("\nBob's received message =",
      bitstring(res.measurements.values()))


