'''
USUSLS Simulator
Main parser script to create instances of objects found in the configuration file.
Uses dynamic importing from sim_classes to instantiate.
Author: Michael Ko
'''

import importlib
import sim_config as config
import components_base
import sys
import imp

componentList = []

for component in config.test_config:
    dataFile = components_base.database[component["Component_name"]]
    fileSource = imp.load_source(dataFile[0], dataFile[1])
    class_ = getattr(fileSource, component["Component_name"])
    instance = class_(component)
    componentList.append(instance)

print(componentList)