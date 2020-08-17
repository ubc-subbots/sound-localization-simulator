## @package input_generation
#  Generates various input signals for the simulator
#
#  Input signals are fed into the component chain and propagated through it
#  in order to generate the simulation frame output data.
import numpy as np
from collections import namedtuple

# TODO: documentation lmfaoooo
def generate_square_wave(sampling_frequency, square_wave_frequency, measurement_period, phase_time):

    sign_change_frequency = square_wave_frequency * 2

    t_sign_changes = np.linspace(0,
                                 measurement_period,
                                 measurement_period * sign_change_frequency)
    t_sampling = np.linspace(0,
                             measurement_period,
                             measurement_period * sampling_frequency)


    t_sign_changes = t_sign_changes + phase_time

    t_sign_changes = np.nonzero(t_sign_changes < measurement_period)[0]

    sample_iter = iter(t_sampling)
    t_sample = next(sample_iter)
    output = list()
    high = True
    for t_sign_change in t_sign_changes:
        high = not high
        while t_sample < t_sign_change:
            output.append(1 if high else 0)
            t_sample = next(sample_iter)

    return np.array(output)

## Generates a sin wave signal that could be fed into the component chain.
#
#  @param sampling_frequency    The frequency at which the wave is sampled. Consecutive samples
#                               are separated by units of time equalling 1/sample_frequency
# @param sine_wave_frequency    The frequency with which the wave oscillates. Two wave samples
#                               separated by units of time equalling 1/sine_wave_frequency will
#                               have the same value
# @param measurement_period     The number of time units to generate the wave for
# @param phase_time             Number of time units the phase of the wave will be delayed by
#
# @return   A numpy array length measurement_period*sampling_frequency containing the sine wave
#           samples
def generate_sine_wave(sampling_frequency, sine_wave_frequency, measurement_period, phase_time):
    t_sampling = np.linspace(0,
                             measurement_period,
                             measurement_period * sampling_frequency)
    sine_wave_period = 1 / sine_wave_frequency
    phase = phase_time / (sine_wave_period) * 2 * np.pi

    return np.sin(2 * np.pi * sine_wave_frequency * t_sampling + phase)

Point = namedtuple('Point', ['x', 'y', 'z'])

def generate_hydrophone_response(pinger_location, hydrophone_location, measurement_period,
                                 sine_wave_frequency, carrier_frequency, sampling_frequency):

    c = 1480
    
    distance = ((pinger_location.x - hydrophone_location.x) ** 2 + 
                (pinger_location.y - hydrophone_location.y) ** 2 +
                (pinger_location.z - hydrophone_location.z) ** 2) ** (1/2)

    propogation_time = distance / c 
    sw_phase_time = propogation_time % (1/sine_wave_frequency)
    carrier_phase_time = propogation_time % (1/carrier_frequency)

    sine_wave = generate_sine_wave(sampling_frequency, sine_wave_frequency,
                                       measurement_period, sw_phase_time)
    carrier_wave = generate_square_wave(sampling_frequency, carrier_frequency,
                                       measurement_period, carrier_phase_time)
    
    return sine_wave * carrier_wave