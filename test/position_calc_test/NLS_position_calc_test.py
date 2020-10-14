from components.position_calc.NLS_position_calc import NLS_position_calc, get_squared_error_sum
from components.position_calc import position_calc_utils
from simulator_main import sim_config as cfg
from sim_utils.common_types import *
import numpy as np
from scipy.optimize import minimize

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
pinger_guess = PolarPosition(5, np.pi)

true_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([cfg.pinger_position.r, cfg.pinger_position.phi]), hydrophone_position, True)
                for hydrophone_position in cfg.hydrophone_positions[1:])

noise = [np.random.normal(0, 1*TIME_CONV['us']) for i in range(len(true_tdoa))]

tdoa_noisy = [
    tdoa+noise_val 
    for tdoa,noise_val in zip(true_tdoa, noise)
]

#####################################################
# Cylindrical Coordinates
#####################################################

# Nelder Mead
####################
print()
print("===============================================")
print("Results: Nelder Mead in Cylindrical")
print("===============================================")

# set component specific configurations
initial_guess = pinger_guess
opt_type = OptimizationType.nelder_mead
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess)

print()
print("Pinger Parameters")
print("=================")
print("actual pinger position: ", cfg.pinger_position)
print("initial guess: ", initial_guess)
print()

predicted_position = component.apply(true_tdoa)

predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([predicted_position.r, predicted_position.phi]), hydrophone_position, True)
                for hydrophone_position in cfg.hydrophone_positions[1:])
                
print("No Noise Run")
print("=================")
print("TDOA data: ", true_tdoa)
print("predicted position: ", predicted_position)
print("predicted TDOA: ", predicted_tdoa)
print()

predicted_position = component.apply(tdoa_noisy)

predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([predicted_position.r, predicted_position.phi]), hydrophone_position, True)
                for hydrophone_position in cfg.hydrophone_positions[1:])
                
print("Noisey Run")
print("=================")
print("Noise Values (us): ", [noise_val/TIME_CONV['us'] for noise_val in noise])
print("TDOA data: ", tdoa_noisy)
print("predicted position: ", predicted_position)
print("predicted TDOA: ", predicted_tdoa)
print()

# # Gardient Descent
# ####################
# print()
# print("===============================================")
# print("Results: Gradient Descent in Cylindrical")
# print("===============================================")

# # set component specific configurations
# opt_type = OptimizationType.gradient_descent
# initial_guess = pinger_guess
# component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess)

# predicted_position = component.apply(true_tdoa)

# predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
#                 np.array([predicted_position.r, predicted_position.phi]), hydrophone_position, True)
#                 for hydrophone_position in cfg.hydrophone_positions[1:])
# print("actual pinger position: ", cfg.pinger_position)
# print("initial guess: ", initial_guess)
# print("TDOA data (no noise)", true_tdoa)
# print("predicted position (no noise): ", predicted_position)
# print("predicted TDOA: ", predicted_tdoa)
# print()

#####################################################
# Cartesian Coordinates
#####################################################

# Nelder Mead
####################
print()
print("===============================================")
print("Results: Nelder Mead in Cartesian")
print("===============================================")

# set component specific configurations
opt_type = OptimizationType.nelder_mead
initial_guess = pol_2_cart2d(pinger_guess)
component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess, is_polar=False)

print()
print("Pinger Parameters")
print("=================")
print("actual pinger position: ", cyl_2_cart(cfg.pinger_position))
print("initial guess: ", initial_guess)
print()

predicted_position = component.apply(true_tdoa)

predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([predicted_position.x, predicted_position.y]), hydrophone_position, False)
                for hydrophone_position in cfg.hydrophone_positions[1:])
                
print("No Noise Run")
print("=================")
print("TDOA data: ", true_tdoa)
print("predicted position: ", predicted_position)
print("predicted TDOA: ", predicted_tdoa)
print()

predicted_position = component.apply(tdoa_noisy)

predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
                np.array([predicted_position.x, predicted_position.y]), hydrophone_position, False)
                for hydrophone_position in cfg.hydrophone_positions[1:])
                
print("Noisey Run")
print("=================")
print("Noise Values (us): ", [noise_val/TIME_CONV['us'] for noise_val in noise])
print("TDOA data: ", tdoa_noisy)
print("predicted position: ", predicted_position)
print("predicted TDOA: ", predicted_tdoa)
print()

# # Gardient Descent
# ####################
# print()
# print("===============================================")
# print("Results: Gradient Descent in Cartesian")
# print("===============================================")

# # set component specific configurations
# opt_type = OptimizationType.gradient_descent
# initial_guess = pol_2_cart2d(pinger_guess)
# component = NLS_position_calc(optimization_type=opt_type, initial_guess=initial_guess, is_polar=False)

# predicted_position = component.apply(true_tdoa)

# predicted_tdoa = tuple(position_calc_utils.tdoa_function_3D(
#                 np.array([predicted_position.x, predicted_position.y]), hydrophone_position, False)
#                 for hydrophone_position in cfg.hydrophone_positions[1:])
# print("actual pinger position: ", cyl_2_cart(cfg.pinger_position))
# print("initial guess: ", initial_guess)
# print("TDOA data (no noise)", true_tdoa)
# print("predicted position (no noise): ", predicted_position)
# print("predicted TDOA: ", predicted_tdoa)
# print()
