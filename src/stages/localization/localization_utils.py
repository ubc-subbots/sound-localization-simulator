'''@package localization_utils
Contains a variety of helper functions to be used across all position calculation components

@author Dvir Hilu
@date Oct 21, 2020
'''
import numpy as np
from scipy import optimize
#from simulator_main import sim_config as global_vars
import global_vars
from sim_utils.common_types import *
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

def gradient_descent(func, starting_params, args=(), step_size=0.5, termination_ROC=1e-5, 
                        max_iter=1e5, is_grad=False, delta_x=0.01):
    '''
    @brief Implements gradient descent optimization on the given function

    For more details on the implementation, visit
    https://github.com/ubc-subbots/sound-localization-simulator/blob/master/docs/Position_Calculation_Algorithms.pdf

    @param func                 Either the function to be optimized, or its analytically
                                calculated gradient. Use the is_grad flag to specificy
                                Whether func should be interpreted as the function or its
                                gradient. If func is the function, the gradient will be
                                calculated numerically
    @param starting_params      The initial guess for the function parameters that will result
                                in the function being minimized. The function expects this to
                                be inputted as a numpy array
    @param args                 A tuple containing any other arguments that should be inputted
                                to the function (but don't require minimization)
    @param step_size            The step size (in proportion to the magnitude of the gradient)
                                to be taken at each iteration
    @param termination_ROC      The magnitude of the gradient at which the function converges
    @param max_iter             The maximum amount of iterations the function will take
    @oaram is_grad              A flag to indicate whether func is a gradient or a function
    @param delta_x              If is_grad is true, this parameter determines the difference
                                in input values used when calculating the gradient numerically
    @return                     A numpy array containing the value of arguments that will
                                minimize func
    '''
    params = starting_params

    if (is_grad):
        gradient = func(params, *args)
    else:
        gradient = get_grad(func, params, args, delta_x)

    grad_mag = np.linalg.norm(gradient)
    num_iter = 0
    logger.debug(gradient)

    while (grad_mag > termination_ROC):
        params = params - step_size*gradient

        if (is_grad):
            gradient = func(params, *args)
        else:
            gradient = get_grad(func, params, args, delta_x)
        
        grad_mag = np.linalg.norm(gradient)
        num_iter += 1

        if (grad_mag == np.inf):
            logger.error("OverflowError. Step size might be too big. Optimization diverges")
            logger.debug("Diverging Parameters: %s" % str(params))
            return params

        if (num_iter == max_iter):
            logger.warning("maximum iteration number reached")
            break

    logger.info("Gradient Descent with step-size %f finished after %0d iterations" %(step_size, num_iter))
    return params


def nelder_mead(func, starting_params, args=()):
    '''
    @brief Implements nelder mead optimization on the given function

    For more details on the implementation, visit
    https://github.com/ubc-subbots/sound-localization-simulator/blob/master/docs/Position_Calculation_Algorithms.pdf

    @param func             The function needing to be minimized
    @param starting_params  The initial guess for the function parameters that will result
                            in the function being minimized. The function expects this to
                            be inputted as a numpy array
    @param args             A tuple containing any other arguments that should be inputted
                            to the function (constants, non-numerical parameters, etc.)
    @return                 A numpy array containing the value of arguments that will minimize 
                            func
    '''
    results = optimize.minimize(func, starting_params, args=args, method='Nelder-Mead')

    if (not results.success):
        logger.warning(results.message)

    logger.info("Nelder Mead optimization converged with %d iterations" %results.nit)

    return results.x


def newton_gauss(func, starting_params, args=()):
    pass


def get_grad(func, params, args, delta_x):
    '''
    @brief Calculates the gradient of a function numerically.

    @param func     The function for which the gradient is calculated
    @param params   The variable values at which the gradient is calculated
    @param args     A tuple containing any other arguments that should be inputted to the 
                    function (constants, non-numerical parameters, etc.)
    @param delta_x  The amount each parameter is adjusted by to find the numerical gradient
    @return         A numpy array containg the gradient of the function

    '''
    return np.array([get_partial_derivative(func, params, args, i, delta_x)
                    for i in range(len(params))])


