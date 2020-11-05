'''
UBC Subbots
Project Dolphin
Sound Localization Simulator
Main Simulation File
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
logger = logging.getLogger("sim_logger")
logger.setLevel(args.log_level)

##################################################
# Import Config File Dynamically From File Path
##################################################
from importlib import import_module
sim_config = import_module(args.config)

##################################################
# Construct Stage Chain
##################################################


##################################################
# main Simulation Tasks
##################################################
if __name__ == "__main__":
        pass
