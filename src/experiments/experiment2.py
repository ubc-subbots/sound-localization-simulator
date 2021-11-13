from components.chain import Chain

import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition, CylindricalPosition

from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.tdoa.music import MUSIC
import sim_utils.plt_utils as plt
from matplotlib.pyplot import show
from sim_utils.output_utils import initialize_logger

from experiments.experiment import Experiment

class Experiment2(Experiment):
    results = None
    frames = None

    # Create simulation chain
    def __init__(self):
        self.logger = initialize_logger(__name__)
        self.results = []  # Position list

        array_spacing = 1e-2

        # Modify global constants
        global_vars.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(array_spacing, 0, 0),
            CylindricalPosition(2*array_spacing, 0, 0),
            CylindricalPosition(array_spacing, np.pi, 0),
            CylindricalPosition(2*array_spacing, np.pi, 0),
        ]

        global_vars.pinger_position = CylindricalPosition(10, 3*np.pi/4, 0)

        global_vars.sampling_frequency = 800e3

        # create initial simulation signal\
        sim_signal = None

        self.simulation_chain = Chain(sim_signal)

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=10e-3, duty_cycle=4e-3)
        )

        # self.sigma = 0.01
        # self.simulation_chain.add_component(
        #     GaussianNoise(mu=0, sigma=self.sigma)
        # )

        num_bits=12
        self.simulation_chain.add_component(
            IdealADCStage(num_bits=num_bits, quantization_method=QuantizationType.midtread)
        )

        num_samples = int(
            10 * (global_vars.sampling_frequency / global_vars.signal_frequency))  # sample 10 cycles of the wave
        threshold = 0.05 * (2 ** (num_bits-1))
        self.simulation_chain.add_component(
            ThresholdCaptureTrigger(num_samples=num_samples, threshold=threshold)
        )

        self.simulation_chain.add_component(
            MUSIC(resolution=np.pi/50, visualize_jmusic=True)
        )

    # Execute here
    def apply(self):
        self.results = []
        for i in range(global_vars.num_iterations):
            self.results.append(self.simulation_chain.apply())
            self.frames = self.simulation_chain.frames

        return self.results

    def display_results(self):
        if self.results:
            # plt.plot_calculated_positions(self.results, self.initial_guess, self.sigma)
            # plt.show()
            self.logger.info("Plotting not configured")
            self.logger.info("Simulation Results: ")
            self.logger.info(self.results)
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = Experiment1()
    exp_results = experiment.apply()
    experiment.display_results()
    show()
