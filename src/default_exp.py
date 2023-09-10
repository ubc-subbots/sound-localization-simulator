from components.chain import Chain

import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import *

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
    frames = None

    # Create simulation chain
    def __init__(self, pingerRadius = 10, pingerAngle = np.pi/2, guessRadius = 10):
        self.logger       = initialize_logger(__name__)
        self.results      = []  # Position list
        self.pingerRadius = pingerRadius
        self.pingerAngle  = pingerAngle
        self.guessRadius  = guessRadius

        # Modify global constants
        global_vars.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(1.85e-2, 0, 0),
            CylindricalPosition(1.85e-2, np.pi, 0),
            CylindricalPosition(1.2e-2, -np.pi/10, 1.2e-2),
            CylindricalPosition(1.2e-2, -np.pi+np.pi/10, 1.2e-2),
        ]

        global_vars.pinger_position = CylindricalPosition(self.pingerRadius, self.pingerAngle, 10)

        # this must be modified globally to actually change how the simulator runs
        # guessAngle is iterated through using NLS position calc so a dummy value is used here
        global_vars.initial_guess=PolarPosition(self.guessRadius, np.pi)

        # create initial simulation signal

        sim_signal = None

        self.simulation_chain = Chain(sim_signal)

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=0.4, duty_cycle=0.05)
        )

        self.sigma = 0.01
        if global_vars.input_type == InputType.simulation:
            self.simulation_chain.add_component(
                GaussianNoise(mu=0, sigma=self.sigma)
            )
            global_vars.phase_shift_error = 2.5
            print("Adding a randomized phase-shift-error to each hydrophone of plus/minus " + str(global_vars.phase_shift_error) + " degrees")

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
        
        #this will only be cosmetic, the global variable must be modified to changew how the simulator runs
        self.initial_guess = global_vars.initial_guess


        self.simulation_chain.add_component(
            NLSPositionCalc(optimization_type=OptimizationType.angle_nls, radiusGuess=self.guessRadius)
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
            plt_utils.plot_calculated_positions(self.results, self.initial_guess, self.sigma)
            show()
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = DefaultExp(pingerRadius=(25), guessRadius=(25))
    exp_results = experiment.apply()
    experiment.display_results()