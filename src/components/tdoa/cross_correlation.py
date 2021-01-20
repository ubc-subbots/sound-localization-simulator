import matplotlib.pyplot as plt
from scipy.signal import correlate
import numpy as np
from simulator_main import sim_config as cfg

class CrossCorrelation:
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def apply(self, sim_signal):
        # compute cross correlation
        h0_sig, h_sig = sim_signal
        cross_correlation = correlate(h0_sig, h_sig, mode='same')
        
        # find discrete signal frequency
        f = cfg.signal_frequency / cfg.sampling_frequency
        # find number of samples per signal period
        N = int(np.ceil(1/f))
        # constrain region of interest based on signal periodicity
        # note that the correlation distribution is centered at n=0
        center_idx = int(len(cross_correlation)/2)
        halfrange = int(N/2)
        roi = cross_correlation[center_idx-halfrange:center_idx+halfrange]

        maxima_idx = np.argmax(roi) - halfrange

        n = np.linspace(-len(h0_sig)/2, len(h0_sig)/2, len(h0_sig))
        plt.figure()
        plt.plot(n, cross_correlation)
        plt.plot(n[center_idx-halfrange:center_idx+halfrange] ,roi)
        plt.title(self.id)

        return maxima_idx / cfg.sampling_frequency

    def write_frame(self, frame):
        return {}

def test_lag_finder(): 
    # Sine sample with some noise and copy to y1 and y2 with a 1-second lag
    sample_rate = cfg.sampling_frequency
    signal_frequency = cfg.signal_frequency
    f = signal_frequency / sample_rate
    print(f)
    n = np.linspace(0, round(5/f), int(round(5/f)))
    y = np.sin(f*n)
    y += np.random.normal(0, 0.5, y.shape)
    y1 = y[0:int(3/f)]
    n_delay = int(0.5/f)
    y2 = y[n_delay:int(3/f) + n_delay]

    #plt.plot(y1)
    #plt.plot(y2)
    cc = CrossCorrelation({"id" : "Cross Correlation"})
    delay = cc.apply((y1, y2))

    print("calculated delay", delay)
    print("actual delay", n_delay/sample_rate)

if __name__ == '__main__':
    test_lag_finder()
    plt.show()