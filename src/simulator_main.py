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
import os
import logging
from sim_utils import config_parser, output_parser
from datetime import datetime
import matplotlib.pyplot as plt

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

args = parser.parse_args()
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
	# construct simulation chain from configuration file
	print("Parsing simulator chain...")
	simulation_chain = config_parser.generate_sim_chain(sim_config.simulation_chain)

	# create initial simulation data frame from configuration file
	frame = config_parser.generate_frame(sim_config)

	# create initial simulation signal
	sim_signal = None
	print("starting signal propagation...")
	# propagate simulation signal and data frame through the chain
	for stage in simulation_chain:
		print("Current stage: %s" % stage.Component_name)
		sim_signal 	= stage.apply(sim_signal)
		frame = stage.write_frame(frame)

	print("Final Position:", sim_signal)

	from components.position_calc.position_calc_utils import tdoa_function_3D
	tdoa_vals = [
		tdoa_function_3D(sim_config.pinger_position, hydrophone_pos, True)
		for hydrophone_pos in sim_config.hydrophone_positions[1:]
	]

	print("Actual Time Differences:", tdoa_vals)

	plt.show()


	# write resulting frame to the output files
	pickle_path = "output/" + args.config + "/" + args.outfile_name + ".p"
	xml_path = "output/" + args.config + "/" + args.outfile_name + ".xml"

	# check if output directory exists and if not create it
	if not os.path.exists(os.path.dirname(pickle_path)):
		os.makedirs(os.path.dirname(pickle_path))
		
	output_parser.create_output_file(frame, pickle_path, xml_path)