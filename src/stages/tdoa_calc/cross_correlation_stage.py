import global_vars
from components.tdoa_calc.cross_correlation import CrossCorrelation
import numpy as np
import sim_utils.plt_utils as plt
import logging
from sim_utils.output_utils import initialize_logger
from stages.stage import Stage

# create logger object for this module
logger = initialize_logger(__name__)


class CrossCorrelationStage(Stage):

    def __init__(self):

        # always using hydrophone 0 as reference
        self.num_components = len(global_vars.hydrophone_positions) - 1

        # Create CrossCorrelation
        self.components = []
        for i in range(self.num_components):
            identifier = "Cross Correlation Stage" + "[%0d]" % (i + 1)
            self.components.append(
                CrossCorrelation(identifier=identifier)
            )

    def apply(self, sim_signal):
        # plot hydrophone signals if log level in debug mode
        level = logger.getEffectiveLevel()
        if level <= logging.DEBUG:
            plt.plot_signals(*sim_signal, title="Sampled and Quantized Signals")

        phase_analysis_inputs = [
            (sim_signal[0], sim_signal[i+1])
            for i in range(self.num_components)
        ]

        self.signal =  tuple(
            component.apply(input_sig)
            for (component, input_sig) in zip(self.components, phase_analysis_inputs)
        )

        return self.signal
