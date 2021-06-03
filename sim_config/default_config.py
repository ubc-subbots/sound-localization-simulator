'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

from sim_utils.common_types import *
import numpy as np

config_dict = [
    {
        "Component_name" : "NLS_position_calc",
        "id" : "NLS1",
        "optimization_method" : OptimizationType.nelder_mead,
        "guessed pinger position" : PolarPosition(20, 0)
        #"initial_guess" : Cartesian2DPosition(20, 0)
    },
]

'''
Global Configurations
'''

speed_of_sound = 1500 #m/s
hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(2e-2, 0, 0),
    CylindricalPosition(2e-2, np.pi/2, 0),
    CylindricalPosition(0, 0, 2e-2),
    CylindricalPosition(1e-2, 1e-2, 1e-2),
]
pinger_position = CylindricalPosition(15, np.pi/5, 5)
