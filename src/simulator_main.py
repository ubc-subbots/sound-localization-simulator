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
parser.add_argument('-c', '--config', default = "default_config", type = str,
        help = "The configuration file name used for the simulation run.")
parser.add_argument('-o', '--outfile_name', 
		default = "sim_output_" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S"), type = str, 
		help = "The file name for the simulator output.\n" + 
		"Output files <OUTFILE_NAME>.p and <OUTFILE_NAME>.xml will be located at <REPO_ROOT>/output/<CONFIG>/")
parser.add_argument('-l', '--log_level', default = "INFO", type = str, 
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        help = "The level of verbosity with which the simulator will dump logging information")
parser.add_argument('-n', '--num_iterations', default = 1, type = int,
        help = "The number of iterations that the simulation performs through the component chain")

args = parser.parse_args()

##################################################
# Dynamically Configure
##################################################
#sim_config = import_module(args.config)

# configure logging parameters
output_utils.configure_logger(args.log_level, args.config)

# contain dependency to config so must be imported afterwards
import sim_utils.plt_utils as plt
from sim_utils import config_parser

##################################################
# main Simulation Tasks
##################################################
if __name__ == "__main__":
	# create logger object for this module
	logger = output_utils.initialize_logger(__name__)

	# construct simulation chain from configuration file
	logger.info("Parsing simulator chain...")
	simulation_chain = config_parser.generate_sim_chain(global_vars.simulation_chain)

	# create initial simulation data frame from configuration file
	frame = config_parser.generate_frame(global_vars)

	# create initial simulation signal
	sim_signal = None
	position_list = []
	logger.info("starting signal propagation...")
	for i in range(args.num_iterations):
		logger.info("Current iteration: %0d" % i)
		# propagate simulation signal and data frame through the chain
		for stage in simulation_chain:
			sim_signal = stage.apply(sim_signal)
			frame = stage.write_frame(frame)
		
		position_list.append(sim_signal) 

	# plot results
	plt.plot_calculated_positions(position_list)

	# write resulting frame to the output files
	pickle_path = "output/" + args.config + "/" + args.outfile_name + ".p"
	xml_path = "output/" + args.config + "/" + args.outfile_name + ".xml"

	# check if output directory exists and if not create it
	if not os.path.exists(os.path.dirname(pickle_path)):
		os.makedirs(os.path.dirname(pickle_path))
	
	output_utils.create_output_file(frame, pickle_path, xml_path)
	plt.show()