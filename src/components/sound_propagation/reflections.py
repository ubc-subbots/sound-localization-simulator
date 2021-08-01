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
import math


class reflections:

    def __init__(self, bottom_density, bottom_soundspeed, pool_depth, rx_depth, rx_range, tx_depth,
                surface= None, bottom_absorption= 0, bottom_roughness= 0, frequency= global_vars.signal_frequency, max_angle= 80, min_angle= -80, nbeams= 0, randomize_FFVS= 0):
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
        :param float frequency:
        :param float max_angle: maximum detection angle for the receiver
        :param float min_angle: minimum detection angle for the receiver
        :param int nbeams: number of beams(?) this parameter doesn't affect the output for some reason
        :param bool randomize_FFVS: add option to randomize the free field voltage sensitivity for the hydrophone response
        """
        self.bottom_density = bottom_density
        self.bottom_soundspeed = bottom_soundspeed
        self.pool_depth = pool_depth
        self.rx_depth = rx_depth
        self.rx_range = rx_range
        self.tx_depth = tx_depth
        self.surface = surface
        self.bottom_absorption = bottom_absorption
        self.bottom_roughness = bottom_roughness
        self.frequency = frequency
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.nbeams = nbeams
        self.randomize_FFVS = randomize_FFVS


    def apply(self, sim_signal):
        # sim_signal - should i make this the voltage level of the pinger output? 
        
        # initialize BELLHOP environmnet with inputs
        env = initialize_bellhop(self.bottom_density, self.bottom_soundspeed, self.pool_depth, self.rx_depth, self.rx_range, global_vars.speed_of_sound, self.surface, 
                self.tx_depth, self.bottom_absorption, self.bottom_roughness, self.frequency, self.max_angle, self.min_angle, self.nbeams)
        
        # get time of arrivals from various reflections
        arrivals = pm.compute_arrivals(env)
        toa = arrivals['time_of_arrival'].array

        # convolution of the impulse response from the reflection simulation (bellhop) and the pinger pressure wave
        superposition = convolution(toa)

        # get the FFVS from hydrophone datasheet and calculate the hydrophone voltage response
        return hydrophone_response(free_field_voltave_sensitivity(global_vars.signal_frequency, self.randomize_FFVS), superposition)

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

def convolution(toa):
    n_points = global_vars.pinger_tx_pulse_len*global_vars.continuous_sampling_frequency + 1
    dt = 1/global_vars.continuous_sampling_frequency
    impulse_response = np.zeros(n_points)

    #TODO: talk about reflections received after 4ms - include or ignore? when do we cut it off?
    #TODO: leave for now but log how long the simulation took - ask dvir
    for i in range(len(toa)):
        impulse_response[math.floor(toa[i]/dt)] = toa[i]
    
    #TODO: figure out attenuation coefficient for underwater acoustics
    #TODO: find a range of values and will change them during simulation
    pressure_wave = np.zeros(n_points) # pressure wave output from the pinger
    for i in range(len(pressure_wave)):
        pressure_wave[i] = math.sin(2*math.pi*global_vars.signal_frequency*(dt*i))

    return np.convolve(impulse_response,pressure_wave)

def free_field_voltave_sensitivity(frequency, randomize_FFVS):
    #TODO: discuss required accuracy for the FFVS values (25-20kHz)
    #TODO: add option to randomize to account for manufacturing defects
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