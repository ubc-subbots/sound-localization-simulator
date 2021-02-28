import matplotlib.pyplot as plt
from matplotlib.pyplot import show
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d
from simulator_main import sim_config as cfg
from sim_utils.output_utils import initialize_logger
import numpy as np

# create logger object for this module
logger = initialize_logger(__name__)

def plot_calculated_positions(position_list, sweep_param=None):
	'''
	plots the 2D graph showing the pinger position, hydrophone position,
	pinger initial guess, and calculated position distribution
	'''
	hx = [cyl_to_cart(pos).x     for pos in cfg.hydrophone_positions]
	hy = [cyl_to_cart(pos).y     for pos in cfg.hydrophone_positions]
	x  = [polar_to_cart2d(pos).x for pos in position_list]
	y  = [polar_to_cart2d(pos).y for pos in position_list]
	px = cyl_to_cart(cfg.pinger_position).x
	py = cyl_to_cart(cfg.pinger_position).y
	gx = polar_to_cart2d(cfg.simulation_chain[-1]["initial_guess"]).x
	gy = polar_to_cart2d(cfg.simulation_chain[-1]["initial_guess"]).y

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
	if sweep_param is not None:
		param_string = "%s = %.2f" %(sweep_param, getattr(cfg, sweep_param))
	else:
		param_string = r'$\sigma = $' + str(round(cfg.simulation_chain[1]["sigma"], 2))
	ax2.set_title("Distribution for Pinger Position Results %s" % param_string)
	ax2.legend(loc='lower left')
	f.colorbar(h[3], ax=ax2)

def plot_signals(*signals, title="Hydrophone Signals"):
    plt.figure()
    i=0
    for signal in signals:
        plt.plot(signal, label="hydrophone %0d"%i)
        i += 1
    plt.title(title)
    plt.legend()

def plt_histograms(*hists, titles=None, sup_title = None):
	'''
	@brief  Methods to display multiple histograms at once. Subplot 
			orientation adaptively configured

	@param *hists       The distributions to be displayed
	@param title        A list of titles corresponding to each subplot
	@param sup_title    The super title of the entire figure (not super title 
						if None)
	'''
	rows = int(np.sqrt(len(hists)))
	cols = int(np.ceil(len(hists) / rows))

	if not titles:
		titles = [
			"hist " + str(i)
			for i in range(len(hists))
		]

	logger.info("Plotting %0d rows and %0d columns" %(rows, cols))

	f, axs = plt.subplots(rows, cols)
	if sup_title:
		f.suptitle(sup_title)

	axs = axs.flatten()
	for i in range(len(hists)):
		bins_num = int(max(hists[i]) - min(hists[i]))
		axs[i].hist(hists[i], bins=bins_num, histtype='step')
		axs[i].set_title(titles[i])

def plot_param_sweep_results(param_name, param_vals, num_iter, *evaluation_data, 
							 titles=None, y_labels=None):
	'''
    @brief  Methods to display multiple histograms at once. Subplot 
            orientation adaptively configured

    @param *evaluation_data    	The results from the parameter sweep.
    @param title        		A list of titles for each subplot.
    @param y_labels        		A list of y axis labels for each subplot.
    @param sup_title    		The super title of the entire figure
    '''
	rows = int(np.sqrt(len(evaluation_data)))
	cols = int(np.ceil(len(evaluation_data) / rows))

	logger.info("Plotting %0d rows and %0d columns" %(rows, cols))

	f, axs = plt.subplots(rows, cols)
	f.suptitle("Sweep Results for %s. %0d Iterations per Value" %(param_name, num_iter))

	axs = axs.flatten()
	for i in range(len(evaluation_data)):
		axs[i].set_xlabel(param_name)
		axs[i].plot(param_vals, evaluation_data[i])
		if titles is not None:
			axs[i].set_title(titles[i])
		if y_labels is not None:
			axs[i].set_ylabel(y_labels[i])
		axs[i].set_xlabel(param_name)