import global_vars
import numpy as np
from sim_utils.common_types import CylindricalPosition, PolarPosition, cyl_to_cart, CONV_2_DEG
from numpy.fft import fft
from numpy.linalg import eig
from sim_utils.output_utils import initialize_logger
from sim_utils.plt_utils import plot_signals
import logging
import matplotlib.pyplot as plt

class MUSIC:

    def __init__(self, resolution, plane_wave_propagation = True, 
                 use_depth_sensor=True, visualize_jmusic=False):
        # create logger object for this module
        self.logger = initialize_logger(__name__)
        
        self.plane_wave_propagation = plane_wave_propagation
        self.use_depth_sensor = use_depth_sensor
        self.visualize_jmusic = visualize_jmusic
        
        # error checking
        if resolution > 2*np.pi or resolution < 0:
            self.logger.error("Invalid resolution: %f. "
                         "Resolution must be between 0 and 2pi" % resolution)
        elif resolution > np.pi/10:
            self.logger.warning("Resolution is too coarse and could lead to poor results.")

        self.resolution = resolution

    def apply(self, sim_signal):
        level = self.logger.getEffectiveLevel()
        if level <= logging.DEBUG:
            plot_signals(*sim_signal, title="Input to ADC")        

        # determine model for calculating delays
        if self.plane_wave_propagation:
            delay_func = plane_wave_prop_delay
        else:
            self.logger.error("Only plane wave propagation modelled at the moment.")

        # take FFT of each signal
        y_fft = np.array([
            fft(sig) for sig in sim_signal 
        ])

        # get autocorrelation matrix of frequency domain vector
        r_yy = get_autocorrelation_matrix(y_fft, is_fft=True)

        # eigen analysis on r_yy
        w, v = eig(r_yy)

        # discard vector with largest eigenvalue
        b_vectors = [v[:,i] for i in range(len(v)) if i != np.argmax(w)]

        # loop over parameters
        if self.use_depth_sensor:
            phi_vals = np.arange(start=0, stop=2*np.pi, step=self.resolution)
            steering_vectors = [
                generate_steering_vector(delay_func, phi)
                for phi in phi_vals
            ]
            j_music = [
                calculate_music_coefficient(b_vectors, steering_vector)
                for steering_vector in steering_vectors
            ]

            if self.visualize_jmusic:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='polar')
                ax.plot(phi_vals, j_music)
                plt.xlabel("Polar Angle " + r'$\phi$' + " (degrees)")
                plt.ylabel(r'$J_{MUSIC}$')
                plt.title(r'$J_{MUSIC}$' + " Distribution in " + r'$\phi$')
                plt.show()

            # Return the value of phi that maximizes J_MUSIC
            index = j_music.index(max(j_music))
            return phi_vals[index]
        else:
            self.logger.error("MUSIC not implemented without depth sensor yet.")

    def write_frame(self, frame):
        pass

def get_autocorrelation_matrix(sig_array, is_fft=True):
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
                y_cross = y[i]*np.conj(y[j])
                if is_fft:
                    index = int(len(y_cross) * 
                            global_vars.signal_frequency/global_vars.sampling_frequency)
                    r_yy[i,j] = y_cross[index]
                else:
                    r_yy[i,j] = np.mean(y_cross)

        return r_yy

def plane_wave_prop_delay(sensor_pos, phi, theta=None):
    # convert to numpy array for dot product
    x = np.array(sensor_pos)

    if theta:
        # negative signs indicate propagation is towards sensor
        khat = -np.array([
            np.sin(theta)*np.cos(phi),
            np.sin(theta)*np.sin(phi),
            np.cos(theta)
        ])
    else:
        # negative sign indicates propagation is towards sensor
        khat = -np.array([
            np.cos(phi),
            np.sin(phi),
            global_vars.pinger_position.z
        ])

    return np.dot(khat, x)/global_vars.speed_of_sound

def generate_steering_vector(delay_func, phi, theta=None):
    omega = 2*np.pi*global_vars.signal_frequency
    
    # need the hydrophone positions in cartesian coordinates
    if type(global_vars.hydrophone_positions) == CylindricalPosition:
        h_positions = cyl_to_cart(global_vars.hydrophone_positions)
    else:
        h_positions = global_vars.hydrophone_positions

    # compute delay value at each hydrophone
    tau_vals = [delay_func(hpos, phi, theta) for hpos in h_positions]

    # generate steering vector array from delay values
    return np.array([np.e**(-1j*omega*tau) for tau in tau_vals])

def calculate_music_coefficient(b_vectors, steering_vector):
    # vector inner products
    product_vector = [np.vdot(b, steering_vector) for b in b_vectors]

    # sum of squared inner product magnitudes
    vector_sum = sum(np.abs(product_vector)**2)

    return 1/vector_sum