import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def quantum_crawler(steps, grid_size):
    # Calculate number of qubits needed for position
    pos_qubits = int(np.ceil(np.log2(grid_size**2)))
    
    # Create quantum registers
    position = QuantumRegister(pos_qubits, 'position')
    direction = QuantumRegister(2, 'direction')  # 2 qubits for 4 directions
    c = ClassicalRegister(pos_qubits, 'measurement')

    # Create quantum circuit
    qc = QuantumCircuit(position, direction, c)

    # Initialize superposition state for position
    qc.h(position)

    # Quantum Walk
    for _ in range(steps):
        # Direction superposition
        qc.h(direction)
        
        # Controlled movement based on direction
        for i in range(pos_qubits):
            qc.cx(direction[0], position[i])
            qc.cx(direction[1], position[i])
        
        # Boundary check (optional, can be removed for wrapping behavior)
        # This part ensures the crawler stays within the grid
        for i in range(pos_qubits):
            qc.x(position[i])
        qc.mcx(position, direction[0])
        qc.mcx(position, direction[1])
        for i in range(pos_qubits):
            qc.x(position[i])

    # Measure position
    qc.measure(position, c)

    return qc

def plot_grid(probabilities, grid_size):
    grid = np.zeros((grid_size, grid_size))
    for pos, prob in probabilities.items():
        x, y = pos % grid_size, pos // grid_size
        grid[y, x] = prob
    
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Probability')
    plt.title(f"Quantum Crawler Position Probabilities (Steps: {steps}, Grid: {grid_size}x{grid_size})")
    plt.xlabel("X")
    plt.ylabel("Y")
    for i in range(grid_size):
        for j in range(grid_size):
            plt.text(j, i, f'{grid[i, j]:.3f}', ha='center', va='center', color='w')
    plt.show()

# Set up the quantum crawler
steps = 5
grid_size = 4  # 4x4 grid
qc = quantum_crawler(steps, grid_size)

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
    x, y = position % grid_size, position // grid_size
    print(f"Position ({x}, {y}): Probability {prob:.4f}")

# Plot the results
plot_histogram(counts)
plt.title(f"Quantum Crawler Results (Steps: {steps}, Grid: {grid_size}x{grid_size})")
plt.xlabel("Position")
plt.ylabel("Counts")
plt.show()

# Plot the grid
plot_grid(probabilities, grid_size)