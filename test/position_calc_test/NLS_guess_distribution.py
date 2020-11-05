from components.position_calc.NLS_position_calc import NLS_position_calc, get_squared_error_sum
from components.position_calc import position_calc_utils
from simulator_main import sim_config as cfg
from simulator_main import args
from sim_utils.common_types import *
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

# determine which parts run
vary_noise =        False
vary_pinger =       False
vary_guess =        False
vary_hydrophones =  False

class ChangingVariable(Enum):
    '''
    enum to decide the which variable is changing when plotting
    '''
    Noise = 0,
    HydrophonePositions = 1,
    PingerGuess = 2,
    PingerPosition = 3

# set global configuration
cfg.speed_of_sound = 1500 #m/s
cfg.hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(3*UNIT_PREFIX["centi"], -np.pi/2, 0),
    CylindricalPosition(3*UNIT_PREFIX["centi"], 0, 0),
    CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi/2, 0),
    CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi, 0),
]
cfg.pinger_position = CylindricalPosition(15, np.pi/5, 5)
n_iter = 300

def plot_xy_distribution(x,y, initial_data, change=""):
    '''
    @brief  creates a 2D colourplot showing the disribution of solutions found by the NLS 
            component. Contains information about relative hydrophone position, pinger position,
            and pinger guess.

    @param x                distribution of x coordinate of NLS solutions
    @param y                distribution of y coordinate of NLS solutions
    @param initial_data     Dictionary of initialization data used to construct the NLS component
    @param change           a string containing information about the variable being altered by 
                            the script. Passing this allows the titles of multiple plots produced 
                            by this script to track the current value of the changing variable    
    '''
    hx = [cyl_2_cart(pos).x for pos in cfg.hydrophone_positions]
    hy = [cyl_2_cart(pos).y for pos in cfg.hydrophone_positions]

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    
    h = ax1.hist2d(hx, hy, bins=40,
            range=[[-5*UNIT_PREFIX["centi"], 5*UNIT_PREFIX["centi"]], [-5*UNIT_PREFIX["centi"], 5*UNIT_PREFIX["centi"]]])
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax1.set_title("Hydrophone Distribution")
    f.colorbar(h[3], ax=ax1)
    
    h = ax2.hist2d(x, y, density=True, range=[[-50, 50], [-50, 50]], bins=40)
    ax2.scatter(hx, hy, label="Hydrophone", c = 'white')
    ax2.scatter(cyl_2_cart(cfg.pinger_position).x, cyl_2_cart(cfg.pinger_position).y, 
                label="Pinger", c='orange')
    ax2.scatter(pol_2_cart2d(initial_data["initial_guess"]).x, pol_2_cart2d(initial_data["initial_guess"]).y, 
                label="Position Guess", c = 'red')
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    ax2.set_title("Distribution for NLS Position Predictions" + change)
    ax2.legend(loc='lower left')
    f.colorbar(h[3], ax=ax2)

def plot_error_histograms(r_err, phi_err, change):
    '''
    @brief plots a histogram of error distribution in r and phi

    @param r_err    list of errors in r (xy plane radial distance error)
    @param phi_err  list of errors in phi (xy plane angular error)
    @param change   a string containing information about the variable being altered by the 
                    script. Passing this allows the titles of multiple plots produced by this
                    script to track the current value of the changing variable
    '''
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    f.suptitle("NLS Error Distribution" + change)
    ax1.hist(r_err, histtype='step', density=True)
    ax1.set_title("Radial Distance Error")
    ax1.set_xlabel(r'$\Delta r$ (m)')
    ax1.set_ylabel("Normalized Count")
    ax2.hist(phi_err, histtype='step', density=True)    
    ax2.set_title("Angular Error")
    ax2.set_xlabel(r'$\Delta \phi (^\circ)$')


