'''
USUSLS Simulator
Main parser script to create instances of objects found in the configuration file.
Uses dynamic importing from sim_classes to instantiate.
Author: Michael Ko
'''

import importlib
from sim_utils import components_base

def config_parser(sim_config_file):
    # Instantiate a list to store all objects.
    componentList = []
    # Main loop for instantiating objects - will loop through all input file components.
    for component in sim_config_file:
        # Extract component name used to identify path file.
        dataFile = components_base.database[component["Component_name"]]
        # Match component class file path with name.
        fileSource = importlib.import_module(dataFile)
        # Instantiate object and populate relevant parameters.
        class_ = getattr(fileSource, component["Component_name"])
        instance = class_(component)
        # Append to list of objects.
        componentList.append(instance)

    # Check output of parser.
    print(componentList)
    return componentList