from components.tdoa.cross_correlation import CrossCorrelation
import matplotlib.pyplot as plt
from simulator_main import sim_config as cfg
import numpy as np

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

    plt.figure()
    plt.plot(y1)
    plt.plot(y2)
    cc = CrossCorrelation({"id" : "Cross Correlation"})
    delay = cc.apply((y1, y2))

    print("calculated delay", delay)
    print("actual delay", n_delay/sample_rate)

if __name__ == '__main__':
    test_lag_finder()
    plt.show()