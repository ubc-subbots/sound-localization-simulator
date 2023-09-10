import global_vars
from components.tdoa_calc.cross_correlation import CrossCorrelation
import numpy as np
import sim_utils.plt_utils as plt
import logging
from sim_utils.output_utils import initialize_logger
from sim_utils.common_types import *
import csv, numpy

# create logger object for this module
logger = initialize_logger(__name__)


class CrossCorrelationStage:

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

        # Test to inject CSV data directly into cross-correlation stage: successful!
        # Disabling for now -- can uncomment if we want to look into this further
        # Actual Read takes place in simulator_main, right at start and then is 
        # placed into sim_signal in input gen stage

        # if global_vars.input_type == InputType.csv:
        #     sim_signal_list = []
        #     with open('C:\\Users\\kiera\\OneDrive\\Documents\\SubBots\\ProjectDolphin\\MinimalSimulatorSystem\\src\\sim_utils\\cross_correlated.csv') as csv_file:
        #         csv_reader = csv.reader(csv_file, delimiter=',', lineterminator="\r")
        #         line_count = 0
        #         for row in csv_reader:
        #             sim_signal_list.append(numpy.asarray(list(map(numpy.int32, row))))
        #             line_count += 1
        #         print(f'Processed {line_count} lines.')
        #         sim_signal = tuple(sim_signal_list)
        #         csv_file.close()
        # else:
        #     print("no csv file provided: simulating data")

        phase_analysis_inputs = [
            (sim_signal[0], sim_signal[i+1])
            for i in range(self.num_components)
        ]

        tdoa =  tuple(
            component.apply(input_sig)
            for (component, input_sig) in zip(self.components, phase_analysis_inputs)
        )

        PHASE_SHIFT_ERROR = False

        if PHASE_SHIFT_ERROR:
            # Optional phase shift error insertion
            # Used to simulate variation in each hydrophones filters phase response
            # due to imperfect part tolerances
            
            # TODO: (kross) parameterize optional phase shift error
            phase_shift_error = 12
            group_delay_error = phase_shift_error/360 * (1/global_vars.signal_frequency)

            tdoa = list(tdoa)

            # Add/Subtract worst-case group delay error at random
            for group_delay_index in range(len(tdoa)):
                direction = np.random.choice([1,-1])
                tdoa[group_delay_index] = tdoa[group_delay_index] + direction*group_delay_error
                print("Phase shift " + str(group_delay_index + 1) + " has error " + str(direction*phase_shift_error))

            tdoa = tuple(tdoa)

        return tdoa

    def write_frame(self, frame):
        pass
