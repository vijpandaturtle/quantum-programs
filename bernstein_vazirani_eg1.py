from qiskit import *
from qiskit.tools.visualization import plot_histogram

#secret number
secretnumber = '101001'
#6+1 qubits, 6 classical bits
circuit = QuantumCircuit(6+1, 6)
circuit.h([0,1,2,3,4,5])
circuit.x(6)
circuit.h(6)

circuit.barrier()

#depicting 1 and 0 bits
circuit.cx(5, 6)
circuit.cx(3, 6)
circuit.cx(0, 6)

circuit.barrier()
circuit.h([0,1,2,3,4,5])
circuit.measure([0,1,2,3,4,5], [0,1,2,3,4,5])

circuit.draw(output='mp1')

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots=1).result()
counts = result.get_counts()

print(counts)
