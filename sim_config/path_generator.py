#no clue why these got imported

from lib2to3.pgen2.token import NUMBER
from math import radians
from tkinter import PhotoImage
from components.chain import Chain
import numpy as np
import jsonpickle
import global_vars
from sim_utils.common_types import QuantizationType, OptimizationType, PolarPosition, CylindricalPosition




class path_generator:

    def path_generator_func(func,iterations,start,end):
        '''

    #function to generate a series of inputs

        
    @brief          Generates a series of points to let the algorithim track the pinger

    @param func     A function to generate the points with, returns a numpy array of form [r(t),phi(t),z(t)]
                    HOPEFULLY A CHANGING Z WON'T CAUSE ISSUES

    @param iterations   The number of points to generate on the path
        
    @param start        the starting 'time' parameter value

    @param end          the ending 'time' parameter value

    @return             a numpy array filled with cylyndrical positions along the path
       '''
        
        path_array=np.zeros(iterations)
        #we need to subdivide our interval into time steps
        time_step=(start-end)/iterations

        for i in range(iterations):
            temp=func(start+i*time_step)
            path_array[i]=CylindricalPosition(temp[0],temp[1],temp[2])
            #we must extract the r and phi value from our function into a polar position struct

            #we get this error
                #path_array[i]=CylindricalPosition(temp[0],temp[1],temp[2])
            #ValueError: setting an array element with a sequence.

            # need a data type of an array or tuple filled with these, maybe we should just use a tuple and append
            #or I could output an array of points and make another function to convert them to CylyndricalPosition structs but that would suck
            
            
        return path_array

    def helix(t):
        '''
        @breif          a function to generate a helical path in r phi and z
        @param t        the 'time' parameter

        '''
        output=np.zeros(3)

        radius=2
        #it will snap back to zero once reaching 2pi
        phi=np.pi*2*t%(2*np.pi)
        z=t
        output[0]=radius
        output[1]=phi
        output[2]=z
        
        return output
        

        
           



