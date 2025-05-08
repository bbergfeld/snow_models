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

#%% Theoretical estimates of weak layer crack speeds in snow:
from uncertainties import wrap as unc_wrapper
import numpy as np
import pandas as pd

def _solitary_wave_speed(g, E, h, hf, rho):
    ''' Heierli 2005 - Solitary fracture waves in metastable snow stratifications, Journal of Geophysical Research, Equation 7a
    g = gravitational constant
    E = elastic modulus slab
    h = slab thickness
    hf = collapse height
    rho = mean slab density
    s
    return: speed in m/s

    '''
    D = (E*h**3)/12 # flexural rigidity of the slab 
    c4 = (g*D)/(2*hf*rho*h)
    c = np.sqrt(np.sqrt(c4))
    
    return(c)
solitary_wave_speed = unc_wrapper(_solitary_wave_speed)

def _solitary_wave_touchdown(g, E, h, hf, rho):
    ''' Heierli 2005 - Solitary fracture waves in metastable snow stratifications, Journal of Geophysical Research, Equation 7a
    g = gravitational constant
    E = elastic modulus slab
    h = slab thickness
    hf = collapse height
    rho = mean slab density
    
    return: touchdown distance in m
    '''
    gamma = 2.331 # from Heierli
    D = (E*h**3)/12 # flexural rigidity of the slab 
    tdd4 = gamma**4 * (2*hf*D)/(g*rho*h)
    tdd = np.sqrt(np.sqrt(tdd4))

    return(tdd)
solitary_wave_touchdown = unc_wrapper(_solitary_wave_touchdown)

def _mc_clung_fracture_speeds (nu, E, rho):
    ''' Mc Clung 2005 - Approximate estimates of fracture speeds for dry slab avalanches, Geophysical Research letters, Equation 1
    E = elastic modulus slab
    nu =  Poisson ratio (-)
    rho = mean slab density
    '''
    G = E/(2*(1+nu))
    low_c = 0.7*np.sqrt(G/rho)
    high_c = 0.9*np.sqrt(G/rho)
    return(low_c,high_c)
mc_clung_fracture_speeds = unc_wrapper(_mc_clung_fracture_speeds)

def _anticrack_propagation_speed(g, E, nu, h, hf, rho, theta, l, C_initial_guess=0.5):
    ''' Heierli dissertation - Anticrack model for slab avalanche release, Equation 5.17
        the formula is a dispersion relation which links speed ot touchdowndistance
        hf = sollapse height (m)
        rho = slab mean density (kg/m^3)
        h = slab thickness (m)
        theta = slope angle (°)
        nu = poisson Ratio (-)
        E = slab elastic modulus (Pa)
        l = touchdown distance (m)
    returns crack propagation speed in m/s             
    
    --Note: computation is sensitive to the C_initial_guess -- 
    '''
    from scipy import  optimize

    def get_speed_for_td_length(L):  
        func = lambda C : (L**2/C**2)*((eta/(L*C*(1-C**2))) * (1/np.sin(2*C*L/eta)-1/np.tan(2*C*L/eta))-1)- 2*H_f/Sigma
        C_solution = optimize.fsolve(func, C_initial_guess)
        return(C_solution)
            
    #% values as Heierli page 68
    theta = np.radians(theta)
    k = 5/6 # timoshenko beam correction factor for rectengular beam
    G = E/(2*(1+nu)) # shear modulus 
    eta = np.sqrt(E/(3*k*G))
    
    shear_wave_velocity = np.sqrt(k*G/rho)
    longitudinal_wave_velocity = np.sqrt(E/rho)
    #compressive stress
    sigma = -rho*g*h*np.cos(theta) 
    #shear stress
    tau = rho*g*h*np.sin(theta)
    #dimensionless variables  Table 4.1 Heierli diss and Equ. 5.2
    L = l/h
    H_f = hf/h  # collapse amplitude
    Sigma = -sigma/(k*G) # dimensionless compressive stress // Table 4.1 Heierli diss
    Tau = tau/(k*G)# dimensionless compressive stress // Table 4.1 Heierli diss

        
    C = get_speed_for_td_length(L)
    c = C*shear_wave_velocity
    return(c)
anticrack_propagation_speed = unc_wrapper(_anticrack_propagation_speed)
