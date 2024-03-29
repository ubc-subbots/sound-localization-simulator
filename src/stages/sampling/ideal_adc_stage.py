from components.sampling.ideal_adc import IdealADC
import global_vars
import numpy as np
from sim_utils.output_utils import initialize_logger
import logging
from sim_utils.plt_utils import plot_signals

class IdealADCStage:
    '''
    stage to simulate an ADC for every hydrophone signal channel
    '''

    def __init__(self, num_bits, quantization_method):
        # create logger object for this module
        self.logger = initialize_logger(__name__)
        self.num_bits = num_bits
        self.quantization_method = quantization_method

        # as many channels as there are hydrophones
        self.num_components = len(global_vars.hydrophone_positions)

        # Create IdealADCs
        self.components = []
        for i in range(self.num_components):
            self.components.append(
                IdealADC(num_bits, quantization_method)
            )

    def apply(self, sim_signal):
        level = self.logger.getEffectiveLevel()
        if level <= logging.DEBUG:
            plot_signals(*sim_signal, title="Input to ADC")        

        return tuple(
            np.array(component.apply(sig))
            for (component, sig) in zip(self.components, sim_signal)
        )

    def write_frame(self, frame):
        pass