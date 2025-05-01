#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-----------------------------------------------------------
Script Name: <mechanical_params.py>
Description: <This script provides published parametrizations of mechanical 
parameters on density. Partly they can be scaled to measured data points>
Author: <Bastian Bergfeld>
Email: <bbergfeld@gmx.net>
Date Created: <2025.04.25>
-----------------------------------------------------------
"""

#%% getting elastic wave speeds in snow
import numpy as np

# Theoretical estimates for wave speeds in materials:

def shear_wave_speed(G, rho):
    ''' 
    G = shear modulus slab
    rho = mean slab density
    '''
    return(np.sqrt(G/rho))
    
def long_wave_speed(E, rho):
    return(np.sqrt(E/rho))

def rayleigh_wave_speed(E, G, rho,nu):
    ''' Bergmann approximation
    E = Elastic modulus of slab (Pa)
    G = shear modulus slab  (Pa)
    rho = mean slab density (kg/m3)
    nu = Poisson Ratio of slab
    '''
    x = np.sqrt((0.87 + 1.12*nu)/(1+nu))
    return(x * shear_wave_speed(G,rho,))
    
def youngs_to_pwave_modulus(E,nu):
    return((E*(1-nu))/((1+nu)*(1-2*nu)))