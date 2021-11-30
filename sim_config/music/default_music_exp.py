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

class DefaultMusicExp(Experiment):
    results = None
    frames = None

    # Create simulation chain
    def __init__(self):
        self.logger = initialize_logger(__name__)

        array_spacing = 2/5 * global_vars.speed_of_sound/global_vars.signal_frequency

        # Modify global constants
        global_vars.hydrophone_positions = [
            CartesianPosition(0, 0, 0),
            CartesianPosition(array_spacing, 0, 0),
            CartesianPosition(-array_spacing, 0, 0),
            CartesianPosition(0, 0, array_spacing),
            CartesianPosition(array_spacing, 0, array_spacing),
            CartesianPosition(-array_spacing, 0, array_spacing),
        ]
        global_vars.pinger_position = CylindricalPosition(10, 0, 5)

        global_vars.sampling_frequency = 15*global_vars.signal_frequency
        global_vars.continuous_sampling_frequency = 100*global_vars.signal_frequency

        # create initial simulation signal\
        sim_signal = None

        self.simulation_chain = Chain(sim_signal)

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=20e-3, duty_cycle=4e-3)
        )

        self.sigma = 0.01
        self.simulation_chain.add_component(
            GaussianNoise(mu=0, sigma=self.sigma)
        )

        num_bits=12
        self.simulation_chain.add_component(
            IdealADCStage(num_bits=num_bits, quantization_method=QuantizationType.midtread)
        )

        # num_samples = int(
        #     10 * (global_vars.sampling_frequency / global_vars.signal_frequency))  # sample 10 cycles of the wave
        # threshold = 0.1 * (2 ** (num_bits-1))
        # self.simulation_chain.add_component(
        #     ThresholdCaptureTrigger(num_samples=num_samples, threshold=threshold)
        # )

        self.simulation_chain.add_component(
            MUSIC(resolution=np.pi/50, visualize_jmusic=False, xy_halfplane=True)
        )

    # Execute here
    def apply(self):
        resolution = np.pi/100
        self.param_vals = np.arange(0, np.pi, resolution)
        norm_factor = np.sqrt(global_vars.pinger_position.r**2 
                          + global_vars.pinger_position.z**2)
        theta = np.arccos(global_vars.pinger_position.z/norm_factor)
        
        # initial comparison dictionary
        theta_string = r'$\theta$'
        phi_string = r'$\phi$'
        self.actual_dict = {
            theta_string: [theta]*len(self.param_vals),
            phi_string: self.param_vals
        }
        
        # get simulation results dictionary
        self.results_dict = {
            theta_string: [],
            phi_string: []
        }
        for phi in self.param_vals:
            computed_theta = []
            computed_phi = []
            global_vars.pinger_position = CylindricalPosition(10, phi, 5)
            self.logger.info("Running simulation with pinger DOA at %.2f"%(phi*CONV_2_DEG))
            for i in range(global_vars.num_iterations):
                result = self.simulation_chain.apply()

                self.logger.info("System computed a DOA of (theta, phi) = (%.2f, %.2f)"
                                 %(result[0]*CONV_2_DEG, result[1]*CONV_2_DEG))
                self.logger.info("Actual DOA is (theta, phi) = (%.2f, %.2f)"
                                 %(theta*CONV_2_DEG, phi*CONV_2_DEG))

                computed_theta.append(result[0])
                computed_phi.append(result[1])

            self.results_dict[theta_string].append(computed_theta)
            self.results_dict[phi_string].append(computed_phi)

        return self.results_dict

    def display_results(self):
        if self.results_dict:
            # plot error
            plt.plt_param_sweep_abs_avg_error(self.param_vals, self.actual_dict, 
                            self.results_dict, title="Average Absolute DOA Error", 
                            ispolar=True, scaley=CONV_2_DEG, 
                            isangular_error=True)

        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = music_experiment()
    exp_results = experiment.apply()
    experiment.display_results()