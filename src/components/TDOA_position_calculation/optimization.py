#!/usr/bin/env python

import numpy as np
from scipy import optimize

# TODO: documentation (RIP)
def gradient_descent(grad_func, starting_params, args=(), step_size=0.5, termination_ROC=0.001, max_iter=1e5):
    params = starting_params
    gradient = grad_func(params, *args)
    grad_mag = np.linalg.norm(gradient)
    num_iter = 0

    while (grad_mag > termination_ROC):
        params = params - step_size*gradient
        gradient = grad_func(params, *args)
        grad_mag = np.linalg.norm(gradient)
        num_iter += 1

        if (grad_mag == np.inf):
            print("OverflowError. Step size might be too big. Optimization diverges")
            print("Diverging Parameters: ", params)
            return params

        if (num_iter == max_iter):
            print("WARNING! maximum iteration number reached")
            break

    print("Gradient Descent with step-size %f finished after %0d iterations" %(step_size, num_iter))
    return params

def nelder_mead(func, starting_params, args=()):
    results = optimize.minimize(func, starting_params, args=args)

    if (not results.success):
        print(results.message)

    return results.x

def newton_gauss(func, starting_params, args=()):
    pass

