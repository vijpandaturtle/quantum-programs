import sys, time, math
import numpy as np
from qiskit import QuantumCircuit, QuantumProgram

sys.path.append('../Config/')
import Qconfig
from qiskit.tools.visualization import plot_histogram

def main():
    Q_program = QuantumProgram()
    Q_program.register(Qconfig.APItoken, Qconfig.config["url"])

    #Create registers
    q = Q_program.create_quantum_register('q', 3)
    c0 = Q_program.create_classical_register('c0', 1)
    c1 = Q_program.create_classical_register('c1', 1)
    c0 = Q_program.create_classical_register('c2', 1)

    #Quantum circuit to make Bell Pair
    teleport = Q_program.create_circuit('teleport', [q], [c0, c1, c2])
    teleport.h(q[1])
    teleport.cx(q[1], q[2])

    #A prepares quantum state to be teleported
    teleport.ry(np.pi/4, q[0])
    #A applies CNOT to her two quantum states followed by H to entangle them
    teleport.cx(q[0], q[1])
    teleport.h(q[0])
    teleport.barrier()
    #A measures her two quantum states
    teleport.measure(q[0], c0[0])
    teleport.measure(q[1], c1[0])

    circuits = ['teleport']
    print(Q_program.get_qasms(circuits)[0])

    #B depending on the result applies x or z or both
    teleport.z(q[2]).c_if(c0,1)
    teleport.x(q[2]).c_if(c1,1)

    teleport.measure(q[2], c2[0])

    #dump asm
    circuits = ['teleport']
    print(Q_program.get_qasms(circuits)[0])

    backend = "ibmq_qasm_simulator"
    shots = 1024
    result = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=3, timeout=240)

    print("Counts:" + str(result.get_counts("teleport")))

    #RESULTS
    #Alice's measurements
    data = result.get_counts("teleport")
    alice = {}
    alice['00'] = data['0 0 0'] + data['1 0 0']
    alice['10'] = data['0 1 0'] + data['1 1 0']
    alice['01'] = data['0 0 1'] + data['1 0 1']
    alice['11'] = data['0 1 1'] + data['1 1 1']
    plot_histogram(alice)

    bob = {}
    bob['0'] = data['0 0 0'] + data['0 1 0'] + data['0 0 1'] + data['0 1 1']
    bob['1'] = data['1 0 0'] + data['1 1 0'] + data['1 0 1'] + data['1 1 1']
    plot_histogram(bob)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
