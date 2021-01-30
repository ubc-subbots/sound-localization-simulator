'''
USUSLS Simulator
Main parser script to structure the output of the simulation.
Author: Michael Ko
'''

# We can simply use dict-to-xml to achieve an output XML format.
# https://pypi.org/project/dicttoxml/

import dicttoxml
from xml.dom.minidom import parseString
import pickle
import logging
from simulator_main import args

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

def initialize_logger(logger_name):
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(args.log_level)

    # create console handler
    console = logging.StreamHandler()
    console.setLevel(args.log_level)
    # create formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s:%(message)s')
    # add formatter to ch
    console.setFormatter(formatter)

    # create new logfile when starting simulator main, append for other modules
    if __name__ == "__main__":
        file_mode = 'w'
    else:
        file_mode = 'a'
    filename= "log/%s.log" % args.config

    # create file handler    
    logfile = logging.FileHandler(filename, mode=file_mode, encoding='utf-8')
    logfile.setLevel(args.log_level)
    # create formatter - add date to log file
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:%(message)s')
    # add formatter to ch
    logfile.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(console)
    logger.addHandler(logfile)

    return logger
