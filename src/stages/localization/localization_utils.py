'''@package localization_utils
Contains a variety of helper functions to be used across all position calculation components

@author Dvir Hilu
@date Oct 21, 2020
'''
from math import floor
import time
import numpy as np
from scipy import optimize
from itertools import chain
#from simulator_main import sim_config as global_vars
import global_vars
from sim_utils.common_types import *
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

#def gradient_descent(func, starting_params, args=(), step_size=0.5, termination_ROC=1e-5, 
 #                      max_iter=1e5, is_grad=False, delta_x=0.01):


 #we could change the coodinate system in which we perform gradient descent

def gradient_descent(func, starting_params, args=(), step_size=1e7, termination_ROC=1e-13, 
                       max_iter=2.5e2, is_grad=False, delta_x=0.0001):
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

    mytuple=gradient_sampling(func, global_vars.pinger_position, args,delta_x, radius=0.01, num_samples=100000, print_all=False)
    print("average gradient around the solution is")
    print(mytuple[0])
    print("with a standard deviation")
    print(mytuple[1])

    #BIG NOTE TO SELF, A 3D GRAPH OF THE SQUARED ERROR WOULD GO HARD AND SO WOULD WATCHING THE ALGORITHIM'S PATH ON SAID GRAPH
    #NOW THAT YOU GOT A GRADIENT SAMPLING SCRIPT, THIS IS THE NEXT BIG VISUALIZATION TOOL
    params = starting_params

    if (is_grad):
        gradient = func(params, *args)
    else:
        gradient = get_grad(func, params, args, delta_x)

    grad_mag = np.linalg.norm(gradient)
    
    num_iter = 0
    logger.debug(gradient)
    print("initial magnitude of the gradient is")
    print(grad_mag)
    print("the algorithim converges if gradient is below")
    print(termination_ROC)
    while (grad_mag > termination_ROC):
        params = params - step_size*gradient
        

        if (is_grad):
            gradient = func(params, *args)
        else:
            gradient = get_grad(func, params, args, delta_x)
           #gradient is of the form [-4.74012403e-10  1.06097890e-10]
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
    #print("it estimated a pinger location of")
    #print(params)
    #print("the gradient descent functoin has a starting params value of ")
    #print(starting_params)
    

    
    
    
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
    print("Nelder mead was fed initial guess of")
    print(starting_params)
    print("estimated location")
    print(results.x)
    return results.x


def newton_gauss(func, starting_params, args=()):
    pass

