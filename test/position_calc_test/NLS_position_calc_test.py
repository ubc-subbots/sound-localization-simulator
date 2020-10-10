from components.position_calc.NLS_position_calc import NLS_position_calc
from components.position_calc import position_calc_utils
from simulator_main import sim_config as cfg
from sim_utils.common_types import *
import numpy as np
from scipy.optimize import minimize

# set global configuration
cfg.speed_of_sound = 1500 #m/s
cfg.hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(1e-2, -np.pi/2, 1e-2),
    CylindricalPosition(1e-2, 0, 0),
    CylindricalPosition(1e-2, np.pi/2, 0),
    CylindricalPosition(1e-2, np.pi, 2e-2),
]
cfg.pinger_position = CylindricalPosition(15, np.pi/5, 5)
pinger_guess = PolarPosition(20, np.pi/10)

true_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([cfg.pinger_position.r, cfg.pinger_position.phi]), hydrophone_position, False)
                for hydrophone_position in cfg.hydrophone_positions[1:])

#####################################################
# Cylindrical Coordinates
#####################################################

# Nelder Mead
####################

# set component specific configurations
initial_guess = pinger_guess
opt_type = OptimizationType.nelder_mead
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess)


predicted_position = component.apply(true_tdoa)
print()
print("===============================================")
print("Results: Nelder Mead in Cylindrical")
print("===============================================")
print("actual pinger position: ", cfg.pinger_position)
print("initial guess: ", initial_guess)
print("TDOA data (no noise)", true_tdoa)
print("predicted_position (no noise): ", predicted_position)
print()

# Gardient Descent
####################

# set component specific configurations
opt_type = OptimizationType.gradient_descent
initial_guess = pinger_guess
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess)

predicted_position = component.apply(true_tdoa)

print()
print("===============================================")
print("Results: Gradient Descent in Cylindrical")
print("===============================================")
print("actual pinger position: ", cfg.pinger_position)
print("initial guess: ", initial_guess)
print("TDOA data (no noise)", true_tdoa)
print("predicted_position (no noise): ", predicted_position)
print()

#####################################################
# Cartesian Coordinates
#####################################################

# Nelder Mead
####################

# set component specific configurations
opt_type = OptimizationType.nelder_mead
initial_guess = pol_2_cart2d(pinger_guess)
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess, is_polar=False)

predicted_position = component.apply(true_tdoa)
print()
print("===============================================")
print("Results: Nelder Mead in Cartesian")
print("===============================================")
print("actual pinger position: ", cyl_2_cart(cfg.pinger_position))
print("initial guess: ", initial_guess)
print("TDOA data (no noise)", true_tdoa)
print("predicted_position (no noise): ", predicted_position)
print()

# Gardient Descent
####################

# set component specific configurations
opt_type = OptimizationType.gradient_descent
initial_guess = pol_2_cart2d(pinger_guess)
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess, is_polar=False)

predicted_position = component.apply(true_tdoa)

print()
print("===============================================")
print("Results: Gradient Descent in Cartesian")
print("===============================================")
print("actual pinger position: ", cyl_2_cart(cfg.pinger_position))
print("initial guess: ", initial_guess)
print("TDOA data (no noise)", true_tdoa)
print("predicted_position (no noise): ", predicted_position)
print()