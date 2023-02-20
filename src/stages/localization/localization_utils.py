'''@package localization_utils
Contains a variety of helper functions to be used across all position calculation components

@author Dvir Hilu
@date Oct 21, 2020
'''
from math import floor
import numpy as np
from scipy import optimize
#from simulator_main import sim_config as global_vars
import global_vars
from sim_utils.common_types import *
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

#def gradient_descent(func, starting_params, args=(), step_size=0.5, termination_ROC=1e-5, 
 #                      max_iter=1e5, is_grad=False, delta_x=0.01):


 #TO DO, IMPLIMENT SOME KIND OF GRAPHICAL INDICATOR TO TELL YOU THE GRADIENT DESCENT PATH OR A TERMINATION CONDITION IF CIRCLING THE DRAIN IS
 #DETECTED IE EVEY 100 OR 1000 STEPS WE COMPARE VALUES AND SEE IF THE MAGNITUDE DIFFERENCE IS BELOW A CUTOFF

 #we could change the coodinate system in which we perform gradient descent
 #noise could be seriously hurting the accuracy of grad calculations
 #not sure why args is set to just empty brackets
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
    
    #lets call our scatter gradient function just one time
    #print("average gradient around pinger is")
    
    
    
    
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

    @param func         function: for which the gradient is calculated
    @param params       CylindricalPosition: type struct telling us the center point about which point we will calculate our scatter of gradients,
    @param args         tuple: containing any other arguments that should be inputted to the gradient descent 
                        function: (constants, non-numerical parameters, etc.)
    @param radius       float: the radius being swept out and sampled across
    @param num_samples  int: the approximate number of samples taken, ballpark is more what matters
    @param delta_x      float: The amount by which each parameter is adjusted by to find the numerical gradient
    @param print_all    Bool: Whether or not we print all gradients sampled
    
    @return             float: average gradient within the specified polar domain as well as standard deviation in a tuple
                        ADD A FEATURE TO TELL YOU HOW MANY SAMPLES ARE ABOVE A CUTOFF

    '''

    #we should add functionality to specify the angular and radial density of gradinet sampling as well as the radius size
    
 
  
    loop_iterations=floor(np.sqrt(num_samples))

    #I will have angle loop run from 0 to 2pi and radius loop run up to the radius needed with floor(sqrt(num_samples)) for each
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
            #we have to index the r and phi values for our gradient calculation, index phi to rotate 2pi
            new_polar=PolarPosition(central_r+i*radius_scaling_factor, central_phi+j*angle_scaling_factor)
            #this indexing scheme might overwrite some or duplicate some but that is not a huge issue for ballaprk estimate
            new_grad=get_grad(func, central_polar, args, delta_x)
            grad_mag=np.sqrt(new_grad[0]*new_grad[0]+new_grad[1]*new_grad[1])
            if(print_all):
                print(grad_mag)
            #we need to count up from zero to loop_itearations, i increases by 1 each time
            grad_array[loop_iterations*i+j]=grad_mag

    

    #to account for non-filled indices
    num_nonzero=np.count_nonzero(grad_array)

    #sum across filled indices
    grad_sum=np.sum(grad_array[:(num_nonzero-1)])
    average=grad_sum/num_nonzero
    #I want to get the variance of all nonzero elements, I should make a function to sum across the first n elements
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

    @param func         The function for which the partial derivative should be calculated
    @param params       The variable values at which the partial derivative is calculated
    @param args         A tuple containing any other arguments that should be inputted to the 
                        function (constants, non-numerical parameters, etc.)
                        it is defined in \sound-localization-simulator-master\src\stages\localization\multilateration\ nls.py like this
                        # non-minimized args are packaged in a single tuple
                        args = (self.is_polar, *sim_signal)
    @param var_index    The index of params that contains the variable that the function is
                        differentiating with respect to
    @param delta_x      The amount each parameter is adjusted by to find the numerical gradient
    @return             The partial derivative of the function as a float
    '''

    #print(params)
    #this params.shape throws an error when trying to run my gradient descent function, 
    #some documentation for function input types would sure help
    #params is of the form [3.82449559 1.58876409], shape is of the form (2,) 
    
    #perhaps my grad sampling function is being fed a parameter of a weird format like polar position(3.82449559 1.58876409) instead of just [3.82449559 1.58876409]
    #get_grad is just fed another params that goes into get_partial_derivitave, my gradient_samplong probably give it a wierd type
   # print("get partial derivitiave sees")
    #print(params)
    #we tryna make a numpy array of the size of our input params, we add them so it seems that params might be a numpy array too, not just a list
    #print(params.shape)
    delta_params = np.zeros(params.shape)
    delta_params[var_index] = delta_x
    # this is what stocco calls hacking
    #error is get_square_error needs parameter is_polar, perhaps  func is get_square error,
    #TypeError: get_squared_error_sum() missing 1 required positional argument: 'is_polar'
    #why complain now when I define params.sahpe myself as numpy array, why is it mad now

    #OH PERHAPS THE DATA TYPE I FEED IT MAY GIVE IT INFO ABOUT WHETHER OR NOT IT IS POLAR

    #lets try tracking back to where get_square_error is put into this "func"

    #AFTER HARDCODING IT WE GET 
    #    grad_mag=sqrt(new_grad[0]*new_grad[0]+new_grad[1]*new_grad[1]) NameError: name 'sqrt' is not defined
    #OK WE PROBABLY FIXED IT, WE DON'T WANNA RELY ON HARDCODING THOUGH SQRT IS NOT STANDARD

    #IT WORKED, THIS HARDCODING IS POLAR ISSUE IS WEIRD THO, IT CLEARLY WANTS NUMPY ARRAYS BUT SOMEHOW
    #THE DEFAULT INPUTS COMMUNICATED THAT WE WERE FEEDING get_square_error a polar value, lets not be too brute force
    # if type(self.initial_guess) == PolarPosition:
         #   self.initial_guess = np.array([self.initial_guess.r, self.initial_guess.phi])
          #  self.is_polar = True
    #this is in the apply(self, sim_signal) function which calls get_square_error
    #it looks at initial guess which it wants as a polarposition struct, turns it into a numpy array, and sets is_polar with that
    #so how deos the default arrangement do this while my function fails to, lets probe initial guess 
    #inside of get_square_error as it runs?

    #get square error sees this as initial guess PolarPosition(r=3.8, phi=1.6), lets dig into what is_polar value is at
    #diferent points

    #get_squared_error_sum seems is_polar=True
    #this is right before get_squared_error_sum is called in gradient descent
    #it is called without any parameters, I guess they are all taken from the self class
    #pinger_pos = localization_utils.gradient_descent(get_squared_error_sum,
     #                                                         self.initial_guess, args=args)
     #somehow it infers parameters but poorly
     #do we even enter the function call???, nope nope nope how sad
     #i should take time to understand how function calls with no parameters work lol

    #print("the value of args is")
    #print(args)

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