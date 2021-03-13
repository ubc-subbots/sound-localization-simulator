'''@package nls_position_calc
The component modelling the Non-linear Least Squares (NLS) solution of the position calculation
problem.

@author Dvir Hilu
@date Oct 21, 2020
'''

from components.position_calc import position_calc_utils
import numpy as np
import global_vars
from sim_utils.common_types import *

class NLSPositionCalc:
    '''
    NLS_position_calc is a class used to model the method of calculating the position of the pinger
    from hydrohpone Time Differece Of Arrival (TDOA) using a Non-linear Least Squares (NLS) solution

    The component first receives inputs corresponding to the TDOA measured between each hydrophone
    and the designated hydrophone 0 (this assignment is arbitrary, but hydrophone 0 must be located at
    the origin of the coordinate system). It then calculates an expected value based on the 3D TDOA
    model equation given some initial guess for the position. After calculating the expected TDOA values, 
    it takes a sum of the squares of the differences between the actual and expected TDOA values 
    ( sum[(expected-actual)^2] ), to get a single value representing the correctness" of
    the pinger location. The function then iterates this process using a minimization algorithm (Gradient
    Descent, Nelder Mead, Newton-Gauss) to find the optimal pinger position to fit the data.

    Currently, the algorithm does not calculate the z position of the pinger and instead extracts it
    directly. This is beacuse the z position is available through the pressure sensor.

    For more info:
    https://github.com/ubc-subbots/sound-localization-simulator/blob/master/docs/Position_Calculation_Algorithms.pdf
    '''

    def __init__(self, initial_data):
        '''
        @brief class constructor

        @param initial_data["name"]
            a unique ID to distinguish the component instance
        @param initial_data["optimization_type"]
            The optimization type chosen for the method. Options include Gradient Descent, Nelder Mead, 
            or Newton Gauss. The input is expecting an OptimizationType enum defined in common_types.py. 
            The possible values the enum could take are 
            OptimizationType.<nelder_mear, gradient_descent, newton_gauss>
        @param initial_data["initial_guess"] 
            The initial guess for the XY plane position of the pinger. The function expects an input of 
            type PolarPosition or Cartesian2DPosition, both defined in common_types.py
        '''
        self.component_name = initial_data.get("component_name", "NLSPositionCalc")
        self.id = initial_data.get("id", "NLS")
        self.optimization_type = initial_data.get("optimization_type", OptimizationType.nelder_mead)
        initial_guess = initial_data.get("initial_guess", PolarPosition(0,0))
        if (type(initial_guess) == PolarPosition):
            self.initial_guess = np.array([initial_guess.r, initial_guess.phi])
            self.is_polar = True
        elif (type(initial_guess) == Cartesian2DPosition):
            self.initial_guess = np.array([initial_guess.x, initial_guess.y])
            self.is_polar = False
        else:
            raise ValueError("Initial Pinger Position should be either a PolarPosition or Cartesian2DPosition")
    
    def apply(self, sim_signal):
        '''
        @brief Applies the simulation signal to the component and returns its outputs.

        @param sim_signal   A tuple representing the TDOA values measured by each hydrophone with hydrophone
                            0. The order of TDOA values in the tuple MUST follow the order of hydrophones
                            specified in the config file. For example, the first value in the tuple will be
                            the TDOA between global_vars.hydrophone_positions[1] and global_vars.hydrophone_positions[0]
                            (specifically t1-t0)
        '''        
        # argument to the minimizer must be a numpy array
        pinger_pos = np.zeros(2)
        # non-minimized args are packaged in a single tuple
        args = (self.is_polar, *sim_signal)

        if (self.optimization_type == OptimizationType.nelder_mead):
            pinger_pos = position_calc_utils.nelder_mead(get_squared_error_sum, 
                            self.initial_guess, args=args)
        elif (self.optimization_type == OptimizationType.gradient_descent):
            pinger_pos = position_calc_utils.gradient_descent(get_squared_error_sum, 
                            self.initial_guess, args=args)
        # elif (self.optimization_type == OptimizationType.newton_gausss):
        #     pinger_pos = position_calc_utils.newton_gauss(get_squared_error_sum, 
        #                     self.initial_guess, args=args)
        else:
            raise ValueError("Optimization type must be of type OptimizationType. You inputted " + 
                                str(self.optimization_type))

        if(self.is_polar):
            return CylindricalPosition(pinger_pos[0], pinger_pos[1], global_vars.pinger_position.z)
        else:
            return CartesianPosition(pinger_pos[0], pinger_pos[1], global_vars.pinger_position.z)

    def write_frame(self, frame):
        return {}

def get_squared_error_sum(pinger_pos, is_polar, *hydrophone_tdoas):
    '''
    @brief  calculates the sum of error squared (sum[(expected-actual)^2]) for a given pinger
            position and tuple of hydrophone tdoa values.

    @param pinger_pos           The estimated pinger position. a numpy array with the XY 
                                plane position of the pinger position relative to hydrophone 0, 
                                given either in polar or cartesian coordinates. The is_polar 
                                flag should be set accordingly
    @param is_polar             Tells the function whether the pinger position was inputted in 
                                polar or cartesian (True -> polar, False -> cartesian)
    @param *hydrophone_tdoas    TDOA values of each hydrophone relative to hydrophone 0. The 
                                order of TDOA values in the tuple MUST follow the order of 
                                hydrophones specified in the config file. For example, the first 
                                value in the tuple will be the TDOA between 
                                global_vars.hydrophone_positions[1] and global_vars.hydrophone_positions[0]
                                (specifically t1-t0)
    @return                     The sum of square of the error calculated for each hydrophone
                                with the given pinger position
    '''
    expected_delta_t_vals = [
        position_calc_utils.tdoa_function_3D(pinger_pos, position, is_polar) 
        for position in global_vars.hydrophone_positions[1:]
    ]

    r = pinger_pos[0] if is_polar else np.sqrt(pinger_pos[0]**2 + pinger_pos[1]**2)
    
    squared_error_sum = sum([
        (actual_delta_t - expected_delta_t) ** 2 + 1e6*np.heaviside(r-50, 0.5)
        for (actual_delta_t, expected_delta_t) in zip(hydrophone_tdoas, expected_delta_t_vals)
    ])

    return squared_error_sum