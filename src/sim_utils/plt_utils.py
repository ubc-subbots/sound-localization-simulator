import matplotlib.pyplot as plt
from matplotlib.pyplot import show
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d
from simulator_main import sim_config as cfg

def plot_calculated_positions(position_list):
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
	sigma_string = r'$\sigma = $' + str(round(cfg.simulation_chain[1]["sigma"], 2))
	ax2.set_title("Distribution for Pinger Position Results %s" % sigma_string)
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