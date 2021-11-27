from sim_utils.common_types import *

##############################################
# Procedural Parameters
##############################################

num_iterations = 1

##############################################
# Content Parameters
##############################################

speed_of_sound = 1500 #m/s

#### position information ####
hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(1.85e-2, 0, -1e-2),
    CylindricalPosition(1.85e-2, np.pi/2, -1e-2),
    CylindricalPosition(1.85e-2, np.pi, -1e-2),
    CylindricalPosition(1.85e-2, -np.pi/2, -1e-2),
]
pinger_position = CylindricalPosition(15, 0, 5)

#### frequency information ####
signal_frequency = 40e3
# used as ADC sampling frequency and for "digital" portion
sampling_frequency = 20*signal_frequency
# picked to be much higher so it's approximately continuous and can be used in "analog" portion
continuous_sampling_frequency = 100*signal_frequency
# TODO: double check pinger on-off frequency
carrier_frequency = 1
pinger_tx_pulse_len = 4e-3

#### pinger intensity ####
pinger_intensity = 177 # dB re 1uPa @1m
attenuation_coeff = 0.02 #TODO: add details in the description here