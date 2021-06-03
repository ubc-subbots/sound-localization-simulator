'''
USUSLS Simulator
Main parser script to create instances of objects found in the configuration file.
Uses dynamic importing from sim_classes to instantiate.
Author: Michael Ko
'''

import importlib
from sim_utils import components_base
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

def generate_sim_chain(simulation_chain_dict):
    # Instantiate a list to store all objects.
    sim_chain = []
    # Main loop for instantiating objects - will loop through all input file components.
    for component in simulation_chain_dict:
        # Extract component name used to identify path file.
        dataFile = components_base.database[component["component_name"]]
        # Match component class file path with name.
        fileSource = importlib.import_module(dataFile)
        # Instantiate object and populate relevant parameters.
        class_ = getattr(fileSource, component["component_name"])
        instance = class_(component)
        # Append to list of objects.
        sim_chain.append(instance)

    # Check output of parser.
    logger.info("Simulation chain:")
    for stage in sim_chain:
        logger.info("%s Stage (%s)" %(stage.component_name, stage.id))

    return sim_chain

def generate_frame(sim_config):
    return {}