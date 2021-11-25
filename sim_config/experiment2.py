from components.chain import Chain

import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import CONV_2_DEG, CartesianPosition, QuantizationType, CylindricalPosition

from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.localization.subspace.music import MUSIC
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

        array_spacing = 2/5 * global_vars.speed_of_sound/global_vars.signal_frequency

        # Modify global constants
        global_vars.hydrophone_positions = [
            CartesianPosition(0, 0, 0),
            CartesianPosition(array_spacing, 0, 0),
            CartesianPosition(2*array_spacing, 0, 0),
            CartesianPosition(-array_spacing, 0, 0),
            CartesianPosition(-2*array_spacing, 0, 0),
        ]

        global_vars.sampling_frequency = 15*global_vars.signal_frequency
        global_vars.continuous_sampling_frequency = 100*global_vars.signal_frequency

        # create initial simulation signal\
        sim_signal = None

        self.simulation_chain = Chain(sim_signal)

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=10e-3, duty_cycle=4e-3)
        )

        self.sigma = 0.01
        self.simulation_chain.add_component(
            GaussianNoise(mu=0, sigma=self.sigma)
        )

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
            MUSIC(resolution=np.pi/50, visualize_jmusic=False, halfplane=True)
        )

    # Execute here
    def apply(self):
        resolution = np.pi/100
        self.param_vals = np.arange(0, np.pi, resolution)
        self.actual = self.param_vals
        
        self.results = []
        for phi in self.param_vals:
            computed_vals = []
            global_vars.pinger_position = CylindricalPosition(10, phi, 0)
            for i in range(global_vars.num_iterations):
                computed_vals.append(self.simulation_chain.apply())
                # self.frames = self.simulation_chain.frames

            self.results.append(computed_vals)

        return self.results

    def display_results(self):
        if self.results:
            plt.plt_param_sweep_abs_avg_error(self.param_vals, self.actual, 
                            self.results, title="Average Absolute DOA Error", 
                            ispolar=True, scaley=CONV_2_DEG, 
                            isangular_error=True)
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = Experiment2()
    exp_results = experiment.apply()
    experiment.display_results()