def angle_nls(func, args=(), radius=10, resolution = 1000):
    '''
    @brief Implements gradient descent optimization on the given function

    For more details on the implementation, visit
    https://github.com/ubc-subbots/sound-localization-simulator/blob/master/docs/Position_Calculation_Algorithms.pdf

    @param func                 Either the function to be optimized, or its analytically
                                calculated gradient. Use the is_grad flag to specificy
                                Whether func should be interpreted as the function or its
                                gradient. If func is the function, the gradient will be
                                calculated numerically
    @param args                 A tuple containing any other arguments that should be inputted
                                to the function (but don't require minimization)
    @param radius               A float determining the constant radius at which we interate over differing phi values to find MinError
    @param resolution           An integer determining the resolution at which we iterate over phi (from 0 - 2pi)
    @return                     A numpy array containing the value of arguments that will
                                minimize func
    '''


    #BIG NOTE TO SELF, A 3D GRAPH OF THE SQUARED ERROR WOULD GO HARD AND SO WOULD WATCHING THE ALGORITHIM'S PATH ON SAID GRAPH
    #NOW THAT YOU GOT A GRADIENT SAMPLING SCRIPT, THIS IS THE NEXT BIG VISUALIZATION TOOL
    #params = starting_params
    params=np.zeros(2)

    minMinError = 1e6
    bestPhi = 0
    startTime = time.time()

    # Large range for high accuracy (~0.8s of calculations on regular laptop)
    radiusRangeThorough = [x/10 for x in range(10,40)] + [x/5 for x in range(20,50)] + list(range(10,20)) + [x*2 for x in range(10,20)] + [x*4 for x in range(10,20)]
    
    # Smaller range for higher speed (~0.14s of calculations on regular laptop)
    # Note that the accuracy is not very affected - therefore better to use smaller range
    radiusRangeEcon =  [x/2 for x in range(2,8)] + [x*2 for x in range(2,5)] + [x*5 for x in range(2,4)] + [x*10 for x in range(2,4)] + [x*20 for x in range(2,4)]

    # Step through predetermined list of radius guesses, with higher granularity at lower values
    for radiusIndex in radiusRangeEcon:
        params[0]=radiusIndex

        squareErrorList = np.zeros(resolution)

        for i in range(resolution):
            #stepping phi from 0 to 2pi with resolution number of increments
            params[1]=np.pi*float(i)/float(resolution)
            squareErrorList[i] = func(params, *args)

        minError = squareErrorList[0]
        phi = 0
        for i in range(resolution):
            if squareErrorList[i] < minError:
                phi = np.pi*float(i)/float(resolution)
                minError = squareErrorList[i]
        
        #print("minError = " + str(minError) + "  Phi = " + str(phi) + " rads,   " + str(phi*180/(np.pi))+ " degrees")

        #testing stuff
        pinger = global_vars.pinger_position.phi*180/np.pi
        pingerdistance = global_vars.pinger_position.r
        phi1 = phi*180/(np.pi)

        #print("Pinger Distance = " + str(pingerdistance)  +" meters, Pinger Angle = " + str(pinger) + " degrees,  Guess Distance = " + str(radius) + " meters,   Angle Error: " + str(100*abs(pinger-phi1)/180)+ "% Min NLS Error: " + str(minError))
        
        if(minError < minMinError):
            minMinError = minError
            bestPhi = phi
            
    # Calculate time calculations took (for testing purposes)
    endTime = time.time()
    print("it took: " + str(endTime-startTime) + "s")

    # Finalize best angle found
    params[1] = bestPhi
    print("Pinger Distance = " + str(pingerdistance)  +" meters, Pinger Angle = " + str(pinger) + " degrees, Calculated Angle: " + str(bestPhi * 180/np.pi) + " degrees, Angle Error: " + str(100*abs(pinger-bestPhi*180/(np.pi))/180)+ "%")
    
    return params



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
    #print(params)
    return np.array([get_partial_derivative(func, params, args, i, delta_x)
                    for i in range(len(params))])



