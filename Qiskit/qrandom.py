import sys, time
import qiskit
import logging
from qiskit import QuantumProgram

#Q experience config
sys.path.append('../Config/')
import Qconfig

#Generate a 2**n bit random number
def qrandom(n):
    #create a program
    qp = QuantumProgram()
    #create n qubits
    quantum_r = qp.create_quantum_register("qr", n)
    classical_r = qp.create_classical_register("cr", n)
    #Create circuit
    circuit = qp.create_circuit("QRND", [quantum_r], [classical_r])

    #Hadamard gate to all input qubits
    for i in range(n):
        circuit.h(quantum_r[i])

    #measure qubit and store in classical reg
    for i in range(n):
        circuit.measure(quantum_r[i], classical_r[i])

    #backend simulator
    backend = 'ibm_qasm_simulator'
    circuits = ['QRND']

    print(qp.get_qasm('Circuit'))
    qobj = qp.compile(circuits, backend)
    print(str(qobj))

    qp.set_api((Qconfig.APItoken, Qconfig.config['url'])
    result = qp.execute(circuits, backend, shots=1024, max_credits=3, timeout=240)

    #Show result counts
    counts = result.get_counts('QRND')

    bits = ""
    for v in counts.values():
        if v > shots/(2**n):
            bits += "1"
        else:
            bits += "0"

    return int(bits, 2)

    if __name__ == '__main__':
        start_time = time.time()
        size = 10
        qubits = 3 # bits = 2**qubits

        for i in range(size):
            n = qrng(qubits)
            numbers.append(n)

        print("list=" + str(numbers))
        print("--- %s seconds ---" % (time.time() - start_time))
