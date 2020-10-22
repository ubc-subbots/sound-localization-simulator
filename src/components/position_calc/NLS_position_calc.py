from components.position_calc import position_calc_utils
import numpy as np
from simulator_main import sim_config as cfg
from sim_utils.common_types import *

class NLS_position_calc:
    
    def __init__(self, name = "NLS_position_calc", optimization_type = OptimizationType.nelder_mead, 
                initial_guess = CylindricalPosition(0,0,0), is_polar=True):
        self.name = name
        self.optimization_type = optimization_type
        if (is_polar):
            self.initial_guess = np.array([initial_guess.r, initial_guess.phi])
        else:
            self.initial_guess = np.array([initial_guess.x, initial_guess.y])
        self.is_polar = is_polar
    
    def apply(self, sim_signal):
        pinger_pos = np.zeros(2)
        args = (self.is_polar, *sim_signal)

        if (self.optimization_type == OptimizationType.nelder_mead):
            pinger_pos = position_calc_utils.nelder_mead(get_squared_error_sum, 
                            self.initial_guess, args=args)
        elif (self.optimization_type == OptimizationType.gradient_descent):
            pinger_pos = position_calc_utils.gradient_descent(get_squared_error_sum, 
                            self.initial_guess, args=args)
        # else:
        #     pinger_pos = position_calc_utils.newton_gauss(get_squared_error_sum, 
        #                     self.initial_guess, args=args)

        if(self.is_polar):
            return CylindricalPosition(pinger_pos[0], pinger_pos[1], cfg.pinger_position.z)
        else:
            return CartesianPosition(pinger_pos[0], pinger_pos[1], cfg.pinger_position.z)

    def write_frame(self, frame):
        pass

def get_squared_error_sum(pinger_polar_pos, *args):
    expected_delta_t_vals = [
        position_calc_utils.tdoa_function_3D(pinger_polar_pos, position, args[0]) 
        for position in cfg.hydrophone_positions[1:]
    ]

    r = pinger_polar_pos[0] if args[0] else np.sqrt(pinger_polar_pos[0]**2 + pinger_polar_pos[1]**2)
    
    squared_error_sum = sum([
        (actual_delta_t - expected_delta_t) ** 2 + 1e6*np.heaviside(r-50, 0.5)
        for (actual_delta_t, expected_delta_t) in zip(args[1:], expected_delta_t_vals)
    ])

    return squared_error_sum