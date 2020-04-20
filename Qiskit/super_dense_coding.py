import sys, time, math
from qiskit import QuantumCircuit, QuantumProgram

sys.path.append('../Config/')
import Qconfig
from qiskit.tools.visualization import plot_histogram

def main():
    Q_program = QuantumProgram()
    Q_program.register(Qconfig.APItoken, Qconfig.config["url"])
    #Creating registers
    q = Q_program.create_quantum_register("q", 2)
    c = Q_program.create_classical_register("c", 2)
    #Quantum circuit to make shared entangled state
    superdense = Q_program.create_circuit("superdense", [q], [c])
    #Party A : Alice
    superdense.h(q[0])
    superdense.cx(q[0], q[1])
    #00:do nothing, 10:apply x, 01:apply z
    superdense.x(q[0])
    superdense.z(q[0])
    #11:apply zx
    superdense.z(q[0])
    superdense.x(q[0])
    superdense.barrier()

    #Party B : Bob
    superdense.cx(q[0], q[1])
    superdense.h(q[0])
    superdense.measure(q[0], c[0])
    superdense.measure(q[1], c[1])

    circuits = ["superdense"]
    print(Q_program.get_qasms(circuits)[0])

    backend = "ibmq_qasm_simulator"
    shots = 1024

    result = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=3, timeout=240)

    print("Counts:" + str(result.get_counts("superdense")))
    plot_histogram(result.get_counts("superdense"))


if __name__ = '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
