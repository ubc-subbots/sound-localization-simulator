# have bellhop.exe in your PATH variable
# pip install arlpy
# import arlpy

import arlpy.uwapm as pm
import arlpy
import arlpy.plot as plt
import numpy as np

bottom_absorption = 0 # for max reflection
bottom_density = 1600 # default value
bottom_roughness = 0 # for max reflection
bottom_soundspeed = 1500
pool_depth = 11.58 # m
frequency = 40000
max_angle = 80
min_angle = -80
nbeams = 0
rx_depth = 5
rx_range = 10 # distance from tx
soundspeed = bottom_soundspeed
#pool_depth = np.array([[d,-1/19*d**2+0.3048*38] for d in np.linspace(0,rx_range,100)])
surface = np.array([[r, 0.5+0.2*np.sin(2*np.pi*2*r)] for r in np.linspace(0,rx_range,1000)])
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
#pm.print_env(env)

#pm.plot_env(env, width=900)
rays = pm.compute_eigenrays(env)
#pm.plot_rays(rays, env=env, width=900)

arrivals = pm.compute_arrivals(env)
print(arrivals.keys())
#pm.plot_arrivals(arrivals, width=900)