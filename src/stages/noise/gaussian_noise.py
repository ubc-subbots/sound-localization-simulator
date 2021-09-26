import global_vars
import numpy as np
from stages.stage import Stage

class GaussianNoise(Stage):
    '''
    adds gaussian noise at the configured mean and standard deviation
    '''
    def __init__(self, mu, sigma):
        super().__init__()
        self.mu = mu
        self.sigma = sigma

    def apply(self, sim_signal):
        self.signal = tuple(
            sig + np.random.normal(self.mu, self.sigma, sig.shape)
            for sig in sim_signal
        )

        return self.signal