'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

from sim_utils.common_types import *
import numpy as np

config_dict = [
    {
        "Component_name"        : "input_generation_stage",
        "measurement_period"    : 1,
        "duty-cycle"            : 10*UNIT_PREFIX["m"]
    },
    {
        "Component_name"        : "ideal_ADC_stage",
        "id"                    : "ideal ADC stage",
        "num_bits"              : 12,
        "quanitzation_method"   : QuantizationType.midtread
    },
    {
        "Component_name"        : "phase_analysis",
        "id"                    : "Fourier Phase Stage",
    },
    {
        "Component_name"        : "NLS_position_calc",
        "id"                    : "NLS 1",
        "optimization_method"   : OptimizationType.nelder_mead,
        "initial_guess"         : Cartesian2DPosition(20, 0)
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
signal_frequency = 40*UNIT_PREFIX["k"]
sampling_frequency = 10*signal_frequency
continuous_sampling_frequency = 100*signal_frequency
