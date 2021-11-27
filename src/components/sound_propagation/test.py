# have bellhop.exe in your PATH variable
# pip install arlpy
# import arlpy

import arlpy.uwapm as pm
import arlpy
import arlpy.plot as plt
import global_vars
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as pyplot
from datetime import datetime

bottom_absorption = 0 # for max reflection
bottom_density = 1600 # default value
bottom_roughness = 0 # for max reflection
bottom_soundspeed = 1500
pool_depth = 11.58 # m
frequency = 50
max_angle = 80
min_angle = -80
nbeams = 0
rx_depth = 5
rx_range = 10 # distance from tx
soundspeed = bottom_soundspeed
#pool_depth = np.array([[d,-1/19*d**2+0.3048*38] for d in np.linspace(0,rx_range,100)])
#surface = np.array([[r, 0.5+0.2*np.sin(2*np.pi*2*r)] for r in np.linspace(0,rx_range,1000)])
surface = np.array([[r, 0.5+0.2*np.sin(2*np.pi*r)] for r in np.linspace(0,rx_range,100)])
tx_depth = 5 # depth of pinger


env = pm.create_env2d(
    bottom_absorption = bottom_absorption,
    bottom_density = bottom_density,
    bottom_roughness = bottom_roughness,
    bottom_soundspeed = bottom_soundspeed,
    depth = pool_depth,
    frequency = frequency,
    max_angle = max_angle,
    min_angle = min_angle,
    nbeams = nbeams,
    rx_depth = rx_depth,
    rx_range = rx_range,
    soundspeed = soundspeed,
    surface = None,
    tx_depth = tx_depth
)

#pm.plot_env(env, width=900)
rays = pm.compute_eigenrays(env)
pm.plot_rays(rays, env=env, width=900)

arrivals = pm.compute_arrivals(env)
ir = pm.arrivals_to_impulse_response(arrivals, fs=5000, abs_time = True)
impulse_response = np.abs(ir)
pyplot.figure()
pyplot.plot(impulse_response)
pyplot.title("impulse response")

I_1m = 10**(global_vars.pinger_intensity/20)*1 # units in uPa
I_0m = I_1m/math.exp(-global_vars.attenuation_coeff)
dt = 1/5000
n_points = 1/dt
pressure_wave = np.zeros(int(n_points)) # pressure wave output from the pinger

for i in range(len(pressure_wave)):
    pressure_wave[i] =I_0m* math.sin(2*math.pi*50*(dt*i))
pyplot.figure()
pyplot.plot(pressure_wave)
pyplot.title("original pressure wave")

conv = np.convolve(impulse_response,pressure_wave)
pyplot.figure()
pyplot.plot(conv)
pyplot.title("convolution with impulse response")

def free_field_voltave_sensitivity(frequency, randomize_FFVS):
    FFVS = None
    if (randomize_FFVS):
        FFVS = np.random.randint(-208,-211)
    else:      
        if (frequency <= 30e3):
            FFVS = -208
        else:
            FFVS = -211
    return FFVS

def hydrophone_response(FFVS,pressure):
    output = 10**(FFVS/20)*pressure
    return output

FFVS = free_field_voltave_sensitivity(global_vars.signal_frequency, 0)
hydrophone_response_output = hydrophone_response(FFVS, conv)

pyplot.figure()
pyplot.plot(hydrophone_response_output)
pyplot.title("hydrophone voltage response")
pyplot.show()