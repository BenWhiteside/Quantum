# Quantum Teleportation in Cirq
# See pg 85 of Hidary

import random
import cirq

def make_quantum_teleportation_circuit(ranX, ranY):
    # Returns a quantum teleportation circuit
    circuit = cirq.Circuit()
    msg, alice, bob = cirq.LineQubit.range(3)

    # Create a Bell State to be shared between Alice and Bob
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])

    # Create a random state for the Message
    circuit.append([cirq.X(msg)**ranX, cirq.Y(msg)**ranY])

    # Bell measurement of the Message and Alice's entangled qubit
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circuit.append(cirq.measure(msg, alice))

    # Uses the two classical bits from the Bell Measurement
    # to recover the original quantum message that is on
    # Bob's entangled qubit.
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])

    return msg, circuit

def main():
    # Encode a random state to teleport
    ranX = random.random()
    ranY = random.random()
    msg, circuit = make_quantum_teleportation_circuit(ranX, ranY)

    # Simulate the circuit
    sim = cirq.Simulator()
    message = sim.simulate(cirq.Circuit.from_ops(
        [cirq.X(msg)**ranX, cirq.Y(msg)**ranY]))

    # Display the teleportation circuit
    print("\nCircuit:")
    print(circuit)

    # Print the Bloch sphere of Alice's qubit
    print("Bloch Sphere of Alice's qubit:")
    b0X, b0Y, b0Z = cirq.bloch_vector_from_state_vector(
        message.final_state, 0)
    print("x: ", round(b0X, 4),
          "y: ", round(b0Y, 4),
          "z: ", round(b0Z, 4))

    # Record the final state of the simulation
    final_results = sim.simulate(circuit)

    # Print the Bloch sphere of Alice's qubit
    print("Bloch Sphere of Bob's qubit:")
    b2X, b2Y, b2Z = cirq.bloch_vector_from_state_vector(
        final_results.final_state, 2)
    print("x: ", round(b2X, 4),
          "y: ", round(b2Y, 4),
          "z: ", round(b2Z, 4))

if __name__ == '__main__':
    main()
