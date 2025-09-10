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

#%% getting Elastic moduli from densities
import numpy as np
from uncertainties import ufloat

class get_E_from_rho:
    def __init__(self, rho, scaling=None, output_unit="Pa"):
        '''
        Initialize the class with density, scaling, and desired output unit.
        
        Args:
            rho (float): The density (kg/m³).
            scaling (tuple, optional): A tuple of (Elastic modulus measured, density measured).
            output_unit (str, optional): Desired output unit for elastic modulus. Options: "Pa", "kPa", "MPa", "GPa".
        '''
        self.rho = rho
        self.scaling = scaling
        self.output_unit = output_unit

    def scale_output(self, result):
        ''' 
        Scale the result based on the desired output unit.
        
        Args:
            result (float): The raw elastic modulus value in Pa.
        
        Returns:
            float: The scaled elastic modulus.
        '''
        if self.output_unit == "Pa":
            return result  # No scaling needed for Pa
        elif self.output_unit == "kPa":
            return result * 1E-3  # Convert Pa to kPa
        elif self.output_unit == "MPa":
            return result * 1E-6  # Convert Pa to MPa
        elif self.output_unit == "GPa":
            return result * 1E-9  # Convert Pa to GPa
        else:
            print("Invalid output unit. Use 'Pa', 'kPa', 'MPa', or 'GPa'.")
            return None

    def apply_scaling(self, scaling_factor, formula_result):
        '''
        This allows to scale the parametrization to one measured datapoint
        (Elastic modulus measured, density measured). the overall behavior
        of the parametrization (the powerlaw exponent) remains the same.
        
        Args:
            scaling_factor (float): The factor for scaling.
            formula_result (float): The raw result from the formula.
        
        Returns:
            float: The scaled result, or the original result if no scaling is applied.
        '''
        if self.scaling:
            try:
                factor = self.scaling[0] / scaling_factor * self.scaling[1]**scaling_factor
                return factor * formula_result
            except:
                print("Scaling failed")
                return None
        return formula_result

    def e_gerling_2017_AC(self):
        ''' 
        Gerling et al 2017 ( https://doi.org/10.1002/2017GL075110)
        AC based parametrization (Equation 6, first line)
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 6E-10 * self.rho**4.6 * 1E6  # Base formula without scaling
        result = self.apply_scaling(6E-10, result)
        return self.scale_output(result)

    def e_gerling_2017_CT(self):
        ''' 
        Gerling et al 2017 ( https://doi.org/10.1002/2017GL075110)
        CT based parametrization formula (Equation 6, second line)
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 2E-8 * self.rho**3.98 * 1E6  # Base formula without scaling
        result = self.apply_scaling(2E-8, result)
        return self.scale_output(result)

    def e_bergfeld_2022(self):
        ''' 
        Bergfeld et al 2022 (https://doi.org/10.5194/nhess-23-293-2023)
        Equation 4 and Appendix B
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 6.5E3 * (self.rho / 918)**4.4 * 1E6  # Base formula without scaling
        result = self.apply_scaling(6.5E3, result)
        return self.scale_output(result)

    def e_Herwijnen_2016(self):
        ''' 
        Van Herwijnen 2016 (doi:10.1017/jog.2016.90)
        Parametrization based on PTV measured beam bending during sawing phase
        of PST experiments. Heierli and Clapeyron used to model the bending.
        
        Equation 8 and Fig 8.
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 0.93 * self.rho**2.8  # Base formula without scaling
        result = self.apply_scaling(0.93, result)
        return self.scale_output(result)

    def e_scapozza_2004(self):
        ''' 
        Scapozza 2004 (https://www.research-collection.ethz.ch/entities/publication/6996d34d-e46c-418a-adda-2fcccf731fd2) Page 96 formula 5-7
        Parametrization of the Young's Moduls based on a Triaxial testing maschine. Strain rates ranged from 10**-6 to 10**-3 and snow temperatures range: -18.5°C to -1.9°C, snow densities: 180 to 490 kg/m**3
        Korrelationskoeffizient of the fit fits : r2 = 0.928
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 0.1873 * np.exp(0.0149 * self.rho) * 1E6  # Base formula without scaling
        result = self.apply_scaling(0.1873, result)
        return self.scale_output(result)

    def e_sigrist_2006_powerlaw(self):
        ''' 
        Sigrist 2006 (https://www.research-collection.ethz.ch/entities/publication/1c564911-fb9f-4b1a-b3b3-b447e4df33cd) page 76, equation 4.8
        Parametrization of the Young's Moduls on denstiy based on small cylindrical samples with a diameter of 48 mm and a height of 30 mm were loaded and unloaded with a frequency of 100 Hz. The force response F due to the predefined displacement resulted in a strain rate of e = 2 7 10~2s-1 results
        snow densities: 215 to 355 kg/m**3
        Korrelationskoeffizient of the fit: r2 = 0.80
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 1.89E-6 * self.rho**2.94 * 1E6  # Base formula without scaling
        result = self.apply_scaling(1.89E-6, result)
        return self.scale_output(result)

    def e_sigrist_2006_exponential(self):
        ''' 
        Sigrist 2006 (https://www.research-collection.ethz.ch/entities/publication/1c564911-fb9f-4b1a-b3b3-b447e4df33cd) page 76, in the text after equation 4.8
        Parametrization of the Young's Moduls on denstiy based on small cylindrical samples with a diameter of 48 mm and a height of 30 mm were loaded and unloaded with a frequency of 100 Hz. The force response F due to the predefined displacement resulted in a strain rate of e = 2 7 10~2s-1 results
        snow densities: 215 to 355 kg/m**3
        Korrelationskoeffizient of the fit: r2 = 0.78
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 2.71 * np.exp(0.0085 * self.rho) * 1E6  # Base formula without scaling
        result = self.apply_scaling(0.1873, result)
        return self.scale_output(result)   
    
        
#%% getting density from manual profile

def get_rho_from_hhi_geldsetzer_2001(hhi, gt):

    ''' 
    Estimation of snow density based on Hand hardness index (hhi) and and Grain type (gt) according to:
    Geldsetzer, T. and Jamieson, J.B., 2001. Estimating dry snow density from grain form and hand hardness, Proceedings International Snow Science Workshop, Big Sky, Montana, U.S.A., 1-6 October 2000. Montana State University, Bozeman MT, USA, pp. 121-127.
    https://arc.lib.montana.edu/snow-science/item.php?id=717
    
    Args:
        hand hardness (float):  value of Handhardness index (1,2,3,4,5)
        grain type (string): Grain typ from manual profile following Fierz et al (The International Classification for Seasonal Snow on the Ground)
                            ( 'PP', 'PPgp', 'DF', 'RGmx', 'FC', 'FCmx', 'DH', 'MFcr', 'MF', 'IF', 'SH')
        
    Returns:
        float: density of the snow layer in kg/m**3
    '''

    if gt == 'PP':
        rho, unc_rho = 45 + 36*hhi, 27
    elif gt == 'PPgp':
        rho, unc_rho = 83 + 37*hhi, 42       
    elif gt == 'DF':
        rho, unc_rho = 65 + 36*hhi,30
    elif gt == 'RG':
        rho, unc_rho = 154 + 1.51*hhi**3.15, 46       
    elif gt == 'RGmx':
        rho, unc_rho = 91 + 42*hhi     ,32
    elif gt == 'FC':
        rho, unc_rho = 112 + 46*hhi   ,43
    elif gt == 'FCmx':
        rho, unc_rho = 56 + 64*hhi    ,43
    elif gt == 'DH':
        rho, unc_rho = 185 + 25*hhi  ,41
    
    elif gt == 'MFcr': ## Bastian Bergfeld added this guess
        rho, unc_rho = 2*(185 + 25*hhi)  ,2*41 
    elif gt == 'MF': ## Bastian Bergfeldi added this guess
        rho, unc_rho = 2*(185 + 25*hhi)  ,2*41         
    elif gt == 'IF': ## Bastian Bergfeld added this guess
        rho, unc_rho = 870  ,50   
    elif gt == 'SH': ## Bastian Bergfeld added this guess
        rho, unc_rho = np.nan  ,np.nan 
        
        
    else:  raise ValueError('grain type not valid: '+ gt) 
    return(ufloat(rho, unc_rho))
    



