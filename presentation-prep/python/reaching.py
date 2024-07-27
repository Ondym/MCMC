import numpy as np

# Transition matrix based on the provided Markov chain
# States: 0, 1, 2, 3, 4
P = [
    [0.6, 0.2, 0.0, 0.15, 0.05],  # Transition probabilities from state 0
    [0.5, 0.1, 0.1, 0.0, 0.3],    # Transition probabilities from state 1
    [0.35, 0.0, 0.25, 0.15, 0.25],  # Transition probabilities from state 2
    [0.6, 0.0, 0.1, 0.0, 0.3],    # Transition probabilities from state 3
    [0.0, 0.0, 0.0, 0.0, 1.0]     # Transition probabilities from state 4
]

for p in P:
    print(sum(p)),

# Function to simulate the Markov chain and count steps to reach node 4
def simulate_steps_to_node_4(P, initial_state, target_state, num_simulations):
    total_steps = 0
    
    for _ in range(num_simulations):
        state = initial_state
        steps = 0
        
        while state != target_state:
            state = np.random.choice([0, 1, 2, 3, 4], p=P[state])
            steps += 1
        
        total_steps += steps
    
    average_steps = total_steps / num_simulations
    return average_steps

target_state = 4
num_simulations = 10**5
# Parameters
for initial_state in range (target_state):
    # Run the simulation
    average_steps = simulate_steps_to_node_4(P, initial_state, target_state, num_simulations)
    print(f"Average number of steps to reach node {target_state} from node {initial_state}: {average_steps}")
