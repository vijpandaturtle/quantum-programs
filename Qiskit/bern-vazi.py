from qiskit import *
from qiskit.tools.visualization import plot_histogram

#secret number
secretnumber = '101001'
#6+1 qubits, 6 classical bits
circuit = QuantumCircuit(6+1, 6)
circuit.h(range(len(secretnumber)))
circuit.x(len(secretnumber))
circuit.h(len(secretnumber))

circuit.barrier()

for ii, yesno in enumerate(reversed(secretnumber)):
    if yesno='1':
        circuit.cx(ii, len(secretnumber))

circuit.barrier()
circuit.h(range(len(secretnumber)))
circuit.measure(range(len(secretnumber)), range(len(secretnumber)))

circuit.draw(output='mp1')

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots=1).result()
counts = result.get_counts()

print(counts)
