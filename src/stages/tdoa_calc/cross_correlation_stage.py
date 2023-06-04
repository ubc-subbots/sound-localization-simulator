import global_vars
from components.tdoa_calc.cross_correlation import CrossCorrelation
import numpy as np
import sim_utils.plt_utils as plt
import logging
from sim_utils.output_utils import initialize_logger
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

        if 1:
            sim_signal_list = []
            with open('C:\\Users\\kiera\\OneDrive\\Documents\\SubBots\\ProjectDolphin\\MinimalSimulatorSystem\\src\\sim_utils\\cross_correlated.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',', lineterminator="\r")
                line_count = 0
                for row in csv_reader:
                    sim_signal_list.append(numpy.asarray(list(map(numpy.int32, row))))
                    line_count += 1
                print(f'Processed {line_count} lines.')
                sim_signal = tuple(sim_signal_list)
        else:
            print("no csv file provided: simulating data")
        #global_vars.DataList.append(sim_signal)
        print(sim_signal)
        print(type(sim_signal))
        print(type(sim_signal[0]))
        print(type(sim_signal[0][0]))
        # with open('sim_utils\\cross_correlated.csv', 'w') as csv_file:
        #     csv_writer = csv.writer(csv_file, delimiter=',', lineterminator="\r")
        #     csv_writer.writerows(sim_signal)
        #     #csv_writer.writerows([[1,2,3,4],[5,6,8,3],[26,3,5,7]])
        
        #     print("Finished")
        #     print( global_vars.DataList)
        #     csv_file.close()


        phase_analysis_inputs = [
            (sim_signal[0], sim_signal[i+1])
            for i in range(self.num_components)
        ]

        tdoa =  tuple(
            component.apply(input_sig)
            for (component, input_sig) in zip(self.components, phase_analysis_inputs)
        )

        return tdoa

    def write_frame(self, frame):
        pass
