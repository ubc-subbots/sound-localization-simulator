from simulator_main import sim_config as cfg

class ThresholdIndexFinder:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def apply(self, sim_signal):
        for i in range(len(sim_signal)):
            if sim_signal[i] > self.threshold:
                return i

    def write_frame(self, frame):
        return frame        