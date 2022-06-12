from turtle import back
from unittest.mock import NonCallableMagicMock
from matplotlib import backend_bases
from matplotlib.pyplot import title
import qiskit
from qiskit.algorithms import Shor
from qiskit import IBMQ, BasicAer, QuantumCircuit, Aer, execute, transpile, assemble
from qiskit.tools.visualization import plot_histogram
import numpy as np
from qiskit.providers.aer import QasmSimulator

simulator = QasmSimulator()

def modFunc(r, power):                      
    #Funktion welche die verschiedenen Varianten der Gleichung x^r ≡ 1 mod N prüft für Werte von r
    # bestimmt die Ordnung von r von x in der primen Restklassengruppe 
    circuit = QuantumCircuit(4)
    for iteration in range(power):
        circuit.swap(2,3)                   #nutzt swap Gatter um Eingangs Qubits zu vertauschen
        circuit.swap(1,2)
        circuit.swap(0,1)
        for q in range(4):                  #dreht das Eingangs Qubit um pi/2 um die X-Achse, auch als Not Gatter bezeichnet
            circuit.x(q)
    circuit=circuit.to_gate()               #verwandelt Schaltung zu einem Gatter
    circuit.name="%i^%i mod 15" %(a,power)
    circuit_2 = circuit.control()
    return circuit_2

n_count = 8                                 #Anzahl Qubits 
a = 7

def qft(n):                                 
    #Funktion die, die Quanten-Fouriertransformation ausführt bzw. als Gatter erzeugt
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)),m,j)
        qc.h(j)
    qc.name="Quantum Fourier Transform"
    return qc

    
qc = QuantumCircuit(n_count + 4,n_count)

for q in range(n_count):                    
    #Anwenden des Hadamard-Gatters auf alle 8 Qubits die ich für modFunc benutzen will
    qc.h(q)

qc.x(3+n_count)

for q in range(n_count):
    #fügt modFunc, also die Gatter zu unseren 8 Qubits hinzu
    qc.append(modFunc(a,2**q), [q]+[i+n_count for i in range(4)])

qc.append(qft(n_count), range(n_count))
    #fügt Quanten-Fouriertransformation nach modFunc hinzu

qc.measure(range(n_count), range(n_count))
qc.draw(output='mpl', filename='circuit')
    #Zeichnet unsere Schaltung und speichert Sie als Bild (circuit.png) ab

     
simulator = BasicAer.get_backend('qasm_simulator')
qc = transpile(qc, simulator)

result = simulator.run(qc).result()
counts = result.get_counts(qc)
hist = plot_histogram(counts, title='Shors Algorithmus Wahrscheinlichkeiten')
hist.savefig('histogram.png', bbox_inches='tight')