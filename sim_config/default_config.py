'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

from sim_utils.common_types import *
import numpy as np

def regenerate_positions():
    global hydrophone_positions, pinger_position

    pinger_position = CylindricalPosition(pinger_r, pinger_phi, pinger_z)
    
    hr = hydrophone_rho*np.sin(hydrophone_theta)
    hz = hydrophone_rho*np.cos(hydrophone_theta)
    hydrophone_positions = [
        CylindricalPosition(0, 0, 0),
        CylindricalPosition(hr, 0, hz),
        CylindricalPosition(hr, np.pi/2, -hz),
        CylindricalPosition(hr, np.pi, hz),
        CylindricalPosition(hr, -np.pi/2, -hz),
    ]

##############################################
# Gloabl Parameters
##############################################

speed_of_sound = 1500 #m/s

#### position information ####
# hydrophone_theta = np.pi/2
hydrophone_theta = 120/180*np.pi
hydrophone_rho = 1.8e-2
pinger_z = 5
pinger_r = 10
pinger_phi = 0

regenerate_positions()

#### frequency information ####
signal_frequency = 40e3
# used as ADC sampling frequency and for "digital" portion
sampling_frequency = 10*signal_frequency
# picked to be much higher so it's approximately continuous and can be used in "analog" portion
continuous_sampling_frequency = 100*signal_frequency
# TODO: double check pinger on-off frequency
carrier_frequency = 1

##############################################
# Simulation Chain
##############################################

simulation_chain = [
    {
        "component_name"        : "InputGenerationStage",
        "id"                    : "Input Generation Stage",
        "measurement_period"    : 0.1,
        "duty_cycle"            : 0.05
    },
    {
        "component_name"        : "GaussianNoise",
        "id"                    : "Gaussian Noise",
        "mu"                    : 0,
        "sigma"                 : 0.03
    },
    {
        "component_name"        : "IdealADCStage",
        "id"                    : "ideal ADC stage",
        "num_bits"              : 12,
        "quantization_method"   : QuantizationType.midtread
    },
    {
        "component_name"        : "ThresholdCaptureTrigger",
        "id"                    : "Threshold Capture Trigger",
        "num_samples"           : int(10*(sampling_frequency / signal_frequency)), # sample 10 cycles of the wave
        "threshold"             : 0.15*(2**11)
    },
    {
        "component_name"        : "CrossCorrelationStage",
        "id"                    : "Cross Correlation Stage",
    },
    {
        "component_name"        : "NLSPositionCalc",
        "id"                    : "NLS",
        "optimization_method"   : OptimizationType.nelder_mead,
        "initial_guess"         : PolarPosition(10, np.pi)
    }
]