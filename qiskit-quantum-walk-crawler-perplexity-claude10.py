#(C)Tsubasa Kato - 2024/6/25 8:03AM JST - Inspire Search Corporation - https://www.inspiresearch.io/en
#Created with the help of Perplexity AI, Claude. Tested to work on Qiskit 1.1.0. 
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import networkx as nx

def quantum_crawler(steps, adjacency):
    num_sites = len(adjacency)
    pos_qubits = int(np.ceil(np.log2(num_sites)))
    position = QuantumRegister(pos_qubits, 'position')
    coin = QuantumRegister(1, 'coin')
    c = ClassicalRegister(pos_qubits, 'measurement')
    qc = QuantumCircuit(position, coin, c)

    # Initialize superposition state for position
    qc.h(position)

    for _ in range(steps):
        # Coin flip
        qc.h(coin)

        # Controlled movement based on coin state and adjacency
        for i in range(num_sites):
            for j in adjacency[i]:
                if i != j:
                    # Calculate the differing bits
                    diff = i ^ j  # XOR to find different bits
                    for k in range(pos_qubits):
                        if (diff >> k) & 1:
                            # Apply CNOT only for the differing bit
                            qc.cx(coin[0], position[k])

        # Reset coin state
        qc.reset(coin)

    qc.measure(position, c)
    return qc

def plot_graph_with_probabilities(probabilities, adjacency):
    G = nx.Graph()
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=16, font_weight='bold')
    labels = {i: f"{i}\n{probabilities.get(i, 0):.4f}" for i in range(len(adjacency))}
    nx.draw_networkx_labels(G, pos, labels, font_size=14)
    plt.title(f"Quantum Crawler on Custom Graph (Steps: {steps})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Define a custom adjacency structure for a 5-node graph
adjacency = {
    0: [1, 2, 3],
    1: [0, 2, 4],
    2: [0, 1, 3, 4],
    3: [0, 2, 4],
    4: [1, 2, 3]
}

steps = 10
qc = quantum_crawler(steps, adjacency)
# Run the simulation
simulator = AerSimulator()
job = simulator.run(qc, shots=10000)
result = job.result()
counts = result.get_counts(qc)


processed_counts = {int(state, 2): count for state, count in counts.items()}
total_counts = sum(processed_counts.values())
probabilities = {position: count / total_counts for position, count in processed_counts.items()}

for position, prob in sorted(probabilities.items()):
    print(f"Site {position}: Probability {prob:.4f}")

plot_histogram(counts)
plt.title(f"Quantum Crawler Results (Steps: {steps})")
plt.xlabel("Site")
plt.ylabel("Counts")
plt.show()

plot_graph_with_probabilities(probabilities, adjacency)
