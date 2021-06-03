## @package input_generation
#  Generates various input signals for the simulator
#
#  Input signals are fed into the component chain and propagated through it
#  in order to generate the simulation frame output data.
import numpy as np
from collections import namedtuple
import sim_utils.sim_config as config

class InputGeneration:
    """ Input generation is a simple class for simulating the input to our hydrophones.
        The class as is simply multiplies a square wave by a sine wave. It more accurately
        represents the output of the pinger more than the response of the hydrophone, but for
        prototyping purposes it takes in hydrophone + pinger distances and calculates the phase.
    """
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])


    def _square_wave(self, sampling_frequency, square_wave_frequency,
                      measurement_period, phase_time):
        """Creates a square wave. This is used as a box function over a sine wave to turn it off and on.

        @param sampling_frequency     The frequency at which the wave is sampled. Consecutive samples
                                      are separated by units of time equalling 1/sample_frequency
        
        @param square_wave_frequency  The frequency with which the wave oscillates. The square wave
                                      value flips between zero and one every 1/(2*square_wave_frequency)
                                      units of time

        @param measurement_period     The number of time units to generate the wave for
        @param phase_time             Number of time units the phase of the wave will be delayed by

        @return                       A numpy array representing the voltages sampled from the square wave.
                                    
        """
        sign_change_frequency = square_wave_frequency * 2

        t_sign_changes = np.linspace(0,
                                     measurement_period,
                                     measurement_period * sign_change_frequency)
        t_sampling = np.linspace(0,
                                 measurement_period,
                                 measurement_period * sampling_frequency)


        t_sign_changes = t_sign_changes + phase_time

        t_sign_changes = t_sign_changes[t_sign_changes < measurement_period]

        return np.array(self.__generate_square_wave(t_sampling, t_sign_changes))

    def __generate_square_wave(self, t_sampling, t_sign_changes):
        """ Helper function for _square_wave. This function generates an array of 0s and 1s matching a square wave
            with the given sampling times and sign change times.

            @param t_sampling       The times that the function samples the square wave at
            @param t_sign_changes   The times that the square wave changes sign

            return                  A numpy array representing the voltages sampled from the square wave.

        """
        sample_iter = iter(t_sampling)
        t_sample = next(sample_iter)
        output = []
        high = True

        for t_sign_change in t_sign_changes:
            high = not high
            while t_sample < t_sign_change:
                output.append(1 if high else 0)
                t_sample = next(sample_iter)
        
        return output


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
                                measurement_period * sampling_frequency)

        return np.sin(2 * np.pi * sine_wave_frequency * t_sampling + phase)

    def apply(self, frame):
        
        distance = ((self.pinger_location.x - self.hydrophone_location.x) ** 2 + 
                    (self.pinger_location.y - self.hydrophone_location.y) ** 2 +
                    (self.pinger_location.z - self.hydrophone_location.z) ** 2) ** (1/2)

        propogation_time = distance / config.c 
        sine_wave_phase_time = propogation_time % (1 / self.sine_wave_frequency)
        carrier_phase_time = propogation_time % (1 / self.carrier_frequency)

        sine_wave = self._sine_wave(self.sampling_frequency, self.sine_wave_frequency,
                                     self.measurement_period, sine_wave_phase_time)

        carrier_wave = self._square_wave(self.sampling_frequency, self.carrier_frequency,
                                          self.measurement_period, carrier_phase_time)
        
        return sine_wave * carrier_wave