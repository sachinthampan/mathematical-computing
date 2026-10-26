from time import perf_counter
from solver import find_largest_minimal_x
from src.pell.solver import pells_solver

start = perf_counter()
best_D, max_x, best_y = find_largest_minimal_x(10_000)

elapsed = perf_counter() - start

print(f"Search limit: 10,000")
print(f"Best D: {best_D}")
print(f"Minimal x: {max_x}")
print(f"Corresponding y: {best_y}")
print(f"Execution time: {elapsed:.4f} seconds")
