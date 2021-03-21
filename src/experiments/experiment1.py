from components.chain import Chain

import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition

from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.tdoa.cross_correlation_stage import CrossCorrelationStage
from components.position_calc.nls_position_calc import NLSPositionCalc
import sim_utils.plt_utils as plt
from sim_utils.output_utils import initialize_logger

from experiments.experiment import Experiment

class Experiment1(Experiment):
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

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=2, duty_cycle=0.05)
        )

        self.sigma = 0.01
        self.simulation_chain.add_component(
            GaussianNoise(mu=0, sigma=self.sigma)
        )

        self.simulation_chain.add_component(
            IdealADCStage(num_bits=12, quantization_method=QuantizationType.midtread)
        )

        num_samples = int(
            10 * (global_vars.sampling_frequency / global_vars.signal_frequency))  # sample 10 cycles of the wave
        threshold = 0.05 * (2 ** 11)
        self.simulation_chain.add_component(
            ThresholdCaptureTrigger(num_samples=num_samples, threshold=threshold)
        )

        self.simulation_chain.add_component(
            CrossCorrelationStage()
        )

        self.initial_guess = PolarPosition(10, np.pi)
        self.simulation_chain.add_component(
            NLSPositionCalc(optimization_type=OptimizationType.nelder_mead, initial_guess=self.initial_guess)
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
            plt.plot_calculated_positions(self.results, self.initial_guess, self.sigma)
            plt.show()
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = Experiment1()
    exp_results = experiment.apply()
    experiment.display_results()
