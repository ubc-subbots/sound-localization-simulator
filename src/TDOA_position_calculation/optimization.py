#!/usr/bin/env python

import numpy as np
from statistics import stdev

# TODO: documentation (RIP)
def gradient_descent(grad_func, starting_params, step_size=0.5, termination_ROC=0.001, max_iter=1e5):
    params = starting_params
    gradient = grad_func(params)
    grad_mag = np.linalg.norm(gradient)
    num_iter = 0

    while (grad_mag > termination_ROC):
        params = params - step_size*gradient
        gradient = grad_func(params)
        grad_mag = np.linalg.norm(gradient)
        num_iter += 1

        if (num_iter == max_iter):
            print("WARNING! maximum iteration number reached")
            break

    print("Gradient Descent with step-size %.1f finished after %0d iterations" %(step_size, num_iter))
    return params

def nelder_mead(func, starting_params, alpha=1, gamma=2, rho=0.5, sigma=0.5, 
                    termination_stdev=0.01, max_iter=1e5, init_simplex_scale=0.5):
    params = starting_params
    simplex = [params]
    for i in range(len(params)):
        next_vertex_adder = np.zeros(params.shape)
        next_vertex_adder[i] = params[i]
        simplex.append(params+next_vertex_adder)
    num_iter = 0

    simplex_stdev = calculate_simplex_stdev(func, simplex)

    while(simplex_stdev > termination_stdev):
        simplex = calculate_next_simplex(func, simplex, alpha, gamma, rho, sigma)
        simplex_stdev = calculate_simplex_stdev(func, simplex)
        num_iter += 1

        if (num_iter == max_iter):
            print("WARNING! maximum iteration number reached")
            break

    simplex_min_index = min([func(vertex) for vertex in simplex])
    print("Nelder Mead finished after %0d iterations" %(num_iter))

    return simplex[simplex_min_index]

def calculate_next_simplex(func, simplex, alpha, gamma, rho, sigma):
    return simplex

def calculate_simplex_stdev(func, simplex):
    return stdev([func(vertex) for vertex in simplex])