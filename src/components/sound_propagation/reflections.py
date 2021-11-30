'''@package reflections
The component modelling sound reflections underwater using BELLHOPS

@author Kota Chang
@date Jul 2, 2021
'''

import numpy as np
from sim_utils.common_types import *
import global_vars
import arlpy.uwapm as pm
import arlpy
import arlpy.plot as plt
import matplotlib.pyplot as pyplot
import math
from datetime import date, datetime
from sim_utils.output_utils import initialize_logger

# create logger object for this module

class Reflections:

    def __init__(self, bottom_density, bottom_soundspeed, pool_depth, rx_depth, 
                 rx_range, tx_depth, surface= None, bottom_absorption= 0, 
                 bottom_roughness= 0, max_angle= 80, min_angle= -80, nbeams= 0, 
                 randomize_FFVS= 0):
        """
        :param float bottom_density: if density is varying, need to specify a density profile
        :param float bottom_soundspeed: if soundspeed is varying, need to specify a sound speed profile
        :param float pool_depth:
        :param float rx_depth:
        :param float rx_range:
        :param float tx_depth:
        :param ndarray_or_None surface: if not specified, the top surface will just be a straight line
        :param float bottom_absorption: set to 0 for max reflections
        :param float bottom_roughness: set to 0 for max reflections
        :param float max_angle: maximum detection angle for the receiver
        :param float min_angle: minimum detection angle for the receiver
        :param int nbeams: number of beams(?) this parameter doesn't affect the output for some reason
        :param bool randomize_FFVS: add option to randomize the free field voltage sensitivity for the hydrophone response
        """
        self.logger = initialize_logger(__name__)
        
        self.bottom_density = bottom_density
        self.bottom_soundspeed = bottom_soundspeed
        self.pool_depth = pool_depth
        self.rx_depth = rx_depth
        self.rx_range = rx_range
        self.tx_depth = tx_depth
        self.surface = surface
        self.bottom_absorption = bottom_absorption
        self.bottom_roughness = bottom_roughness
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.nbeams = nbeams
        self.randomize_FFVS = randomize_FFVS

    def apply(self, sim_signal):

        time_obj = datetime.now()
        start_time = time_obj.microsecond
        # sim_signal = technically the pinger signal, but since this is the first component in the chain, not necessary
        # pinger signal magnitude defined in global_vars
        #TODO: if possible, get measurements with a physical pinger
        
        # initialize BELLHOP environmnet with inputs
        env = initialize_bellhop(
            self.bottom_density, 
            self.bottom_soundspeed, 
            self.pool_depth, 
            self.rx_depth, 
            self.rx_range, 
            global_vars.speed_of_sound, 
            self.surface, 
            self.tx_depth, 
            self.bottom_absorption, 
            self.bottom_roughness, 
            global_vars.signal_frequency, 
            self.max_angle, 
            self.min_angle, 
            self.nbeams
        )
        
        # get time of arrivals from various reflections
        arrivals = pm.compute_arrivals(env)
        #pm.plot_arrivals(arrivals, width=900)
        impulse_resp =  pm.arrivals_to_impulse_response(
            arrivals, 
            fs=global_vars.continuous_sampling_frequency,
            abs_time = True
        )
        
        #pyplot.figure()
        #pyplot.plot(np.abs(impulse_resp))
        #pyplot.title("impulse response")

        # convolution of the impulse response from the reflection simulation (bellhop) and the pinger pressure wave
        superposition = convolution(np.abs(impulse_resp))
        #pyplot.figure()
        #pyplot.plot(superposition[0:len(impulse_resp)])
        #pyplot.title("convolution")
        #pyplot.show()

        # get the FFVS from hydrophone datasheet and calculate the hydrophone voltage response
        FFVS = free_field_voltage_sensitivity(
            global_vars.signal_frequency, 
            self.randomize_FFVS
        )
        hydrophone_response_output = hydrophone_response(FFVS, superposition)
  
        # report total sim time
        time_obj = datetime.now()
        sim_time = time_obj.microsecond - start_time
        self.logger.info("Simulation Time was", sim_time, "microseconds")

        return hydrophone_response_output

    def write_frame(self, frame):
        pass

# create and return bellop environment
def initialize_bellhop(bottom_density, bottom_soundspeed, pool_depth, rx_depth, rx_range, soundspeed, surface, tx_depth,
                bottom_absorption, bottom_roughness, frequency, max_angle, min_angle, nbeams):
    pm.models()
    env = pm.create_env2d(
        bottom_absorption = bottom_absorption,
        bottom_density = bottom_density,
        bottom_roughness = bottom_roughness,
        bottom_soundspeed = bottom_soundspeed,
        depth = pool_depth,
        frequency = frequency,
        max_angle = max_angle,
        min_angle = min_angle,
        nbeams = nbeams,
        rx_depth = rx_depth,
        rx_range = rx_range,
        soundspeed = soundspeed,
        surface = surface,
        tx_depth = tx_depth
    )
    #pm.print_env(env)
    return env

def convolution(impulse_response):
    dt = 1/global_vars.continuous_sampling_frequency
    n_points = global_vars.pinger_tx_pulse_len/dt # pinger lasts 4ms TODO: double check this from pinger datasheet
    
    #TODO: add more details for attenuation coefficient for underwater acoustics (in global_vars)
    # find a range of values and will change them during simulation
    I_1m = 10**(global_vars.pinger_intensity/20)*1 # units in uPa
    I_0m = I_1m/math.exp(-global_vars.attenuation_coeff)

    pressure_wave = np.zeros(int(n_points)) # pressure wave output from the pinger
    for i in range(len(pressure_wave)):
        pressure_wave[i] =I_0m* math.sin(2*math.pi*global_vars.signal_frequency*(dt*i))

    return np.convolve(pressure_wave, impulse_response)

def free_field_voltage_sensitivity(frequency, randomize_FFVS):
    FFVS = None
    if (randomize_FFVS):
        FFVS = np.random.randint(-208,-211)
    else:      
        if (frequency <= 30e3):
            FFVS = -208
        else:
            FFVS = -211
    return FFVS

def hydrophone_response(FFVS,pressure):
    output = 10**(FFVS/20)*pressure
    return output