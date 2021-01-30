import arlpy.uwapm as pm
import arlpy.plot as plt
import numpy as np

print('import done')
#print(pm.models())
print('last line')

env = pm.create_env2d()
pm.print_env(env)
pm.plot_env(env, width=900)
rays = pm.compute_eigenrays(env)
pm.plot_rays(rays, env=env, width=900)