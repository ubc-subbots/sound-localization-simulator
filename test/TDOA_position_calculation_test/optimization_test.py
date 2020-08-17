#!/usr/bin/env python

from TDOA_position_calculation import optimization
from scipy import optimize
import numpy as np

def quartic(x):
    return x**4

def quartic_grad(x):
    return 4*x**3

def paraboloid(params):
    return params[0]**2 + params[1]**2

def paraboloid_grad(params):
    return np.array([2*params[0], 2*params[1]])

starting_params = np.array([20])

#step size too big - diverges
optimized_params = optimization.gradient_descent(quartic_grad, starting_params)
print("Gradient Descent optimized the parameters to be:" + str(optimized_params))

optimized_params = optimization.gradient_descent(quartic_grad, starting_params, step_size=1e-3)
print("Gradient Descent optimized the parameters to be:" + str(optimized_params))

optimized_params = optimization.nelder_mead(quartic, starting_params)
print("Nelder Mead optimized the parameters to be:" + str(optimized_params))

starting_params = np.array([10, 12.3])

optimized_params = optimization.gradient_descent(paraboloid_grad, starting_params, step_size=0.7, termination_ROC=1e-5)
print("Gradient Descent optimized the parameters to be:" + str(optimized_params))

optimized_params = optimization.nelder_mead(paraboloid, starting_params)
print("Nelder Mead optimized the parameters to be:" + str(optimized_params))


