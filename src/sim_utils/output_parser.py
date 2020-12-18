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
