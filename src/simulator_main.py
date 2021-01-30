'''
UBC Subbots
Project Dolphin
Sound Localization Simulator
Main Simulation File
'''
import argparse
import os
import logging
from sim_utils import config_parser, output_utils
from datetime import datetime
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d
import matplotlib.pyplot as plt
from importlib import import_module
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

args = parser.parse_args()
time.ctime(os.path.getmtime(file))

# create logger object for this module
logger = output_utils.initialize_logger(__name__)

##################################################
# Import Config File Dynamically From File Path
##################################################
sim_config = import_module(args.config)

##################################################
# main Simulation Tasks
##################################################
if __name__ == "__main__":
	# construct simulation chain from configuration file
	logger.info("Parsing simulator chain...")
	simulation_chain = config_parser.generate_sim_chain(sim_config.simulation_chain)

	# create initial simulation data frame from configuration file
	frame = config_parser.generate_frame(sim_config)

	# create initial simulation signal
	sim_signal = None
	position_list = []
	print("starting signal propagation...")
	for i in range(sim_config.num_iterations):
		print("Current iteration: %0d" % i)
		# propagate simulation signal and data frame through the chain
		for stage in simulation_chain:
			sim_signal = stage.apply(sim_signal)
			frame = stage.write_frame(frame)
		
		position_list.append(sim_signal) 

	plot_results(position_list)

	# write resulting frame to the output files
	pickle_path = "output/" + args.config + "/" + args.outfile_name + ".p"
	xml_path = "output/" + args.config + "/" + args.outfile_name + ".xml"

	# check if output directory exists and if not create it
	if not os.path.exists(os.path.dirname(pickle_path)):
		os.makedirs(os.path.dirname(pickle_path))
		
	output_utils.create_output_file(frame, pickle_path, xml_path)

def plot_results(position_list):
	hx = [cyl_to_cart(pos).x     for pos in sim_config.hydrophone_positions]
	hy = [cyl_to_cart(pos).y     for pos in sim_config.hydrophone_positions]
	x  = [polar_to_cart2d(pos).x for pos in position_list]
	y  = [polar_to_cart2d(pos).y for pos in position_list]
	px = cyl_to_cart(sim_config.pinger_position).x
	py = cyl_to_cart(sim_config.pinger_position).y
	gx = polar_to_cart2d(sim_config.simulation_chain[-1]["initial_guess"]).x
	gy = polar_to_cart2d(sim_config.simulation_chain[-1]["initial_guess"]).y

	f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

	h = ax1.hist2d(hx, hy, bins=40, range=[[-5e-2, 5e-2], [-5e-2, 5e-2]])
	ax1.set_xlabel("x (m)")
	ax1.set_ylabel("y (m)")
	ax1.set_title("Hydrophone Distribution")
	f.colorbar(h[3], ax=ax1)

	h = ax2.hist2d(x, y, density=True, range=[[-50, 50], [-50, 50]], bins=40)
	ax2.scatter(hx, hy, label="Hydrophone", c = 'white')
	ax2.scatter(px, py, label="Pinger", c='orange')
	ax2.scatter(gx, gy, label="Position Guess", c = 'red')
	ax2.set_xlabel("x (m)")
	ax2.set_ylabel("y (m)")
	sigma_string = r'$\sigma = $' + str(round(sim_config.simulation_chain[1]["sigma"], 2))
	ax2.set_title("Distribution for Pinger Position Results %s" % sigma_string)
	ax2.legend(loc='lower left')
	f.colorbar(h[3], ax=ax2)

	plt.show()