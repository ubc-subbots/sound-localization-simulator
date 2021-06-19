import global_vars
from components.tdoa_calc.phase_analysis import PhaseAnalysis
import numpy as np
from sim_utils import plt_utils as plt
import logging
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)


class PhaseAnalysisStage(Component):

    def __init__(self):
        super().__init__()
        # always using hydrophone 0 as reference
        self.num_components = len(global_vars.hydrophone_positions) - 1

        self.components = []
        for i in range(self.num_components):
            identifier = "Phase Analysis" + "[%0d]" % (i + 1)
            self.components.append(
                PhaseAnalysis(identifier=identifier)
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

        self.signal = tuple(
            component.apply(input_sig)
            for (component, input_sig) in zip(self.components, phase_analysis_inputs)
        )

        return self.signal

