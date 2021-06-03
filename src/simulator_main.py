'''
UBC Subbots
Project Dolphin
Sound Localization Simulator
Main Simulation File
'''
import argparse
import os
import logging
from datetime import datetime
from importlib import import_module
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d
from sim_utils import output_utils
import global_vars

##################################################
# Process Command Line Args
##################################################
parser = argparse.ArgumentParser(description='Sound Localization System Simulator')
parser.add_argument('-c', '--config', default="default_config", type=str,
                    help="The configuration file name used for the simulation run.")
parser.add_argument('-o', '--outfile_name',
                    default="sim_output_" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S"), type=str,
                    help="The file name for the simulator output.\n" +
                         "Output files <OUTFILE_NAME>.p and <OUTFILE_NAME>.xml will be located at <REPO_ROOT>/output/<CONFIG>/")
parser.add_argument('-l', '--log_level', default="INFO", type=str,
                    choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
                    help="The level of verbosity with which the simulator will dump logging information")
parser.add_argument('-n', '--num_iterations', default=1, type=int,
                    help="The number of iterations that the simulation performs through the component chain")
parser.add_argument('-e', '--experiment', default='1', type=int, help='Experiment number to run')

args = parser.parse_args()
global_vars.num_iterations = args.num_iterations

##################################################
# Dynamically Configure
##################################################
# sim_config = import_module(args.config)

# configure logging parameters
output_utils.configure_logger(args.log_level, args.config)

# contain dependency to config so must be imported afterwards
import sim_utils.plt_utils as plt
from sim_utils import config_parser
from experiments.experiment import Experiment

##################################################
# main Simulation Tasks
##################################################
if __name__ == "__main__":
    # create logger object for this module
    logger = output_utils.initialize_logger(__name__)

    # create initial simulation data frame from configuration file
    frame = config_parser.generate_frame(global_vars)

    # Import the module
    experiment_module = import_module(f'experiments.experiment{str(args.experiment)}')

    # Import the class
    Experiment_class = getattr(experiment_module, f'Experiment{str(args.experiment)}')

    # Instantiate the class. Try loading from a previous run.
    experiment = Experiment_class.load()  # type: Experiment
    if experiment is None:
        experiment = Experiment_class()

    # Run
    results = experiment.apply()
    experiment.display_results()

    experiment.dump()
