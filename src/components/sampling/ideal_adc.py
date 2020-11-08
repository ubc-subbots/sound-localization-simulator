import numpy as np
from sim_utils.common_types import *
from simulator_main import sim_config as cfg
import matplotlib.pyplot as plt

class IdealADC:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def apply(self, sim_signal):
        sampled_signal = downsample(sim_signal, cfg.continuous_sampling_frequency, cfg.sampling_frequency)
        quantized_signal = quantize(sampled_signal, self.num_bits, self.quantization_method)

        return quantized_signal

    def write_frame(self, frame):
        pass

def downsample(signal, fs_old, fs_new):
    index_sample_rate = fs_new / fs_old
    new_length = int(round(index_sample_rate*len(signal)))

    sampled_indices = [int(round(index_sample_rate*i)) for i in range(new_length)]

    return signal[sampled_indices]

def quantize(signal, num_bits, quantization_method):
    # number of quantization levels
    L = 2**num_bits

    # shift signal to start at 0
    sig = signal - min(signal)
    
    # find quantization delta
    delta = max(sig) / L

    if (quantization_method == QuantizationType.midrise):
        quantized_signal = [
            int(value/delta)
            for value in sig 
        ]
    elif (quantization_method == QuantizationType.midtread):
        quantized_signal = [
            int(value/delta + 0.5)
            for value in sig
        ]
    else:
        raise ValueError("Illegal Quanitzation Type: " + str(type(quantization_method)))

    return quantized_signal