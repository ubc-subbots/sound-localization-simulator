'''@package ideal_adc
The component modelling an ideal analog to digital converter (ADC) 

@author Dvir Hilu
@date Jan 20, 2021
'''

from components.component import Component
import numpy as np
from sim_utils.common_types import *
import global_vars


class IdealADC(Component):

    def __init__(self, num_bits, quantization_method):
        self.num_bits = num_bits
        self.quantization_method = quantization_method
        
    def apply(self, sim_signal):
        # downsamples signal from global_vars.continuous_sampling_frequency to global_vars.sampling_frequency
        sampled_signal = downsample(sim_signal, global_vars.continuous_sampling_frequency, global_vars.sampling_frequency)
        # map signal from continuous values to an unsigned integers of size self.num_bits
        # uses either midrise or midtread quantization as specified by self.quantization_method
        quantized_signal = quantize(sampled_signal, self.num_bits, self.quantization_method)

        # turn into signed integer representation
        quantized_signal -= 2**(self.num_bits-1)
        
        self.signal = quantized_signal
        return quantized_signal


def downsample(signal, fs_old, fs_new):
    # adjust new signal length based on sampling rate reduction
    index_sample_rate = fs_new / fs_old
    new_length = int(round(index_sample_rate*len(signal)))

    # selectively keep indices at correct interval
    sampled_signal = [
        signal[int(round(i/index_sample_rate))]
        for i in range(new_length)
    ]

    return np.array(sampled_signal)


def quantize(signal, num_bits, quantization_method):
    # number of quantization levels
    L = 2**num_bits

    # shift signal to start at 0
    sig = signal - min(signal)
    
    # find quantization delta
    delta = max(sig) / L

    if quantization_method == QuantizationType.midrise:
        quantized_signal = [
            int(value/delta)
            for value in sig 
        ]
    elif quantization_method == QuantizationType.midtread:
        quantized_signal = [
            int(value/delta + 0.5)
            for value in sig
        ]
    else:
        raise ValueError(f"Illegal Quantization Type: {str(type(quantization_method))}")

    return np.array(quantized_signal)
