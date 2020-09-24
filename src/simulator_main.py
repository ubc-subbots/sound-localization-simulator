'''
UBC Subbots
Sound Localization Simulator
Main Simulation File
Authors:
'''
##################################################
# Process Command Line Args
##################################################

import argparse
import logging

parser = argparse.ArgumentParser(description='Sound Localization System Simulator')
parser.add_argument('-c', '--config', default = "default_config", type = str,
        help = "The configuration file name used for the simulation run.")
parser.add_argument('-l', '--log_level', default = "INFO", type = str, 
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        help = "The level of verbosity with which the simulator will dump logging information")
parser.add_argument('-n', '--vary_noise', action="store_true",
        help = "Vary noise values.")
parser.add_argument('-p', '--vary_pinger', action="store_true",
        help = "Vary true pinger position.")
parser.add_argument('-g', '--vary_guess', action="store_true",
        help = "Vary initial guess pinger position.")
parser.add_argument('-s', '--vary_sensor', action="store_true",
        help = "Vary hydrophone positions.")

args = parser.parse_args()
config_path = args.config
logger = logging.getLogger("sim_logger")
logger.setLevel(args.log_level)

##################################################
# Import Config File Dynamically From File Path
##################################################
from importlib import import_module
sim_config = import_module(args.config)

##################################################
# main Simulation Tasks
##################################################
if __name__ == "__main__":
        pass
