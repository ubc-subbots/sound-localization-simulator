'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

from sim_utils.common_types import *
import numpy as np

simulation_chain = [
    {
        "Component_name"        : "InputGenerationStage",
        "id"                    : "Input Generation Stage",
        "measurement_period"    : 2,
        "duty-cycle"            : 0.01
    },
    {
        "Component_name"        : "IdealADCStage",
        "id"                    : "ideal ADC stage",
        "num_bits"              : 12,
        "quanitzation_method"   : QuantizationType.midtread
    },
    {
        "Component_name"        : "PhaseAnalysisStage",
        "id"                    : "Fourier Phase Stage",
    },
    {
        "Component_name"        : "NLSPositionCalc",
        "id"                    : "NLS 1",
        "optimization_method"   : OptimizationType.nelder_mead,
        "initial_guess"         : Cartesian2DPosition(20, 0)
    },
]

'''
Global Configurations
'''

speed_of_sound = 1500 #m/s

#### position information ####
hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(2e-2, 0, 0),
    CylindricalPosition(2e-2, np.pi/2, 0),
    CylindricalPosition(0, 0, 2e-2),
    CylindricalPosition(1e-2, 1e-2, 1e-2),
]
pinger_position = CylindricalPosition(15, np.pi/5, 5)

#### frequency information ####
signal_frequency = 40e3
# used as ADC sampling frequency and for "digital" portion
sampling_frequency = 10*signal_frequency
# picked to be much higher so it's approximately continuous and can be used in "analog" portion
continuous_sampling_frequency = 100*signal_frequency
# TODO: double check pinger on-off frequency
carrier_frequency = 1