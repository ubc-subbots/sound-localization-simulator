from enum import Enum
from collections import namedtuple
import numpy as np

class OptimizationType(Enum):
    nelder_mead = 0
    gradient_descent = 1
    newton_gauss = 2

CylindricalPosition = namedtuple('CylindricalPosition', 'r phi z')
CartesianPosition = namedtuple('CartesianPosition', 'x y z')
PolarPosition = namedtuple('PolarPosition', 'r phi')
Cartesian2DPosition = namedtuple('Cartesian2DPosition', 'x y')

def cyl_2_cart(cyl_pos):
    return CartesianPosition(
        cyl_pos.r*np.cos(cyl_pos.phi), 
        cyl_pos.r*np.sin(cyl_pos.phi), 
        cyl_pos.z
    )

def cart_2_cyl(cart_pos):
    return CylindricalPosition(
        np.sqrt(cart_pos.x**2 + cart_pos.y**2), 
        np.arctan2(cart_pos.y, cart_pos.x), 
        cart_pos.z
    )

def pol_2_cart2d(pol_pos):
    return Cartesian2DPosition(
        pol_pos.r*np.cos(pol_pos.phi), 
        pol_pos.r*np.sin(pol_pos.phi)
    )

def cart2d_2_pol(cart2d_pos):
    return PolarPosition(
        np.sqrt(cart2d_pos.x**2 + cart2d_pos.y**2), 
        np.arctan2(cart2d_pos.y, cart2d_pos.x)
    )