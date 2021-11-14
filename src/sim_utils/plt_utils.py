import matplotlib.pyplot as plt
import numpy as np
from sim_utils.common_types import cyl_to_cart, polar_to_cart2d
import global_vars

def plot_calculated_positions(position_list, initial_guess, sigma):
    '''
    plots the 2D graph showing the pinger position, hydrophone position,
    pinger initial guess, and calculated position distribution
    '''
    hx = [cyl_to_cart(pos).x for pos in global_vars.hydrophone_positions]
    hy = [cyl_to_cart(pos).y for pos in global_vars.hydrophone_positions]
    x  = [polar_to_cart2d(pos).x for pos in position_list]
    y  = [polar_to_cart2d(pos).y for pos in position_list]
    px = cyl_to_cart(global_vars.pinger_position).x
    py = cyl_to_cart(global_vars.pinger_position).y
    gx = polar_to_cart2d(initial_guess).x
    gy = polar_to_cart2d(initial_guess).y

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

    h = ax1.hist2d(hx, hy, bins=40, range=[[-5e-2, 5e-2], [-5e-2, 5e-2]])
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax1.set_title("Hydrophone XY Distribution")
    f.colorbar(h[3], ax=ax1)

    h = ax2.hist2d(x, y, density=True, range=[[-50, 50], [-50, 50]], bins=40)
    ax2.scatter(hx, hy, label="Hydrophones", c = 'white')
    ax2.scatter(px, py, label="Pinger", c='orange')
    ax2.scatter(gx, gy, label="Initial Guess", c = 'red')
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    sigma_string = r'$\sigma = $' + str(round(sigma, 2))
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

def plt_param_sweep_abs_avg_error(param_vals, actual_vals, sim_results, title, 
                                  ispolar=False, scaley=1, scalex=1,
                                  isangular_error=False):
    average_errors = []
    for actual, result in zip(actual_vals, sim_results):
        if isangular_error:
            # convert to range 0->2pi before finding the error
            error = [
                np.abs((actual)%(2*np.pi)-(calculated)%(2*np.pi)) 
                for calculated in result
            ]
        else:
            error = [np.abs(actual-calculated) for calculated in result]
        average_errors.append(sum(error)/len(error))
    
    param_vals = np.array(param_vals)
    average_errors = np.array(average_errors)
    fig = plt.figure()
    if ispolar:
        ax = fig.add_subplot(111, projection='polar')
    else:
        ax = fig.add_subplot(111)
    ax.plot(param_vals*scalex, average_errors*scaley)
    plt.title(title)
    plt.show()