import global_vars
import numpy as np
from stages.localization.localization_utils import plane_wave_prop_delay
from numpy.fft import fft
from numpy.linalg import eig
from sim_utils.output_utils import initialize_logger
from sim_utils.plt_utils import plot_signals
import logging
import matplotlib.pyplot as plt

class MUSIC:

    def __init__(self, resolution, plane_wave_propagation = True, 
                 use_depth_sensor=False, visualize_jmusic=False, 
                 xy_halfplane=True, r_max=50, num_r_cells=100):
        # create logger object for this module
        self.logger = initialize_logger(__name__)
        
        self.plane_wave_propagation = plane_wave_propagation
        # determine model for calculating delays
        if self.plane_wave_propagation:
            self.logger.info("Using plane wave propagation to approximate TOA")
            self.delay_func = plane_wave_prop_delay
        else:
            self.logger.error("Only plane wave propagation modelled at the moment.")
        
        self.use_depth_sensor = use_depth_sensor
        if use_depth_sensor:
            self.logger.info("Initializing MUSIC localization stage with r, phi as parameters")
        else:
            self.logger.info("Initializing MUSIC localization stage with theta, phi as parameters")
        
        self.visualize_jmusic = visualize_jmusic
        if visualize_jmusic:
            self.logger.warn("Setting visualization setting on MUSIC localization stage will lead to hella plots")

        # set search range
        if xy_halfplane:
            self.logger.warn("Constraining the localization to the +y halfplane."
                             " Not able to detect reflective degeneracy!")
        self.max_phi = np.pi if xy_halfplane else 2*np.pi
        self.r_max = r_max
        self.num_r_cells = num_r_cells
        
        # error checking
        if resolution > 2*np.pi or resolution < 0:
            self.logger.error("Invalid resolution: %f. "
                         "Resolution must be between 0 and 2pi" % resolution)
        elif resolution > np.pi/10:
            self.logger.warning("Resolution in phi is too coarse and could lead to poor results.")

        if num_r_cells < 10 and use_depth_sensor:
            self.logger.warning("Resolution in r is too coarse and could lead to poor results")
        elif num_r_cells > 500 and use_depth_sensor:
            self.logger.warning("Resolution in r is too fine and could lead to large computation time")

        if r_max < 1:
            self.logger.error("Invalid radial bound: %f. "
                         "Radial bound must be greater than 1 to satisfy far field assumption" % resolution)

        self.resolution = resolution

    def apply(self, sim_signal):
        level = self.logger.getEffectiveLevel()
        if level <= logging.NOTSET:
            plot_signals(*sim_signal, title="Input to ADC")        

        # take FFT of each signal
        y_fft = np.array([
            fft(sig) for sig in sim_signal 
        ])

        # get autocorrelation matrix of frequency domain vector
        r_yy = self.get_autocorrelation_matrix(y_fft, is_fft=True)

        # eigen analysis on r_yy
        w, v = eig(r_yy)

        # discard vector with largest eigenvalue
        b_vectors = [v[:,i] for i in range(len(v)) if i != np.argmax(w)]

        # generate parameter values to iterate over
        param2_vals = np.arange(0, self.max_phi, self.resolution)
        if self.use_depth_sensor:
            param1_vals = np.linspace(1, self.r_max, self.num_r_cells)
        else:
            param1_vals = np.arange(0, np.pi/2, self.resolution)
            # shift to lower hemisphere if we are above pinger
            if global_vars.pinger_position.z < 0:
                param1_vals += np.pi/2
        
        max_j_music = 0
        max_params = None
        # parameter to j_music dictionary for visualization
        j_music_dict = {}
        for p1 in param1_vals:
            # sub dictionary for visualization
            j_music_sub_dict = {}
            for p2 in param2_vals:
                # get steering vector for the parameter set
                steering_vector = generate_steering_vector(self.delay_func, (p1, p2), 
                                                           self.use_depth_sensor)
                
                # find MUSIC coefficient for parameter set
                j_music = calculate_music_coefficient(b_vectors, steering_vector)
                j_music_sub_dict[p2] = j_music

                # evaluate whether the maximizing parameters should change
                if j_music > max_j_music:
                    self.logger.debug("Updating max JMUSIC to %.2f with params=(%.2f,%.2f)"%(j_music, p1, p2))
                    max_j_music = j_music
                    max_params = (p1, p2)

            # add sub dictionary to main dictionary    
            j_music_dict[p1] = j_music_sub_dict

        if self.visualize_jmusic:
            num_plots = 6
            vis_indices = (np.linspace(0,1,num_plots)*len(param1_vals)).astype(int)
            vis_p1_vals = param1_vals[vis_indices]
            p1_name = "r" if self.use_depth_sensor else r'$\theta$'

            num_fig_rows = int(np.sqrt(num_plots))
            num_fig_cols = int(np.ceil(num_plots/num_fig_rows))
            fig, axs = plt.subplots(num_fig_rows, num_fig_cols, 
                                    projection='polar', figsize=(10,10))
            fig.suptitle(r'$J_{MUSIC}$'+ " Coefficient Visualization")
            axs = axs.flatten()
            
            for p1, ax in zip(vis_p1_vals, axs):
                phi = j_music_dict[p1].keys()
                j_music = j_music_dict[p1].values()
                ax.plot(phi, j_music)
                ax.scatter(global_vars.pinger_position.phi, max(j_music), 
                            label="Actual DOA")
                ax.set_title(r'$J_{MUSIC}$' + " Distribution in " + r'$\phi$' + 
                             "With %s=%.2f" %(p1_name, p1))
                ax.legend()
                
            plt.show()

        # Return the parameter values that maximizes J_MUSIC
        self.logger.info("JMUSIC maximized at a value of %.2f with params=(%.2f, %.2f)"
                         %(max_j_music, max_params[0], max_params[1]))
        
        return max_params
    
    def write_frame(self, frame):
        pass

    def get_autocorrelation_matrix(self, sig_array, is_fft=True):
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
                        #TODO: figure this out!!!!
                        max_index = np.argmax(np.abs(y_cross))
                        expected_index = int(len(y_cross) 
                                         * global_vars.signal_frequency
                                         / global_vars.sampling_frequency)
                        
                        if max_index != expected_index:
                            frequency = (max_index
                                         * global_vars.sampling_frequency
                                         / len(y_cross))
                            exp_frequency = (expected_index
                                             * global_vars.sampling_frequency
                                             / len(y_cross))
                            self.logger.warn("At correlation matrix indices [%d, %d]"
                                             "Expected frequency %.2f but got frequency %.2f"
                                             %(i, j, exp_frequency, frequency))

                        r_yy[i,j] = y_cross[max_index]
                    else:
                        r_yy[i,j] = np.mean(y_cross)

            return r_yy

def generate_steering_vector(delay_func, params, use_depth_sensor):
    omega = 2*np.pi*global_vars.signal_frequency

    # compute delay value at each hydrophone
    tau = np.array([
        delay_func(params, hpos, use_depth_sensor) 
        for hpos in global_vars.hydrophone_positions
    ])

    # generate steering vector array from delay values
    return np.e**(-1j*omega*tau)

def calculate_music_coefficient(b_vectors, steering_vector):
    # vector inner products
    product_vector = [np.vdot(b, steering_vector) for b in b_vectors]

    # sum of squared inner product magnitudes
    vector_sum = sum(np.abs(product_vector)**2)

    return 1/vector_sum