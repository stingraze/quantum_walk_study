import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import networkx as nx

def quantum_crawler(steps, num_sites):
    # Calculate number of qubits needed for position
    pos_qubits = int(np.ceil(np.log2(num_sites)))
    
    # Create quantum registers
    position = QuantumRegister(pos_qubits, 'position')
    coin = QuantumRegister(1, 'coin')
    c = ClassicalRegister(pos_qubits, 'measurement')

    # Create quantum circuit
    qc = QuantumCircuit(position, coin, c)

    # Initialize superposition state for position
    qc.h(position)

    # Quantum Walk
    for _ in range(steps):
        # Coin flip
        qc.h(coin)
        
        # Controlled movement based on coin state
        for i in range(pos_qubits):
            qc.cx(coin[0], position[i])
        
        # Flip coin state to prepare for next step
        qc.x(coin)

    # Measure position
    qc.measure(position, c)

    return qc

def plot_graph_with_probabilities(probabilities, num_sites):
    G = nx.cycle_graph(num_sites)
    pos = nx.circular_layout(G)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=16, font_weight='bold')
    
    # Add probability labels
    labels = {i: f"{i}\n{probabilities.get(i, 0):.4f}" for i in range(num_sites)}
    nx.draw_networkx_labels(G, pos, labels, font_size=14)
    
    edge_labels = {(u, v): f"{abs(u-v)}" for (u, v) in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    
    plt.title(f"Quantum Crawler on {num_sites}-site Graph (Steps: {steps})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Set up the quantum crawler
steps = 10
num_sites = 5
qc = quantum_crawler(steps, num_sites)

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
    print(f"Site {position}: Probability {prob:.4f}")

# Plot the histogram
plot_histogram(counts)
plt.title(f"Quantum Crawler Results (Steps: {steps}, Sites: {num_sites})")
plt.xlabel("Site")
plt.ylabel("Counts")
plt.show()

# Plot the graph with probabilities
plot_graph_with_probabilities(probabilities, num_sites)