#(C)Tsubasa Kato 2024 - 6/24/2024 14:11PM
# Made with Perplexity AI.
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def quantum_walk(steps):
    # Create quantum registers
    position = QuantumRegister(3, 'position')  # 3 qubits for 8 positions
    coin = QuantumRegister(1, 'coin')
    c = ClassicalRegister(3, 'measurement')

    # Create quantum circuit
    qc = QuantumCircuit(position, coin, c)

    # Initialize superposition state for position
    qc.h(position)

    # Quantum Walk
    for _ in range(steps):
        # Coin flip
        qc.h(coin)
        
        # Controlled shift based on coin state
        for i in range(3):
            qc.cx(coin[0], position[i])
        
        # Flip coin state to prepare for next step
        qc.x(coin)

    # Measure position
    qc.measure(position, c)

    return qc

# Set up the quantum walk
steps = 5
qc = quantum_walk(steps)

# Run the simulation
simulator = AerSimulator()
job = simulator.run(qc, shots=10000)
result = job.result()
counts = result.get_counts(qc)

# Process and display results
processed_counts = {int(state, 2): count for state, count in counts.items()}
total_counts = sum(processed_counts.values())
probabilities = {position: count / total_counts for position, count in processed_counts.items()}

# Print probabilities
for position, prob in sorted(probabilities.items()):
    print(f"Position {position}: Probability {prob:.4f}")

# Plot the results
plt.figure(figsize=(12, 6))
plot_histogram(counts)
plt.title(f"Quantum Walk Results (Steps: {steps})")
plt.xlabel("Position")
plt.ylabel("Counts")
plt.show()