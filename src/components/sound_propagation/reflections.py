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


class reflections:

    def __init__(self, bottom_density, bottom_soundspeed, pool_depth, rx_depth, rx_range, surface, tx_depth, out_info,
                bottom_absorption= 0, bottom_roughness= 0, frequency= global_vars.signal_frequency, max_angle= 80, min_angle= -80, nbeams= 0):
        self.bottom_density = bottom_density
        self.bottom_soundspeed = bottom_soundspeed
        self.pool_depth = pool_depth
        self.rx_depth = rx_depth
        self.rx_range = rx_range
        self.surface = surface
        self.tx_depth = tx_depth
        self.out_info = out_info # type of information/output watned
        self.bottom_absorption = bottom_absorption
        self.bottom_roughness = bottom_roughness
        self.frequency = frequency
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.nbeams = nbeams


    def apply(self, sim_signal):
        # sim_signal - should i make this the voltage level of the pinger output? 
        
        # initialize BELLHOP environmnet with inputs
        env = initialize_bellhop(self.bottom_density, self.bottom_soundspeed, self.pool_depth, self.rx_depth, self.rx_range, global_vars.speed_of_sound, self.surface, 
                self.tx_depth, self.bottom_absorption, self.bottom_roughness, self.frequency, self.max_angle, self.min_angle, self.nbeams)

        if self.out_info == 'toa':
            return pm.compute_arrivals(env)
        elif self.out_info == 'rays':
            return pm.compute_eigenrays(env)
        elif self.out_info == 'tloss':
            return pm.compute_transmission_loss(env)
        else:
            return 0 # no output type selected

    def write_frame(self, frame):
        pass


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
