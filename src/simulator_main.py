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

args = parser.parse_args()

config_path = args.config
logger = logging.getLogger("sim_logger")
logger.setLevel(args.log_level)

##################################################
# Import Config File Dynamically From File Path
##################################################
import imp

