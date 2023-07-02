## @package input_generation
#  Generates various input signals for the simulator
#
#  Input signals are fed into the component chain and propagated through it
#  in order to generate the simulation frame output data.
import csv, os

import numpy as np
from scipy import signal
from collections import namedtuple
import global_vars
from sim_utils.common_types import * # TODO: figure out why this feels wrong

class InputGeneration:
    """ Input generation is a simple class for simulating the input to our hydrophones.
        The class as is simply multiplies a square wave by a sine wave. It more accurately
        represents the output of the pinger more than the response of the hydrophone, but for
        prototyping purposes it takes in hydrophone + pinger distances and calculates the phase.
    """
    def __init__(self, hydrophone_position, measurement_period, duty_cycle):
        self.hydrophone_position = hydrophone_position
        self.measurement_period = measurement_period
        self.duty_cycle = duty_cycle
        self.listofarrays = []
        self.counter = 0

    def _square_wave(self, sampling_frequency, square_wave_frequency,
                      measurement_period, duty_cycle):
        """Creates a square wave. This is used as a box function over a sine wave to turn it off and on.

        @param sampling_frequency     The frequency at which the wave is sampled. Consecutive samples
                                      are separated by units of time equalling 1/sample_frequency
        
        @param square_wave_frequency  The frequency with which the wave oscillates. The square wave
                                      value flips between zero and one every 1/(2*square_wave_frequency)
                                      units of time

        @param measurement_period     The number of time units to generate the wave for
        @param duty_cycle             Duty cycle of the wave

        @return                       A numpy array representing the voltages sampled from the square wave.
                                    
        """
        t_sampling = np.linspace(0,
                                 measurement_period,
                                 int(measurement_period * sampling_frequency))

        # generates a square wave between -1 and 1
        square_wave = signal.square(2 * np.pi * square_wave_frequency * t_sampling, duty=duty_cycle)
        # set wave minimum to 0
        square_wave += 1
        # divide by 2 to get wave maximum of 1
        square_wave /= 2.0
        
        return square_wave
    
    def _sine_wave(self, sampling_frequency, sine_wave_frequency, measurement_period, phase_time):
        """
        Generates a sin wave signal that could be fed into the component chain.
        
        @param sampling_frequency     The frequency at which the wave is sampled. Consecutive samples
                                      are separated by units of time equalling 1/sample_frequency
        @param sine_wave_frequency    The frequency with which the wave oscillates. Two wave samples
                                      separated by units of time equalling 1/sine_wave_frequency will
                                      have the same value
        @param measurement_period     The number of time units to generate the wave for
        @param phase_time             Number of time units the phase of the wave will be delayed by
        
        @return   A numpy array length measurement_period * sampling_frequency containing the sine wave
                  samples
        """
        sine_wave_period = 1 / sine_wave_frequency
        phase = phase_time / (sine_wave_period) * 2 * np.pi
        t_sampling = np.linspace(0,
                                measurement_period,
                                int(measurement_period * sampling_frequency))

        return np.sin(2 * np.pi * sine_wave_frequency * t_sampling + phase)
    
    def _add_leading_zeros(self, signal, propogation_time):
        num_zeros = propogation_time * global_vars.continuous_sampling_frequency
        return np.concatenate(
            (np.zeros(int(num_zeros)), signal),
            axis=None
        )

    def apply(self, input_signal):
        """
        Generates the signal received by the four hydrophones

        @param input_signal Unused parameter. This is here so that the object adheres to the standard
                            stage interface.
        
        @return A 4-tuple of the signal received by each hydrophone. This is in the form of a sine
                wave multiplied by a square wave with leading zeros. The number of leading zeros
                in the signal is normalized such that each hydrophone has
                <expected number of leading zeros of the closest hydrophone> less than expected.
                This is to remove leading zeros that do not affect analysis.
        """

        # If no CSV was specified, generate the simulated data normally
        if global_vars.input_type == InputType.simulation:
            distance = distance_3Dpoints(self.hydrophone_position, global_vars.pinger_position)
            
            propogation_time = distance / global_vars.speed_of_sound
            leading_zeros_t = propogation_time

            sine_wave = self._sine_wave(
                global_vars.continuous_sampling_frequency,
                global_vars.signal_frequency,
                self.measurement_period - leading_zeros_t,
                0
            )

            sine_wave = self._add_leading_zeros(sine_wave, leading_zeros_t)

            carrier_wave = self._square_wave(
                global_vars.continuous_sampling_frequency,
                global_vars.carrier_frequency,
                self.measurement_period - leading_zeros_t, 
                self.duty_cycle
            )

            carrier_wave = self._add_leading_zeros(carrier_wave, leading_zeros_t)

            return sine_wave * carrier_wave

        # If a CSV was specified, use the data from it as the generated input instead
        elif global_vars.input_type == InputType.csv:
            global_vars.nth_hydrophone += 1

            return global_vars.hydrophone_signal_list[global_vars.nth_hydrophone]
