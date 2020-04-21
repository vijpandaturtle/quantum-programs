import sys
import qiskit
import logging
from qiskit import QuantumProgram

def main():
    qp = QuantumProgram()
    #Create 1 qubit
    quantum_r = qp.create_quantum_register("qr",1)
    #Create 1 classical register
    classical_r = qp.create_classical_register("cr",1)
    #Create a circuit
    qp.create_circuit("Circuit", [quantum_r], [classical_r])
    #Get the circuit by name
    circuit = qp.get_circuit('Circuit')
    #enable logging
    qp.enable_logs(logging.DEBUG);
    #pauliX gate
    circuit.x(quantum_r[0])
    #measure gate from qubit 0 to classical bit 0
    circuit.measure(quantum_r[0], classical_r[0])

    #backend simulator
    backend = 'local_qasm_simulator'
    #circuits to execute
    circuits = ['Circuit']
    #Compile the program
    qobj = qp.compile(circuits, backend)
    #run simulator
    result = qp.run(qobj, timeout=240)
    #Show result counts
    print(str(result.get_counts('Circuit')))

if __name__ = '__main__':
    main()
