#!/usr/bin/env python

import position_calc_utils
import numpy as np

class NLS_position_calc:
    
    def __init__(self, name = "NLS_position_calc"):
        self.name = name
        self.frame_data = {}
    
    def apply(self, sim_signal):

        pass

    def write_frame(self, frame):
        pass

    def get_squared_error_sum(self, pinger_location, *hydrophone_times):
        squared_error_sum = 0
        for hydrophone_location in hydrophone_times:
            expected_delta_t = position_calc_utils.tdoa_function_3D(pinger_location, hydrophone)
            actual_delta_t = hydrophone.delta_t
            squared_error_sum += (actual_delta_t - expected_delta_t) ** 2

        return squared_error_sum