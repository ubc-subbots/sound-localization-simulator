from components.chain import Chain

import numpy as np
import jsonpickle
import pprint
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition, CylindricalPosition

from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.tdoa_calc.cross_correlation_stage import CrossCorrelationStage
from stages.localization.multilateration.nls import NLSPositionCalc
from sim_utils import plt_utils
from matplotlib.pyplot import show
from sim_utils.output_utils import initialize_logger

from experiment import Experiment

class DefaultExp(Experiment):
    results = None
    frame = None

    # Create simulation chain
    def __init__(self):
        self.logger = initialize_logger(__name__)
        self.results = []  # Position list

        # Modify global constants
        global_vars.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(1.85e-2, 0, 0),
            CylindricalPosition(1.85e-2, np.pi, 0),
            CylindricalPosition(1.2e-2, -np.pi/10, 1.2e-2),
            CylindricalPosition(1.2e-2, -np.pi+np.pi/10, 1.2e-2),
        ]

        global_vars.pinger_position = CylindricalPosition(10, 0, 10)
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
            NLSPositionCalc(optimization_type=OptimizationType.nelder_mead)
        )

    # Execute here
    def apply(self):
        self.results = []
        for i in range(global_vars.num_iterations):
            self.results.append(self.simulation_chain.apply())
            self.frame = self.simulation_chain.frame

        return self.results

    def display_results(self):
        if self.results:
            plt_utils.plot_calculated_positions(self.results, self.initial_guess, self.sigma)
            show()
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = default_exp()
    exp_results = experiment.apply()
    pprint.pprint(experiment.frame, sort_dicts=False)
    experiment.display_results()
