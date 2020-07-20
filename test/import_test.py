#!/usr/bin/env python

print("******* Python Import Test *******")
from input_generation import input_generation
print("input_generation/input_generation.py imported successfully!")
from time_difference_calculations import phase_analysis
print("time_difference_calculations/phase_analysis.py imported successfully!")
from TDOA_position_calculation import optimization, nonlinear_least_squares, analytical_solution
print("TDOA_position_calculation/optimization.py imported successfully!")
print("TDOA_position_calculation/nonlinear_least_squares.py imported successfully!")
print("TDOA_position_calculation/analytical_solution.py imported successfully!")