'''
USUSLS Simulator
Main script to structure the output of the simulation.
Author: Michael Ko, Dvir Hilu
'''

# We can simply use dict-to-xml to achieve an output XML format.
# https://pypi.org/project/dicttoxml/

import dicttoxml
from xml.dom.minidom import parseString
import pickle
import logging
import os

# initialize to None to better detect errors
log_level = None
config = None


def create_output_file(frame_data, pickle_path, xml_path):
    # Save dictionary to pickle file which will be passed through simulation.
    with open(pickle_path, 'wb+') as fp:
        pickle.dump(frame_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

    # Format dictionary to "pretty" XML format.
    xml = dicttoxml.dicttoxml(frame_data)
    dom = parseString(xml)
    # Write to output XML file.
    outputFile = open(xml_path, "w+")
    outputFile.write(dom.toprettyxml())


def configure_logger(log_lvl, cfg):
    global log_level, config
    config = cfg
    log_level = log_lvl


def initialize_logger(logger_name):
    # create new logfile when starting simulator main, append for other modules
    if logger_name == "__main__":
        file_mode = 'w'
        name = "simulator_main"
    else:
        name = logger_name
        file_mode = 'a'

    # check if log directory exists. If not, create it
    if not os.path.exists('log'):
        os.makedirs('log')

    filename = "log/%s.log" % config # TODO: Create the folder if not exists
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # create console handler
    console = logging.StreamHandler()
    console.setLevel(log_level)
    # create formatter
    formatter = logging.Formatter('%(name)s | %(levelname)s: %(message)s')
    # add formatter to ch
    console.setFormatter(formatter)

    # create file handler
    logfile = logging.FileHandler(filename, mode=file_mode, encoding='utf-8')
    logfile.setLevel(log_level)
    # create formatter - add date to log file
    formatter = logging.Formatter('%(asctime)s - %(name)s | %(levelname)s: %(message)s')
    # add formatter to ch
    logfile.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(console)
    logger.addHandler(logfile)

    return logger
