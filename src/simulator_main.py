
'''
UBC Subbots
Project Dolphin
Sound Localization Simulator
Main Simulation File
'''
import argparse
from datetime import datetime
from importlib import import_module
from sim_utils import output_utils
from sim_utils.common_types import *
import global_vars
import csv
import numpy
import random

def extract_experiment_class_name(experiment_name):
    exp_module_name = experiment_name.split(".")[-1]
    
    # split on underscores
    class_name_list = exp_module_name.split("_")
    # capitalize first letter for CamelCase
    class_name_list = [name.capitalize() for name in class_name_list]

    # return CamelCase experiment name
    return "".join(class_name_list)

if __name__ == "__main__":
    ##################################################
    # Process Command Line Args
    ##################################################
    parser = argparse.ArgumentParser(description='Sound Localization System Simulator')
    parser.add_argument('-e', '--experiment_name', default='default_exp', type=str, 
                        help='Experiment name to run')
    parser.add_argument('-n', '--num_iterations', default=1, type=int,
                        help="The number of iterations that the simulation performs through the component chain")
    parser.add_argument('-o', '--outfile_name',
                        default="sim_output_" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S"), type=str,
                        help="The file name for the simulator output.\n" +
                            "Output files <OUTFILE_NAME>.p and <OUTFILE_NAME>.xml will be located at <REPO_ROOT>/output/<CONFIG>/")
    parser.add_argument('-l', '--log_level', default="INFO", type=str,
                        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
                        help="The level of verbosity with which the simulator will dump logging information")
    parser.add_argument('-f', '--logfile_name', type=str,
                        help="The log file name used for the simulation run. If not passed, the experiment name is used")
    # parser.add_argument('-i', '--input_type', default='simulation', type=str,
    #                     help="Specify the type of input source for the hydrophone data: \nThe Options are:\nglobal_vars.InputSource.simulation\nglobal_vars.InputSource.csv\nglobal_vars.InputSource.shared_memory\nglobal_vars.InputSource.socket")
    parser.add_argument('-csv','--csv_filepath', type=str,
                        help="The file name for csv containing hydrophone data to use")

    args = parser.parse_args()
    global_vars.num_iterations = args.num_iterations

    ##################################################
    # Dynamic Configuration
    ##################################################
    # determine log file name
    if args.logfile_name:
        log_fname = args.logfile_name
    else:
        log_fname = args.experiment_name

    # configure logging parameters
    output_utils.configure_logger(args.log_level, log_fname)

    # Import the experiment module
    experiment_module = import_module(args.experiment_name)

    # Import the experiment class
    class_name = extract_experiment_class_name(args.experiment_name)
    Experiment_class = getattr(experiment_module, class_name)
    # create logger object for this module
    logger = output_utils.initialize_logger(__name__)

    # If a CSV file is specified, read all lines into hydrophone signal list
    if args.csv_filepath:
        global_vars.input_type = InputType.csv
        with open(args.csv_filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', lineterminator="\r")
            line_count = 0
            for row in csv_reader:
                global_vars.hydrophone_signal_list.append(numpy.asarray(list(map(float, row))))
                line_count += 1
            print(f'Processed {line_count} lines from CSV.')
    # Otherwise, simulate the data
    else:
        print("No CSV file provided, simulating data.")


    ##################################################
    # main Simulation Tasks
    ##################################################
    
    # Instantiate the class. Try loading from a previous run.
    # experiment = Experiment_class.load()  # type: Experiment
    # if experiment is None:

    
    # experiment = Experiment_class(radiusPinger=(25), radiusGuess=(25))

    # # Run
    # results = experiment.apply()
    # experiment.display_results()

    # experiment.dump()

    # for pinger_radius in [0.11, 0.5, 1, 3]:
    #     for pinger_angle in [np.pi/5, np.pi/3, 3*np.pi/4]:
    #         for guess_radius in [0.1, 0.51, 1.4, 2]:
            
    #             experiment = Experiment_class(pingerRadius=(pinger_radius), pingerAngle=(pinger_angle), guessRadius=(guess_radius))

    #             # Run
    #             results = experiment.apply()
    #             #experiment.display_results()

    #             experiment.dump()
    #         print("")
    #     print("")
    # print("")
            
    # for pinger_radius in [60]:
    #     for pinger_angle in [3*np.pi/4]:
    #         for guess_radius in [49,51]:
            
    #             experiment = Experiment_class(pingerRadius=(pinger_radius), pingerAngle=(pinger_angle), guessRadius=(guess_radius))

    #             # Run
    #             results = experiment.apply()
    #             #experiment.display_results()

    #             experiment.dump()
    #         print("")
    #     print("")
    # print("")

    for pinger_radius in random.sample(range(1, 80), 5):
        for pinger_angle in random.sample(range(0, 100), 3):
            
            experiment = Experiment_class(pingerRadius=(pinger_radius), pingerAngle=(np.pi/100*pinger_angle), guessRadius=(10))

            # Run
            results = experiment.apply()
            #experiment.display_results()

            experiment.dump()
        print("")
    print("")
