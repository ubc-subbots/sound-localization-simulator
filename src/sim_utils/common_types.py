from enum import Enum
from collections import namedtuple
import numpy as np

##################################################################
# Configuration Enums
##################################################################
class QuantizationType(Enum):
    '''
    enum used to specifty quanitzation method for ADC
    '''
    midrise = 0
    midtread = 1

class OptimizationType(Enum):
    '''
    enum used to specify optimization method for NLS_position_calc component
    '''
    nelder_mead = 0
    gradient_descent = 1
    newton_gauss = 2
    angle_nls = 3

class InputType(Enum):
    '''
    enum used to specify input type
    '''
    csv = 1
    shared_memory = 2
    simulation = 3
    socket = 4

##################################################################
# Position Constructs
##################################################################

CylindricalPosition = namedtuple('CylindricalPosition', 'r phi z')
CartesianPosition = namedtuple('CartesianPosition', 'x y z')
PolarPosition = namedtuple('PolarPosition', 'r phi')
Cartesian2DPosition = namedtuple('Cartesian2DPosition', 'x y')

def cyl_to_cart(cyl_pos):
    return CartesianPosition(
        cyl_pos.r*np.cos(cyl_pos.phi), 
        cyl_pos.r*np.sin(cyl_pos.phi), 
        cyl_pos.z
    )

def cart_to_cyl(cart_pos):
    return CylindricalPosition(
        np.sqrt(cart_pos.x**2 + cart_pos.y**2), 
        np.arctan2(cart_pos.y, cart_pos.x), 
        cart_pos.z
    )

def polar_to_cart2d(pol_pos):
    return Cartesian2DPosition(
        pol_pos.r*np.cos(pol_pos.phi), 
        pol_pos.r*np.sin(pol_pos.phi)
    )

def cart2d_to_polar(cart2d_pos):
    return PolarPosition(
        np.sqrt(cart2d_pos.x**2 + cart2d_pos.y**2), 
        np.arctan2(cart2d_pos.y, cart2d_pos.x)
    )

def distance_3Dpoints(location1, location2):
    if type(location1).__name__ == "CylindricalPosition":
        location1 = cyl_to_cart(location1)
    if type(location2).__name__ == "CylindricalPosition":
        location2 = cyl_to_cart(location2)
    
    return ((location1.x - location2.x) ** 2 
          + (location1.y - location2.y) ** 2
          + (location1.z - location2.z) ** 2) ** (1/2)

##################################################################
# Unit Conversions
##################################################################

DISTANCE_CONV = {
    "feet": 0.3048,
    "ft": 0.3048,
    "inch": 2.54e-2,
    "in": 2.54e-2
}

UNIT_PREFIX = {
    "f"     : 1e-15,
    "femto" : 1e-15,
    "p"     : 1e-12,
    "pico"  : 1e-12,
    "n"     : 1e-9,
    "nano"  : 1e-9,
    "u"     : 1e-6,
    "micro" : 1e-6,
    "m"     : 1e-3,
    "milli" : 1e-3,
    "c"     : 1e-2,
    "centi" : 1e-2,
    "k"     : 1e3,
    "killo" : 1e3,
    "M"     : 1e6,
    "mega"  : 1e6,
    "G"     : 1e9,
    "giga"  : 1e9,
    "T"     : 1e12,
    "tera"  : 1e12
}

CONV_2_DEG = 180/np.pi