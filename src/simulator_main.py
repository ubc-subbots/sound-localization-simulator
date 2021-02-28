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
import numpy as np
from importlib import import_module
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d, distance_3Dpoints
from sim_utils import output_utils

def default_run_mode():
	simulation_chain = config_parser.generate_sim_chain(sim_config.simulation_chain)

	# create initial simulation data frame from configuration file
	frame = config_parser.generate_frame(sim_config)

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

def parameter_sweep_mode():
	if "sweep_param" not in args:
		logger.exception("Sweep parameter not set")
	elif "min" not in args:
		logger.exception("Sweep parameter minimum value not set")
	elif "max" not in args:
		logger.exception("Sweep parameter maxmimum value not set")
	elif "step" not in args:
		logger.exception("Sweep parameter step size not set")

	# initialize error lists
	phi_mean_abs_err = []
	phi_max_abs_err = []
	r_mean_abs_err = []
	r_max_abs_err = []

	param_name = args.sweep_param
	param_min = args.min
	param_max = args.max
	param_step = args.step

	# sweep through specified paramter
	logger.info("Sweeping through parameter %s" % param_name)
	logger.info((
		"Sweeping Parameters -> min value: %.3f, max_value: %.3f, step: %.3f" 
		%(param_min, param_max, param_step)
	))
	param_vals = np.arange(param_min, param_max+param_step, param_step)
	for val in param_vals:
		logger.info("Current value of %s: %.3f" %(param_name, val))
		setattr(sim_config, param_name, val)
		sim_config.regenerate_positions()

		# construct simulation chain from configuration file
		logger.info("Parsing simulator chain...")
		simulation_chain = config_parser.generate_sim_chain(sim_config.simulation_chain)

		# create initial simulation data frame from configuration file
		frame = config_parser.generate_frame(sim_config)

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
		if args.plot_position:
			plt.plot_calculated_positions(position_list, sweep_param=args.sweep_param)

		# calculate error parameters
		r_error = [
			distance_3Dpoints(position, sim_config.pinger_position)
			for position in position_list
		]
		phi_error = [
			np.arccos(np.cos(position.phi - sim_config.pinger_position.phi)) * 180/np.pi
			for position in position_list
		]

		phi_mean_abs_err.append(sum(phi_error)/len(phi_error))
		phi_max_abs_err.append(max(phi_error))
		r_mean_abs_err.append(sum(r_error)/len(r_error))
		r_max_abs_err.append(max(r_error))

	titles = [
		"Mean Absolute Angular Error",
		"Max Absolute Angular Error",
		"Mean Absolute Distance Error",
		"Max Absolute Distance Error"
	]

	y_labels = [
		"Error (Degrees)",
		"Error (Degrees)",
		"Error (Meters)",
		"Error (Meters)",
	]

	plt.plot_param_sweep_results(
		param_name, param_vals, args.num_iterations, phi_mean_abs_err, 
		r_mean_abs_err, titles=titles, y_labels=y_labels)

def configure_cmd_args():
	parser = argparse.ArgumentParser(description='Sound Localization System Simulator')
	parser.add_argument('-c', '--config', default = "default_config", type = str,
			help = "The configuration file name used for the simulation run.")
	parser.add_argument('-m', '--mode', default = "default", type = str,
			choices=["default", "sweep"],
			help = (
				"Specifies the mode the simulator will run in. default mode"
				"iterates over the specified configuration as a 'normal'"
				"simulation run. sweep mode will allow you to iterate over the"
				"value of a parameter and plot error with respect to those values."
			))
	parser.add_argument('-p', '--sweep_param', type = str, default=argparse.SUPPRESS,
			help = "The parameter to sweep through in the simulator")
	parser.add_argument('--min', type = float, default=argparse.SUPPRESS,
			help = "Minimum value of sweep parameter")
	parser.add_argument('--max', type = float, default=argparse.SUPPRESS,
			help = "Maximum value of sweep parameter")
	parser.add_argument('--step', type = float, default=argparse.SUPPRESS,
			help = "Step size of parameter sweep")
	parser.add_argument('-o', '--outfile_name', 
			default = "sim_output_" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S"), type = str, 
			help = "The file name for the simulator output.\n" + 
			"Output files <OUTFILE_NAME>.p and <OUTFILE_NAME>.xml will be located at <REPO_ROOT>/output/<CONFIG>/")
	parser.add_argument('-l', '--log_level', default = "INFO", type = str, 
			choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
			help = "The level of verbosity with which the simulator will dump logging information")
	parser.add_argument('-n', '--num_iterations', default = 1, type = int,
			help = "The number of iterations that the simulation performs through the component chain")
	parser.add_argument('--plot_position', action = 'store_true',
			help = "Plot the calculated pinger positions at the end of a run")

	return parser.parse_args()

##################################################
# Process Command Line Args
##################################################
args = configure_cmd_args()

##################################################
# Dynamically Configure
##################################################
sim_config = import_module(args.config)

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

	if args.mode == "default":
		default_run_mode()
	elif args.mode == "sweep":
		parameter_sweep_mode()

	# construct simulation chain from configuration file
	logger.info("Parsing simulator chain...")
	plt.show()