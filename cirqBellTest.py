import numpy as np
import cirq

''' === BELL INEQUALITY TEST === '''
''' Page 90, Section 7.4 of Hidary '''


def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)


def make_bell_test_circuit():
    # Create qubits for Alice, Bob and Referees
    alice = cirq.GridQubit(0, 0)
    bob = cirq.GridQubit(1, 0)
    alice_referee = cirq.GridQubit(0, 1)
    bob_referee = cirq.GridQubit(1, 1)
    circuit = cirq.Circuit()

    # Prepare shared entangled state between Alice & Bob
    circuit.append([
        cirq.H(alice),
        cirq.CNOT(alice, bob),
        cirq.X(alice) ** -0.25
    ])

    # Referees flip coins
    circuit.append([
        cirq.H(alice_referee),
        cirq.H(bob_referee)
    ])

    # Players do a sqrt(X) based on their ref's coin
    circuit.append([
        cirq.CNOT(alice_referee, alice) ** 0.5,
        cirq.CNOT(bob_referee, bob) ** 0.5
    ])

    # Results of game are recorded
    circuit.append([
        cirq.measure(alice, key='a'),
        cirq.measure(bob, key='b'),
        cirq.measure(alice_referee, key='x'),
        cirq.measure(bob_referee, key='y')
    ])

    return circuit


def main():
    # Create a circuit
    circuit = make_bell_test_circuit()
    print('Circuit:')
    print(circuit)

    # Run Simulations
    print()
    repetitions = 1000
    print('Simulating {} repetitions...'.format(repetitions))
    result = cirq.Simulator().run(program=circuit,
                                  repetitions=repetitions)

    # Collect Results
    a = np.array(result.measurements['a'][:, 0])
    b = np.array(result.measurements['b'][:, 0])
    x = np.array(result.measurements['x'][:, 0])
    y = np.array(result.measurements['y'][:, 0])

    # Compute the winning percentages
    outcomes = a ^ b == x & y
    win_percent = len([e for e in outcomes if e]) * 100 / repetitions

    # Print Data
    print()
    print('Results')
    print('a:', bitstring(a))
    print('b:', bitstring(b))
    print('x:', bitstring(x))
    print('y:', bitstring(y))
    print('(a XOR b) == (x AND y):\n ', bitstring(outcomes))
    print('Win rate: {}%'.format(win_percent))


if __name__ == '__main__':
    main()
    