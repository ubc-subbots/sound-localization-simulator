from components.position_calc.NLS_position_calc import NLS_position_calc, get_squared_error_sum
from components.position_calc import position_calc_utils
from simulator_main import sim_config as cfg
from sim_utils.common_types import *
import numpy as np
import matplotlib.pyplot as plt

# set global configuration
cfg.speed_of_sound = 1500 #m/s
cfg.hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(3e-2, -np.pi/2, 0),
    CylindricalPosition(3e-2, 0, 0),
    CylindricalPosition(3e-2, np.pi/2, 0),
    CylindricalPosition(3e-2, np.pi, 0),
]
cfg.pinger_position = CylindricalPosition(15, np.pi/5, 5)

#####################################################
# Fixed Pinger and Initial Guess
#####################################################


def visualize_NLS_data(pinger_guess, noise_stdev, n_iters, plot_error_hist=False):
    initial_guess = pinger_guess
    opt_type = OptimizationType.nelder_mead
    component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess)

    true_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([cfg.pinger_position.r, cfg.pinger_position.phi]), hydrophone_position, True)
                for hydrophone_position in cfg.hydrophone_positions[1:])

    NLS_outputs = []
    for i in range(n_iters):
        noise = [np.random.normal(0, noise_stdev*TIME_CONV['us']) for j in range(len(true_tdoa))]
        tdoa = [tdoa_val+noise_val for tdoa_val,noise_val in zip(true_tdoa, noise)]
        predicted_pos = component.apply(tdoa)
        NLS_outputs.append(predicted_pos)

    r_err = [(pos.r - cfg.pinger_position.r) for pos in NLS_outputs]
    phi_err = [(pos.phi - cfg.pinger_position.phi)*CONV_2_DEG for pos in NLS_outputs]
    x = [cyl_2_cart(pos).x for pos in NLS_outputs]
    y = [cyl_2_cart(pos).y for pos in NLS_outputs]

    if (plot_error_hist):
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        f.suptitle( "NLS Error Distribution. Guess: r=" + str(round(pinger_guess.r,1)) + r', $\phi = ' + 
                    str(round(pinger_guess.phi*CONV_2_DEG,1)) + r', \sigma = $' + str(noise_stdev))
        ax1.hist(r_err, histtype='step', density=True)
        ax1.set_title("Radial Distance Error")
        ax1.set_xlabel(r'$\Delta r$ (m)')
        ax1.set_ylabel("Normalized Count")
        ax2.hist(phi_err, histtype='step', density=True)    
        ax2.set_title("Angular Error")
        ax2.set_xlabel(r'$\Delta \phi (^\circ)$')

    hx = [cyl_2_cart(pos).x for pos in cfg.hydrophone_positions]
    hy = [cyl_2_cart(pos).y for pos in cfg.hydrophone_positions]

    plt.figure()
    h = plt.hist2d(x, y, density=False, range=[[-50, 50], [-50, 50]], bins=40)
    plt.scatter(hx, hy, label="Hydrophone", c = 'white')
    plt.scatter(cyl_2_cart(cfg.pinger_position).x, cyl_2_cart(cfg.pinger_position).y, 
                label="Pinger", c='orange')
    plt.scatter(pol_2_cart2d(initial_guess).x, pol_2_cart2d(initial_guess).y, 
                label="Position Guess", c = 'red')
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Distribution for NLS Position Predictions. Noise " +r'$\sigma = $' + str(noise_stdev))
    plt.legend(loc='lower left')
    plt.colorbar(h[3])

visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 0, 1000)
visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 0.5, 1000)
visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, 1000)
visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 5, 1000)

plt.show()