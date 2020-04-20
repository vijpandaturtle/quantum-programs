import sys, time, math
from qiskit import QuantumCircuit, QuantumProgram

sys.path.append('../Config/')
import Qconfig
from qiskit.tools.visualization import plot_histogram

def input_phase(circuit, qubits):
    #Uncomment for A = 00
    #Comment for A = 11
    circuit.s(qubits[0])
    #circuit.s(qubits[1])
    return
