import numpy as np
from scipy import optimize
from simulator_main import sim_config as cfg
from sim_utils.common_types import *

# TODO: documentation (RIP)
def gradient_descent(func, starting_params, args=(), step_size=0.5, termination_ROC=1e-5, 
                        max_iter=1e5, is_grad=False, delta_x=0.01):
    params = starting_params
    gradient = get_grad(func, params, args, is_grad, delta_x)
    grad_mag = np.linalg.norm(gradient)
    num_iter = 0
    print(gradient)

    while (grad_mag > termination_ROC):
        params = params - step_size*gradient
        gradient = get_grad(func, params, args, is_grad, delta_x)
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
    results = optimize.minimize(func, starting_params, args=args, method='Nelder-Mead')

    if (not results.success):
        print(results.message)

    # print("Converged with %d iterations" %results.nit)
    # print(func(results.x, *args))

    return results.x

def newton_gauss(func, starting_params, args=()):
    pass

def get_grad(func, params, args, is_grad, delta_x):
    if (is_grad):
        return func(params, *args)
    else:
        return np.array([get_derivative(func, params, args, i, delta_x)
                        for i in range(len(params))])

def get_derivative(func, params, args, var_index, delta_x):
    delta_params = np.zeros(params.shape)
    delta_params[var_index] = delta_x

    return (func(params + delta_params, *args) - func(params, *args))/delta_x

def tdoa_function_3D(pinger_pos, hydrophone_pos, is_polar):
    # in this case, pinger_pos[0] is r and pinger_pos[1] is phi
    if (is_polar):    
        pinger_distance = np.sqrt(pinger_pos[0]**2 + cfg.pinger_position.z**2)
        delta_z = cfg.pinger_position.z - hydrophone_pos.z
        delta_phi = pinger_pos[1] - hydrophone_pos.phi
        
        delta_d = np.sqrt(pinger_pos[0]**2 + hydrophone_pos.r**2 + delta_z**2
                    - 2*pinger_pos[0]*hydrophone_pos.r*np.cos(delta_phi))
    # in this case, pinger_pos[0] is x and pinger_pos[1] is y
    else:
        pinger_distance = np.sqrt(pinger_pos[0]**2 + pinger_pos[1]**2 + cfg.pinger_position.z**2)
        hydrophone_pos_cart = cyl_2_cart(hydrophone_pos)
        delta_x = pinger_pos[0] - hydrophone_pos_cart.x
        delta_y = pinger_pos[1] - hydrophone_pos_cart.y
        delta_z = cfg.pinger_position.z - hydrophone_pos.z
        
        delta_d = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    return (pinger_distance - delta_d)/cfg.speed_of_sound
    

    