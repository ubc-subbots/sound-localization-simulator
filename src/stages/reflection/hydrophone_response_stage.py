import global_vars
from components.sound_propagation.reflections import Reflections
from sim_utils.common_types import cyl_to_cart, CylindricalPosition
import numpy as np
import sim_utils.plt_utils as plt
import logging
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

class Hydrophone_Response_Stage:

    def __init__(self, bottom_density, bottom_soundspeed, pool_depth, tx_depth,
                surface= None, bottom_absorption= 0, bottom_roughness= 0, max_angle= 80, min_angle= -80, nbeams= 0, randomize_FFVS= 0):

        self.num_components = len(global_vars.hydrophone_positions)
        # hydrophone response
        self.components = []
        for i in range(self.num_components):
            
            rx_depth = tx_depth + global_vars.pinger_position.z - global_vars.hydrophone_positions[i].z
            ppos = cyl_to_cart(global_vars.pinger_position)
            if (type(global_vars.hydrophone_positions[i]) == CylindricalPosition):
                hpos = cyl_to_cart(global_vars.hydrophone_positions[i])
            else:
                hpos = global_vars.hydrophone_positions[i]
            rx_range = np.sqrt((ppos.x-hpos.x)**2 + (ppos.y-hpos.y)**2)
            
            self.components.append(
                Reflections(bottom_density, bottom_soundspeed, pool_depth, rx_depth, rx_range, tx_depth,
                surface, bottom_absorption, bottom_roughness, max_angle, min_angle, nbeams, randomize_FFVS)
            )

    def apply(self, sim_signal):
        print(self.num_components, len(self.components))
        return tuple(
            component.apply(sim_signal)
            for component in self.components
        )

    def write_frame(self, frame):
        pass
