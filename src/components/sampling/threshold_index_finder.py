import global_vars

class ThresholdIndexFinder:
    '''
    Finds the index at which the signal first crosses a certain threshold
    '''

    def __init__(self, num_samples, threshold):
        self.num_samples = num_samples
        self.threshold = threshold

    def apply(self, sim_signal):
        for i in range(len(sim_signal)):
            if sim_signal[i] > self.threshold:
                return i

    def write_frame(self, frame):
        return frame
