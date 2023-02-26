from components.chain import Chain
import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition, CylindricalPosition
#import my new path generator
from path_generator import path_generator


from stages.input.input_generation_stage import InputGenerationStage
from stages.noise.gaussian_noise import GaussianNoise
from stages.sampling.ideal_adc_stage import IdealADCStage
from stages.sampling.threshold_capture_trigger import ThresholdCaptureTrigger
from stages.tdoa_calc.cross_correlation_stage import CrossCorrelationStage
from stages.localization.multilateration.nls import NLSPositionCalc
from sim_utils import plt_utils
from matplotlib.pyplot import show
from sim_utils.output_utils import initialize_logger

from experiment import Experiment

class NewExp(Experiment):
    results = None
    frames = None

    # Create simulation chain
    def __init__(self):
        self.logger = initialize_logger(__name__)
        self.results = []  # Position list

        # Modify global constants
        global_vars.hydrophone_positions = [
            CylindricalPosition(0, 0, 0),
            CylindricalPosition(1.85e-2, 0, 0),
            CylindricalPosition(1.85e-2, np.pi, 0),
            CylindricalPosition(1.2e-2, -np.pi/10, 1.2e-2),
            CylindricalPosition(1.2e-2, -np.pi+np.pi/10, 1.2e-2),

           ]

        global_vars.pinger_position = CylindricalPosition(10, 0, 10)

        # create initial simulation signal
        global_vars.initial_guess=PolarPosition(3, 1)
        sim_signal = None
        
        self.simulation_chain = Chain(sim_signal)

        self.simulation_chain.add_component(
            InputGenerationStage(measurement_period=2, duty_cycle=0.05)
        )

        #self.sigma = 0.01
        self.sigma=0.01
        self.simulation_chain.add_component(
            GaussianNoise(mu=0, sigma=self.sigma)
        )

        self.simulation_chain.add_component(
            IdealADCStage(num_bits=12, quantization_method=QuantizationType.midtread)
        )

        num_samples = int(
            10 * (global_vars.sampling_frequency / global_vars.signal_frequency))  # sample 10 cycles of the wave
        threshold = 0.05 * (2 ** 11)
        self.simulation_chain.add_component(
            ThresholdCaptureTrigger(num_samples=num_samples, threshold=threshold)
        )

        self.simulation_chain.add_component(
            CrossCorrelationStage()
        )

 
        self.initial_guess = global_vars.initial_guess
        self.simulation_chain.add_component(
            #NLSPositionCalc(optimization_type=OptimizationType.nelder_mead)
 #options for the enum OptimizationType.<nelder_mead, gradient_descent, newton_gauss>
        NLSPositionCalc(optimization_type=OptimizationType.gradient_descent)
            )














        #bingo
        '''
    pinger_rs = np.zeros(100)
    pinger_phis=np.zeros(100)
    pinger_zs=np.zeros(100)
    
    
    for i in range(10):
        print(CylindricalPosition(r=i,phi=2,z=10))
       #python arrays are wack, lets use 3 float arrays with their indicies represneting r, phi and z respectivley

    for i in range(20):
        pinger_rs[i] = i/2+4
        pinger_phis[i]=2
        pinger_zs[i]=10
    
    for i in range(20):
        print(pinger_rs[i])
     
    for i in range(10):
        print(moving_positions[i+2])

        '''


        






        global_vars.pinger_position = CylindricalPosition(10, 0, 10)

        # create initial positoin guess, it our pinger starts off at 4,2,10 so lets do 3, 1, 10
        #we will start off relativley close to our pinger 
        global_vars.initial_guess=PolarPosition(3.8, 1.6)
        #self.initial_guess=PolarPosition(3,1)
    # Execute here
    def apply(self):
        self.results = []

        #this is to test path generator code
        #my_array=path_generator.path_generator_func(path_generator.helix,20,0,1)
        #print("my array is")
        #print(my_array)

        #define our path here, hopefully it causes no errors
        pinger_rs = np.zeros(100)
        pinger_phis=np.zeros(100)
        pinger_zs=np.zeros(100)
        for i in range(20):
            #pinger will only move by half a meter per step and we will see if we can get a qucik runnign gradient
            #descent to track it across short distances
            pinger_rs[i] = i/2+4
            pinger_phis[i]=2
            pinger_zs[i]=10
        for i in range(global_vars.num_iterations):
            #wanna reupdate the value of pinger position with each new index since it is just indexing with i
            global_vars.pinger_position=CylindricalPosition(pinger_rs[i],pinger_phis[i],pinger_zs[i])
            print("at index")
            print(i)
            print("initial guess is at")
            print(global_vars.initial_guess)
            print("pinger is at")
            print(global_vars.pinger_position)


            self.results.append(self.simulation_chain.apply()) # the yellow rectangles could be here because we do these multiple itme sin the graph, seemlilgly once for each iteratoin
            self.frames = self.simulation_chain.frames
            #we need to update the new initial value as the found estimate
            #print(self.results[i])
            
            global_vars.initial_guess=PolarPosition(self.results[i].r,self.results[i].phi)   
            self.initial_guess=global_vars.initial_guess
        #print(self.results)
        return self.results

    def display_results(self):
        if self.results:
            plt_utils.plot_calculated_positions(self.results, self.initial_guess, self.sigma)
            show()
        else:
            self.logger.warn("Run the experiment before displaying results.")


if __name__ == '__main__':
    experiment = new_exp()
    exp_results = experiment.apply()
    experiment.display_results()
