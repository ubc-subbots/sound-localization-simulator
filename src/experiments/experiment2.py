from components.chain import Chain

import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition, CylindricalPosition

from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.tdoa.cross_correlation_stage import CrossCorrelationStage
from components.position_calc.nls_position_calc import NLSPositionCalc
from components.position_calc.initial_position_estimator import InitialPositionEstimator
import sim_utils.plt_utils as plt
from sim_utils.output_utils import initialize_logger

from experiments.experiment import Experiment

class Experiment2(Experiment):
    results = None
    frames = None

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
        global_vars.num_iterations = 10

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

        # self.simulation_chain.add_component(
        #     InitialPositionEstimator()
        # )

        self.simulation_chain.add_component(
            NLSPositionCalc(optimization_type=OptimizationType.nelder_mead, guess_at_init=False)
        )

    # Execute here
    def apply(self):
        self.results = {}
        angles = np.linspace(-np.pi, np.pi, 20)
        for angle in angles:
            self.results[angle] = []
            print("angle:", angle)
            global_vars.pinger_position = CylindricalPosition(10, angle, 5)
            for i in range(global_vars.num_iterations):
                print("iteration:")
                self.results[angle].append(self.simulation_chain.apply().phi)
                self.frames = self.simulation_chain.frames

        return self.results

    def display_results(self):
        if self.results:
            plt.plot_average_error_polar(self.results)
            plt.show()
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = Experiment2()
    exp_results = experiment.apply()
    experiment.display_results()
