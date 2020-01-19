import matplotlib as mpl
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr
from qiskit import ClassicalRegister as cr
from qiskit import execute, Aer
from qiskit.visualization import plot_histogram
from datetime import datetime

mpl.use('TkAgg')


def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)


# Use Aer
backend = Aer.get_backend('qasm_simulator')
print('Provider: ', backend)

# Create two registers: one quantum, one classical
q = qr(2, 'q')
c = cr(2, 'c')
circuit = qc(q, c)

# Add a Hadamard gate on q0 to create superposition
circuit.h(q[0])

# Add a CNOT gate control on q0 with q2 target
# to create an entangled pair:
circuit.cx(q[0], q[1])

# Add a X gate to q0 to encode message:
# | Message | Pauli Gate | Measurement
# | 00      | iden       | 00 (100%)
# | 01      | Z          | 01 (100%)
# | 10      | X          | 10 (100%)
# | 11      | XZ         | 11 (100%)
circuit.z(q[0])
# circuit.x(q[0])
# circuit.iden(q[0])

# Add another CNOT gate as before to entangle
# the encoded message and q1:
circuit.cx(q[0], q[1])

# Apply another Hadamard gate to q0 to take
# it out of superposition:
circuit.h(q[0])

# Add a measurement gate to obtain the measurement
circuit.barrier()
circuit.measure(q, c)

# Plot Circuit
diagram = circuit.draw(output='mpl')  # output='mpl', output='latex', scale=0.5
show_figure(diagram)

# Execute the circuit on the QASM Simulator
start_time = datetime.now()
job = execute(circuit, backend, shots=100000)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# Get Results
result = job.result()

# Return results
counts = result.get_counts(circuit)
print('\nTotal count for 00 and 11 are:', counts)
plot_histogram(counts);
show_figure(plot_histogram(result.get_counts(circuit)))
