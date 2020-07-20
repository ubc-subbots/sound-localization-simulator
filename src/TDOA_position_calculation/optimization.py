#!/usr/bin/env python

import numpy as np

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
    