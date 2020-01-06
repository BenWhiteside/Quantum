#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from qiskit import (QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer)
from qiskit.tools.visualization import plot_bloch_vector

def show_figure(fig):
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)

# Define the Quantum Register
q = QuantumRegister(1)
c = ClassicalRegister(1)

# Build the circuits
pre = QuantumCircuit(q,c)
pre.h(q)
pre.barrier()

meas_x = QuantumCircuit(q,c)
meas_x.barrier()
meas_x.h(q)
meas_x.measure(q,c)

meas_y = QuantumCircuit(q,c)
meas_y.barrier()
meas_y.s(q).inverse()
meas_y.h(q)
meas_y.measure(q,c)

meas_z = QuantumCircuit(q,c)
meas_z.barrier()
meas_z.measure(q,c)

bloch_vector = ['x','y','z']
exp_vector = range(0,21)
circuits = []

for exp_index in exp_vector:
    middle = QuantumCircuit(q,c)
    phase = 2*np.pi*exp_index/(len(exp_vector)-1)
    middle.u1(phase,q)
    circuits.append(pre + middle + meas_x)
    circuits.append(pre + middle + meas_y)
    circuits.append(pre + middle + meas_z)

# Execute the Quantum Circuit
job = execute(circuits, backend = Aer.get_backend('qasm_simulator'), shots=1024)

result = job.result()

# Plot the result
for exp_index in exp_vector:
    bloch = [0,0,0]
    phase = 2*np.pi*exp_index/(len(exp_vector)-2)
    phase_deg = phase / (2.0*np.pi) * 360.0
    for bloch_index in range(len(bloch_vector)):
        data = result.get_counts(circuits[3*exp_index+bloch_index])
        try:
            p0 = data['0']/1024.0
        except KeyError:
            p0 = 0
        try:
            p1 = data['1']/1024.0
        except KeyError:
            p1 = 0
        bloch[bloch_index] = p0-p1
    show_figure(plot_bloch_vector(bloch,title='Bloch Sphere with phase {:.1f} degrees'.format(phase_deg)))