def visualize_NLS_data(pinger_guess, noise_stdev, n_iters, change_var = ChangingVariable.Noise, 
                        plot_error_hist=False):
    '''
    @brief visualizes the results of the NLS_position_calc component

    @param pinger_guess     Initial guess for pinger position
    @param noise_stdev      Standard deviation of gaussian noise injected to time differences
                            (mean is 0)
    @param n_iters          Number of noise simulations performed before plotting results
    @param change_var       provides information about which variable is changing in simulation
                            run to determine what information gets printed in plot title. Takes
                            type ChangingVariable enum
    @param plot_error_hist  flag to determine if to output a histogram of angular and distance error
    '''
    initial_data = {
        "optimization_type" : OptimizationType.nelder_mead,
        "initial_guess"     : pinger_guess
    }
    component = NLS_position_calc(initial_data)

    def _true_time_of_arrival(hydrophone_position):
        return position_calc_utils.tdoa_function_3D(
            np.array([cfg.pinger_position.r, cfg.pinger_position.phi]),
            hydrophone_position,
            True
        )

    true_tdoa = tuple(
        _true_time_of_arrival(hydrophone_position)
        for hydrophone_position in cfg.hydrophone_positions[1:]
    )

    NLS_outputs = []
    for i in range(n_iters):
        noise = [np.random.normal(0, noise_stdev*UNIT_PREFIX['u']) for j in range(len(true_tdoa))]
        tdoa = [tdoa_val+noise_val for tdoa_val,noise_val in zip(true_tdoa, noise)]
        predicted_pos = component.apply(tdoa)
        NLS_outputs.append(predicted_pos)

    r_err = [(pos.r - cfg.pinger_position.r) for pos in NLS_outputs]
    phi_err = [(pos.phi - cfg.pinger_position.phi)*CONV_2_DEG for pos in NLS_outputs]
    x = [cyl_2_cart(pos).x for pos in NLS_outputs]
    y = [cyl_2_cart(pos).y for pos in NLS_outputs]

    if (change_var == ChangingVariable.Noise):
        change = " Noise " + r'$\sigma = $' + str(round(noise_stdev,1)) + r'$\mu s$'
    elif (change_var == ChangingVariable.HydrophonePositions):
        change = ""
    elif (change_var == ChangingVariable.PingerGuess):
        change = " Initial Guess: r=" + str(round(pinger_guess.r,1)) + " " + r'$\phi =$' + str(round(pinger_guess.phi*CONV_2_DEG,1))
    else:
        change = " Pinger Position: r=" + str(round(cfg.pinger_position.r,1)) + " " + r'$\phi =$' + str(round(cfg.pinger_position.phi*CONV_2_DEG,1)) + " " + "z=" + str(round(cfg.pinger_position.z,1))

    if (plot_error_hist):
        plot_error_histograms(r_err, phi_err, change)

    plot_xy_distribution(x, y, initial_data, change)


if __name__ == "__main__":
    #####################################################
    # Noise Variation Only
    #####################################################

    if (vary_noise):
        change_var = ChangingVariable.Noise
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 5, n_iter, change_var)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 0.5, n_iter, change_var)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 0, n_iter, change_var)

    #####################################################
    # Hydrophone Position Variation Only
    #####################################################

    if (vary_hydrophones):
        change_var = ChangingVariable.HydrophonePositions
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], -np.pi/2, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], 0, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], np.pi/2, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], np.pi, 0),
        ]

        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(3*UNIT_PREFIX["centi"], -np.pi/2, 0),
            CylindricalPosition(0, 0, 3*UNIT_PREFIX["centi"]),
            CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi/2, 0),
            CylindricalPosition(0, 0, -3*UNIT_PREFIX["centi"]),
        ]

        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)
        visualize_NLS_data(PolarPosition(30, 0), 1, n_iter, change_var)

        cfg.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], -np.pi/2, 0),
            CylindricalPosition(2*UNIT_PREFIX["centi"], 0, 0),
            CylindricalPosition(1*UNIT_PREFIX["centi"], np.pi/2, 1*UNIT_PREFIX["centi"]),
            CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi, -1*UNIT_PREFIX["centi"]),
        ]

        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        # reset hydrophone positions
        cfg.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(3*UNIT_PREFIX["centi"], -np.pi/2, 0),
            CylindricalPosition(3*UNIT_PREFIX["centi"], 0, 0),
            CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi/2, 0),
            CylindricalPosition(3*UNIT_PREFIX["centi"], np.pi, 0),
        ]

    #####################################################
    # Pinger Guess Position Variation Only
    #####################################################

    if (vary_guess):
        change_var = ChangingVariable.PingerGuess
        visualize_NLS_data(PolarPosition(15, 180/CONV_2_DEG), 1, n_iter, change_var)
        visualize_NLS_data(PolarPosition(0, 0/CONV_2_DEG), 1, n_iter, change_var)
        visualize_NLS_data(PolarPosition(16, np.pi/5 + 5/CONV_2_DEG), 1, n_iter, change_var)
        visualize_NLS_data(PolarPosition(40, 30/CONV_2_DEG), 1, n_iter, change_var)

    #####################################################
    # Pinger True Position Variation Only
    #####################################################

    if (vary_pinger):
        change_var = ChangingVariable.PingerPosition

        cfg.pinger_position = CylindricalPosition(15, np.pi/4, 0)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)
            
        cfg.pinger_position = CylindricalPosition(15, np.pi/4, 1)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.pinger_position = CylindricalPosition(15, np.pi/4, 5)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.pinger_position = CylindricalPosition(15, np.pi/4, -10)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.pinger_position = CylindricalPosition(5, -np.pi/2, 10)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

        cfg.pinger_position = CylindricalPosition(40, np.pi/2, 10)
        visualize_NLS_data(PolarPosition(30, 180/CONV_2_DEG), 1, n_iter, change_var)

    plt.show()