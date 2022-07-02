from sim_utils.input_generation import InputGeneration
import global_vars
import numpy as np


class InputFileImportStage:

    def __init__(self, data_path):
        """
        @param data_path    The path to the 2d ndarray .npy file containing the sampled hydrophone signals
        """
        # as many channels as there are hydrophones
        self.num_components = len(global_vars.hydrophone_positions)

        self.data = np.load(data_path)

        assert self.num_components in self.data.shape

    def apply(self, sim_signal):
        """
        @param sim_signal    Nothing, for compatibility
        @return              A tuple of arrays containing the signal for each hydrophone
        """
        return tuple(arr for arr in self.data)

    def write_frame(self, frame):
        pass