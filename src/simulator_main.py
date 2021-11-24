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
import global_vars


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
    Experiment_class = getattr(experiment_module, args.experiment_name)
    # create logger object for this module
    logger = output_utils.initialize_logger(__name__)

    ##################################################
    # main Simulation Tasks
    ##################################################
    
    # Instantiate the class. Try loading from a previous run.
    experiment = Experiment_class.load()  # type: Experiment
    if experiment is None:
        experiment = Experiment_class()

    # Run
    results = experiment.apply()
    experiment.display_results()

    experiment.dump()
