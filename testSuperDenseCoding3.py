import matplotlib as mpl
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr
from qiskit import ClassicalRegister as cr

mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show()


# Setup of basic 2-qubit register and circuit
# Create two registers: one quantum, one classical
q = qr(2, 'q')
c = cr(2, 'c')
circuit = qc(q, c)


def create_bell_pair(qc, q, q0, q1):
    qc.h(q[q0])  # Apply a Hadamard to the first qubit.
    qc.cx(q[q0], q[q1])  # Apply a CNOT, controlled on the first qubit.


def inverse_bell_pair(qc, q, q0, q1):
    qc.cx(q[q0], q[q1])
    qc.h(q[q0])


def encoder(qc, q, q0, message_to_encode):
    if message_to_encode == "00":
        pass  # do nothing
    elif message_to_encode == "10":
        qc.x(q[q0])  # Apply the X gate.
    elif message_to_encode == "01":
        qc.z(q[q0])  # Apply the Z gate.
    elif message_to_encode == "11":
        qc.z(q[q0])  # Apply the Z gate, then
        qc.z(q[q0])  # apply the X gate.
    else:
        print("Invalid message! Will just send '00'.")


# Main Program #
create_bell_pair(circuit, q, 0, 1)
circuit.barrier()

# Qubit 0 goes to Alice, and qubit 1 goes to Bob

# Alice wants to send the message:
message_to_send = "11"

# Encode the message:
encoder(circuit, q, 0, message_to_send)
circuit.barrier()

# Alice sends her 1 qubit to Bob.

# Bob receives 1 qubit and decodes it:
inverse_bell_pair(circuit, q, 0, 1)
circuit.barrier()

circuit.measure(q, c)
# Plot Circuit
diagram = circuit.draw(output='mpl')  # output='mpl', output='latex', scale=0.5
show_figure(diagram)
