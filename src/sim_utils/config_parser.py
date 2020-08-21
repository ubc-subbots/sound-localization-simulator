'''
USUSLS Simulator
Main parser script to create instances of objects found in the configuration file.
Uses dynamic importing from sim_classes to instantiate.
Author: Michael Ko
'''

import importlib
import sim_config as config
import components_base

componentList = []
module = importlib.import_module("components_base")

for component in config.test_config:
    class_ = getattr(module, component["Component_name"])
    instance = class_(component)
    componentList.append(instance)

print(componentList)