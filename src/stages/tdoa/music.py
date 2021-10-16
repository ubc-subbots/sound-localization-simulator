import global_vars
import numpy as np
import numpy.linalg as la
from numpy.fft import fft
import logging
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

def get_autocorrelation_matrix(sig_array):
        # convert to numpy array
        y = np.array(sig_array)
        rows = y.shape[0]
        
        # loop through signal array and perform the matrix multiplication
        # and expectation opertaion for the autocorrelation of the vector
        # contatining all hydrophone signals.
        # initialize array of complex numbers to avoid casting
        r_yy = np.ones((rows, rows))*(1+1j)
        for i in range(rows):
            for j in range(rows):
                r_yy[i,j] = np.mean(y[i]*np.conj(y[j]))

        return r_yy

def generate_delay_vector(tau, size, frequency):
    omega = 2*np.pi*frequency
    return np.array([np.e**(1j*omega*i*tau) for i in range(size)])

def calculate_music_coefficient(b_vectors, delay_vector):
    # vector inner products
    product_vector = [np.conj(b) @ delay_vector.T for b in b_vectors]

    # sum of squared inner product magnitudes
    vector_sum = sum(np.abs(product_vector)**2)

    return 1/vector_sum


class MUSIC:

    def __init__(self, initial_angle_guess=np.pi/2):
        # TODO: first ensure that the hydrophones geometry is compatible

        self.initial_angle_guess = initial_angle_guess

    def apply(self, sim_signal):
        # take FFT of each signal
        y_fft = np.array([
            fft(sig) for sig in sim_signal 
        ])

        # get autocorrelation matrix of frequency domain vector
        r_yy = get_autocorrelation_matrix(y_fft)

    def write_frame(self, frame):
        pass