def gradient_sampling(func, params, args,delta_x,radius,num_samples,print_all):
    '''
    @brief calculates the gradient of a function at a lot of points near a location, intnded to figure out gradient near the pinger to
    properly calibrate the gradient descent's endpoint

    @param functio:n func         function: for which the gradient is calculated
    @param struct: params         CylindricalPosition type struct telling us the center point about which point we will
                                 calculate our scatter of gradients,
    @param tuple: args           containing any other arguments that should be inputted to the gradient descent 
                                 function (constants, non-numerical parameters, etc.)
    @param float: radius         the radius being swept out and sampled across
    @param int: num_samples      the approximate number of samples taken, ballpark is more what matters
    @param float: delta_x        The amount by which each parameter is adjusted by to find the numerical gradient
    @param bool: print_all       Whether or not we print all gradients sampled
    
    @return tuple:      floats of average gradient within the specified polar domain as well as standard deviation
                        
                        
                        PERHAPS A FEATURE TO TELL YOU HOW MANY SAMPLES ARE ABOVE A CUTOFF?

    '''

    #add functionality to specify the angular and radial density of gradinet sampling as well as the radius size?
    
 
  
    loop_iterations=floor(np.sqrt(num_samples))

    #angle loop run from 0 to 2pi and radius loop run up to the radius needed with floor(sqrt(num_samples)) for each
    radius_scaling_factor=radius/loop_iterations
    angle_scaling_factor=2*np.pi/loop_iterations


    print_all=False

    central_r=params.r
    central_phi=params.phi
    central_z=params.z

    central_polar=np.zeros(2)
    central_polar[0]=central_r
    central_polar[1]=central_phi
    
    #central_polar=[central_r,central_phi]
    #we want to record an array of gradient magnitudes, AN ARRAY OF ZEROS WOULD SKEW OUR AVERAGE SUM ALL NONZERO ELEMENTS
    
    grad_array=np.zeros(num_samples)
    for i in range(loop_iterations):
        for j in range(loop_iterations):
            #we have to index the r and phi values for our gradient calculations by our scaling factor
            #this indexing scheme might overwrite some or duplicate some but that is not a huge issue for ballaprk estimate
            new_polar=PolarPosition(central_r+i*radius_scaling_factor, central_phi+j*angle_scaling_factor)

            new_grad=get_grad(func, central_polar, args, delta_x)
            grad_mag=np.sqrt(new_grad[0]*new_grad[0]+new_grad[1]*new_grad[1])
            #do we want to print each gradiant value?
            if(print_all):
                print(grad_mag)
            #we need to count up from zero to loop_itearations, loop_iterations times so a counter i increases when j
            #hits loop_iterations
            grad_array[loop_iterations*i+j]=grad_mag

    

    #to account for non-filled indices
    num_nonzero=np.count_nonzero(grad_array)

    #sum across filled indices
    grad_sum=np.sum(grad_array[:(num_nonzero-1)])
    average=grad_sum/num_nonzero
    #I want to get the variance of all nonzero elements, I made a function to find var across the first n elements
    variance=calc_variance(grad_array,average,num_nonzero)

    standev=np.sqrt(variance)
    return [average,standev]



def calc_variance(array,mean,n):
    '''
    @breif calculates variance of an array with a mean up to element n
    @param array    a numpy array: to find variance of elements in
    @param mean     float: the mean of the numpy array
    @param n        int: the number of elements to sum to when finding the variance
    @return         float: returns variance as a number
    '''
    sum=0
    for i in range(n):
        sum=sum+(array[i]-mean)**2

    return sum/n



    
 

def get_partial_derivative(func, params, args, var_index, delta_x):
    '''
    @brief calculates the partial derivative of a function numerically

    @param function: func      The function for which the partial derivative should be calculated
    @param ???: params         The variable values at which the partial derivative is calculated
    @param tuple: args         A tuple containing any other arguments that should be inputted to the 
                              function we are differentiating (constants, non-numerical parameters, etc.)
                              it is defined in \sound-localization-simulator-master\src\stages\localization\multilateration\ nls.py like this
                              args = (self.is_polar, *sim_signal)
    @param int: var_index    The index of params that contains the variable that the function is
                             differentiating with respect to
    @param float: delta_x    The amount each parameter is adjusted by to find the numerical gradient
    @return float:           The partial derivative of the function as a float
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
        pinger_distance = np.sqrt(pinger_pos[0]**2 + global_vars.depth_sensor_reading()**2)
        delta_z = global_vars.depth_sensor_reading() - hydrophone_pos.z
        delta_phi = pinger_pos[1] - hydrophone_pos.phi
        
        delta_d = np.sqrt(pinger_pos[0]**2 + hydrophone_pos.r**2 + delta_z**2
                    - 2*pinger_pos[0]*hydrophone_pos.r*np.cos(delta_phi))
    # in this case, pinger_pos[0] is x and pinger_pos[1] is y
    else:
        pinger_distance = np.sqrt(pinger_pos[0]**2 + pinger_pos[1]**2 + global_vars.depth_sensor_reading()**2)
        hydrophone_pos_cart = cyl_to_cart(hydrophone_pos)
        delta_x = pinger_pos[0] - hydrophone_pos_cart.x
        delta_y = pinger_pos[1] - hydrophone_pos_cart.y
        delta_z = global_vars.depth_sensor_reading() - hydrophone_pos.z
        
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
        z = global_vars.depth_sensor_reading()
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