def get_partial_derivative(func, params, args, var_index, delta_x):
    '''
    @brief calculates the partial derivative of a function numerically

    @param func         The function for which the partial derivative should be calculated
    @param params       The variable values at which the partial derivative is calculated
    @param args         A tuple containing any other arguments that should be inputted to the 
                        function (constants, non-numerical parameters, etc.)
    @param var_index    The index of params that contains the variable that the function is
                        differentiating with respect to
    @param delta_x      The amount each parameter is adjusted by to find the numerical gradient
    @return             The partial derivative of the function as a float
    '''
    delta_params = np.zeros(params.shape)
    delta_params[var_index] = delta_x

    return (func(params + delta_params, *args) - func(params, *args))/delta_x


def tdoa_function_3D(pinger_pos, hydrophone_pos, is_polar):
    '''
    @brief  calculates the time difference of arrival (TDOA) of the sound signal between the
            given hydrophone and hydrophone 0, given a specified pinger position

    @param pinger_pos       The position of the pinger. a numpy array with the XY plane position 
                            of the pinger position relative to hydrophone 0, given either in polar 
                            or cartesian coordinates. The is_polar flag should be set accordingly
    @param hydrophone_pos   The position of the hydrophone relative to hydrophone 0
    @param is_polar         Tells the function whether the pinger position was inputted in polar 
                            or cartesian (True -> polar, False -> cartesian)
    @return                 The TDOA value of the hydrophone relative to hydrophone 0 as a float
    '''
    # in this case, pinger_pos[0] is r and pinger_pos[1] is phi
    if (is_polar):    
        pinger_distance = np.sqrt(pinger_pos[0]**2 + global_vars.pinger_position.z**2)
        delta_z = global_vars.pinger_position.z - hydrophone_pos.z
        delta_phi = pinger_pos[1] - hydrophone_pos.phi
        
        delta_d = np.sqrt(pinger_pos[0]**2 + hydrophone_pos.r**2 + delta_z**2
                    - 2*pinger_pos[0]*hydrophone_pos.r*np.cos(delta_phi))
    # in this case, pinger_pos[0] is x and pinger_pos[1] is y
    else:
        pinger_distance = np.sqrt(pinger_pos[0]**2 + pinger_pos[1]**2 + global_vars.pinger_position.z**2)
        hydrophone_pos_cart = cyl_to_cart(hydrophone_pos)
        delta_x = pinger_pos[0] - hydrophone_pos_cart.x
        delta_y = pinger_pos[1] - hydrophone_pos_cart.y
        delta_z = global_vars.pinger_position.z - hydrophone_pos.z
        
        delta_d = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    return (pinger_distance - delta_d)/global_vars.speed_of_sound

def plane_wave_prop_delay(params, sensor_pos, use_depth_sensor=False):
    # need to convert sensor position to cartesian
    if (type(sensor_pos) == CylindricalPosition):
        pos = np.array(cyl_to_cart(sensor_pos))
    else:
        pos = np.array(sensor_pos)
    
    # convert to numpy array for dot product
    x = np.array(pos)

    if use_depth_sensor:
        # construct wave direction vector wit
        r = params[0]
        phi = params[1]
        z = global_vars.pinger_position.z
        norm_factor = np.sqrt(r**2 + z**2)

        # negative signs indicate propagation is towards sensor
        khat = -1/norm_factor * np.array([
            r*np.cos(phi),
            r*np.sin(phi),
            z
        ])
    else:
        # construct wave direction vector with spherical angles as params
        theta = params[0]
        phi = params[1]

        # negative signs indicate propagation is towards sensor
        khat = -np.array([
            np.sin(theta)*np.cos(phi),
            np.sin(theta)*np.sin(phi),
            np.cos(theta)
        ])
        
    return np.dot(khat, x)/global_vars.speed_of_sound