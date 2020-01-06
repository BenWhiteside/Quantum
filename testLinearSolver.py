from qiskit.aqua import run_algorithm
from qiskit.aqua.input import LinearSystemInput
from qiskit.quantum_info import state_fidelity
from qiskit.aqua.algorithms.classical import ExactLSsolver
import numpy as np

params = {
    'problem': {
        'name': 'linear_system'
    },
    'algorithm': {
        'name': 'HHL'
    },
    'eigs': {
        'expansion_mode': 'suzuki',
        'expansion_order': 2,
        'name': 'EigsQPE',
        'num_ancillae': 3,
        'num_time_slices': 50
    },
    'reciprocal': {
        'name': 'Lookup'
    },
    'backend': {
        'provider': 'qiskit.BasicAer',
        'name': 'statevector_simulator'
    }
}

def fidelity(hhl,ref):
    solution_hhl_normed = hhl / np.linalg.norm(hhl)
    solution_ref_normed = ref / np.linalg.norm(ref)
    fidelity = state_fidelity(solution_hhl_normed,solution_ref_normed)
    print("fidelity %f" % fidelity)

matrix = [[1,0],[0,2]]
vector = [1,4]

params['input'] = {
    'name': 'LinearSystemInput',
    'matrix': matrix,
    'vector': vector
}

result = run_algorithm(params)
print("solution ", np.round(result['solution'],5))

result_ref = ExactLSsolver(matrix,vector).run()
print("classical solution ", np.round(result_ref['solution'],5))

print("probability %f" % result['probability_result'])
fidelity(result['solution'], result_ref['solution'])
