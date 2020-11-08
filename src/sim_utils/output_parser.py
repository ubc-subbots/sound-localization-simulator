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

# Initialize sample dictionary files to test with.
# Suggest that for our simulation, we pass a python file containing a dictionary 
# of all simulation frame results to store our data with.
dictTest = {
    "id" : "Frame 1",
    "positions" : {"name" : "position_test_1", "pinger_acutal" : [1.0, 2.0, -1.0], "pinger_calculated" : [5.0, 5.0, -5.0], "hydrophone_1" : [1.0, 1.0, 1.0], "hydrophone_2" : [1.0, 2.0, 3.0]},
    "noise" : {"noise_value_1" : 3.0, "noise_tolerance_1" : 0.1},
    "uncertainty" : {"name" : "bessel_filter", "R1_error" : 0.1, "C1_error" : 0.05, "phase_delay" : 0.2, "center_freq" : 1000.0}
}

output_test_nested = [
    {
        "id" : "Frame 1",
        "positions" : {"name" : "position_test_1", "pinger_acutal" : [5.0, 2.0, -5.0], "pinger_calculated" : [7.0, 8.0, -10.0], "hydrophone_1" : [-1.0, 11.0, 14.0], "hydrophone_2" : [-1.0, 7.0, 1.0]},
        "noise" : {"noise_value_1" : 9.0, "noise_tolerance_1" : 0.01},
        "uncertainty" : {"name" : "bessel_filter", "R1_error" : 1.1, "C1_error" : 0.03, "phase_delay" : 0.1, "center_freq" : 50000.0}
    },

    {
        "id" : "Frame 2",
        "positions" : {"name" : "position_test_1", "pinger_acutal" : [10.0, 20.0, -10.0], "pinger_calculated" : [50.0, 50.0, -50.0], "hydrophone_1" : [10.0, 10.0, 10.0], "hydrophone_2" : [18.0, 22.0, 31.0]},
        "noise" : {"noise_value_1" : 3.7, "noise_tolerance_1" : 0.15},
        "uncertainty" : {"name" : "bessel_filter", "R1_error" : 3.1, "C1_error" : 1.05, "phase_delay" : 0.2, "center_freq" : 100.0}
    },

    {
        "id" : "Frame 3",
        "positions" : {"name" : "position_test_1", "pinger_acutal" : [1.0, 2.0, -1.0], "pinger_calculated" : [5.0, 5.0, -5.0], "hydrophone_1" : [1.0, 1.0, 1.0], "hydrophone_2" : [1.0, 2.0, 3.0]},
        "noise" : {"noise_value_1" : 3.0, "noise_tolerance_1" : 0.1},
        "uncertainty" : {"name" : "bessel_filter", "R1_error" : 0.1, "C1_error" : 0.05, "phase_delay" : 0.2, "center_freq" : 1000.0}
    },
]

def create_output_file(frame_data, pickle_path, xml_path):
    # Save dictionary to pickle file which will be passed through simulation.
    with open(pickle_path, 'wb') as fp:
        pickle.dump(frame_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

    # Format dictionary to "pretty" XML format.
    xml = dicttoxml.dicttoxml(frame_data)
    dom = parseString(xml)
    # Write to output XML file.
    outputFile = open(xml_path, "w+")
    outputFile.write(dom.toprettyxml())
