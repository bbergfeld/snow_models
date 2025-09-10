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
        Scapozza 2004 formula.
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 0.1873 * np.exp(0.0149 * self.rho) * 1E6  # Base formula without scaling
        result = self.apply_scaling(0.1873, result)
        return self.scale_output(result)

    def e_sigrist_2006(self):
        ''' 
        Sigrist 2006 formula.
        
        Returns:
            float: Elastic modulus in the desired unit (Pa, kPa, MPa, or GPa).
        '''
        result = 1.89E-6 * self.rho**2.94 * 1E6  # Base formula without scaling
        result = self.apply_scaling(1.89E-6, result)
        return self.scale_output(result)
        
        
        



