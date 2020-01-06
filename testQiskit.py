import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from qiskit import (QuantumCircuit, execute, Aer)
from qiskit.visualization import plot_histogram

def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)

# Use Aer
simulator = Aer.get_backend('qasm_simulator')

# Create a Simple Quantum Circuit acting on the qubit register
circuit = QuantumCircuit(2,2)

# Add a Hadamard Gate on qubit 0
circuit.h(0)

# Add a CNOT gate on control qubit 0 and target qubit 1
circuit.cx(0,1)

# Add a measurement at the end to convert in to classical bits
circuit.measure([0,1],[0,1])

# Plot Circuit
diagram = circuit.draw(output='mpl') #output='mpl', output='latex', scale=0.5
show_figure(diagram)
#diagram.savefig("testQiskit.svg",format="svg")

# Execute the circuit on the QASM Simulator
job = execute(circuit, simulator, shots=10000)

# Get Results
result = job.result()

# Return results
counts = result.get_counts(circuit)
print('\nTotal count for 00 and 11 are:', counts)
plot_histogram(counts);
show_figure(plot_histogram(result.get_counts(circuit)))