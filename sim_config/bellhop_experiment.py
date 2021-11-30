from components.chain import Chain

import numpy as np
#import jsonpickle
import global_vars

from stages.reflection.hydrophone_response_stage import Hydrophone_Response_Stage
import sim_utils.plt_utils as plt
from sim_utils.output_utils import initialize_logger

from experiment import Experiment

class Experiment2(Experiment):
    results = None
    frames = None

    # Create simulation chain
    def __init__(self):
        self.logger = initialize_logger(__name__)
        self.results = []  # Position list

        # Modify global constants

        global_vars.speed_of_sound_mps = 2000

        # create initial simulation signal

        sim_signal = None

        self.simulation_chain = Chain(sim_signal)

        bottom_absorption = 0 # 0 for max reflection
        bottom_density = 1600 # default value
        bottom_roughness = 0 # 0 for max reflection
        bottom_soundspeed = 1500
        pool_depth = 11.58 # m
        frequency = 40000
        max_angle = 80
        min_angle = -80
        nbeams = 0
        rx_depth = 5
        rx_range = 10 # distance from tx
        soundspeed = bottom_soundspeed
        #pool_depth = np.array([[d,-1/19*d**2+0.3048*38] for d in np.linspace(0,rx_range,100)])
        surface = np.array([[r, 0.5+0.2*np.sin(2*np.pi*2*r)] for r in np.linspace(0,rx_range,1000)])
        tx_depth = 5 # depth of pinger

        self.simulation_chain.add_component(
            Hydrophone_Response_Stage(bottom_density, bottom_soundspeed, pool_depth, tx_depth, surface=None)
        )

    # Execute here
    def apply(self):
        self.results = self.simulation_chain.apply()
        return self.results

    def display_results(self):
        print(len(self.results))
        print(self.results[0].shape)
        plt.plot_signals(*self.results)
        plt.show()


if __name__ == '__main__':
    experiment = Experiment2()
    exp_results = experiment.apply()
    experiment.display_results()
