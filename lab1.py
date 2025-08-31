#!/usr/bin/env python3
from state import State
import random
from functional import seq
from bitarray import frozenbitarray as bitarray

# Add set_amplitudes method to State class
def set_amplitudes(self, amplitudes: list):
    """Set state amplitudes directly for testing purposes"""
    assert len(amplitudes) == 2**self.n_qubits, f"Need {2**self.n_qubits} amplitudes"
    self.state = seq([
        (bitarray(format(i, f"0{self.n_qubits}b")), complex(amplitudes[i]))
        for i in range(len(amplitudes))
    ])
    return self

# Monkey patch the method to State class
State.set_amplitudes = set_amplitudes

random.seed(42)  # For reproducible results

# Task 1: Test |0> state
print("Testing |0> state")
results_0 = []
for i in range(10):
    state = State(1)
    result = state.measure(0)
    results_0.append(result)

print(f"Results: {results_0}")
all_zeros = all(r == 0 for r in results_0)
print(f"All measurements return 0: {all_zeros}")

# Test |1> state
print("\nTesting |1> state")
results_1 = []
for i in range(10):
    state = State(1)
    state.x(0)  # Apply X gate to get |1>
    result = state.measure(0)
    results_1.append(result)

print(f"Results: {results_1}")
all_ones = all(r == 1 for r in results_1)
print(f"All measurements return 1: {all_ones}")

# Task 2: Test custom state {0.866, 0.5}
print("\nTesting custom state {0.866, 0.5}")
amp_0 = 0.866
amp_1 = 0.5

# Check normalization
norm_squared = amp_0**2 + amp_1**2
print(f"Normalization: {amp_0}^2 + {amp_1}^2 = {norm_squared:.6f}")
is_normalized = abs(norm_squared - 1.0) < 1e-6
print(f"State is normalized: {is_normalized}")

# Theoretical probabilities
prob_0_theory = amp_0**2
prob_1_theory = amp_1**2
print(f"Theoretical P(0) = {prob_0_theory:.6f}")
print(f"Theoretical P(1) = {prob_1_theory:.6f}")

# Measure 1000 times
measurements = []
for i in range(1000):
    state = State(1)
    state.set_amplitudes([amp_0, amp_1])
    result = state.measure(0)
    measurements.append(result)

# Analyze results
count_0 = measurements.count(0)
count_1 = measurements.count(1)
prob_0_measured = count_0 / 1000
prob_1_measured = count_1 / 1000

print(f"Measured results: {count_0} zeros, {count_1} ones")
print(f"Measured P(0) = {prob_0_measured:.6f}")
print(f"Measured P(1) = {prob_1_measured:.6f}")
print(f"Error in P(0): {abs(prob_0_measured - prob_0_theory):.6f}")
print(f"Error in P(1): {abs(prob_1_measured - prob_1_theory):.6f}")

# Task 3: Test |+> state using Hadamard gate
print("\nTesting |+> state using Hadamard gate")

# Create |+> state
state = State(1)
state.h(0)
print("Created |+> state with Hadamard gate")

# Expected probabilities for |+> state
expected_prob = 0.5
print(f"Expected P(0) = P(1) = {expected_prob}")

# Measure 1000 times
measurements = []
for i in range(1000):
    state = State(1)
    state.h(0)  # Create fresh |+> state
    result = state.measure(0)
    measurements.append(result)

# Analyze results
count_0 = measurements.count(0)
count_1 = measurements.count(1)
prob_0_measured = count_0 / 1000
prob_1_measured = count_1 / 1000

print(f"Measured results: {count_0} zeros, {count_1} ones")
print(f"Measured P(0) = {prob_0_measured:.6f}")
print(f"Measured P(1) = {prob_1_measured:.6f}")
print(f"Difference from 50/50: {abs(prob_0_measured - 0.5):.6f}")
