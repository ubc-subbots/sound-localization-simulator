from simulator_main import sim_config as cfg
import numpy as np

class GaussianNoise:
    '''
    adds gaussian noise at the configured mean and standard deviation
    '''
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def apply(self, sim_signal):
        noisy_sigs = tuple(
            sig + np.random.normal(self.mu, self.sigma, sig.shape)
            for sig in sim_signal
        )

        return noisy_sigs

    def write_frame(self, frame):
        pass