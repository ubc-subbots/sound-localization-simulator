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
       
Point = namedtuple('Point', ['x', 'y', 'z'])

def generate_hydrophone_response(pinger_location, hydrophone_location, measurement_period,
                                 square_wave_frequency, carrier_frequency, sampling_frequency):

    c = 1480
    
    distance = ((pinger_location.x - hydrophone_location.x) ** 2 + 
                (pinger_location.y - hydrophone_location.y) ** 2 +
                (pinger_location.z - hydrophone_location.z) ** 2) ** (1/2)

    propogation_time = distance / c 
    sw_phase_time = propogation_time % (1/square_wave_frequency)
    carrier_phase_time = propogation_time % (1/carrier_frequency)

    square_wave = generate_square_wave(sampling_frequency, square_wave_frequency,
                                       measurement_period, sw_phase_time)
    carrier_wave = generate_square_wave(sampling_frequency, carrier_frequency,
                                       measurement_period, carrier_phase_time)
    
    return square_wave * carrier_wave

        


