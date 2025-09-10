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
    Estimation of snow density based on Hand hardness index (hhi) and Grain type (gt) according to:
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



def get_rho_from_gt_hhi_kim_2014(hhi, gt):
    ''' 
    Estimation of snow density based on Hand hardness index (hhi) and Grain type (gt) and Grain size according to:
    Kim, D. and Jamieson, J.B., 2014. Estimating the Density of Dry Snow Layers From Hardness, and Hardness From Density, International Snow Science Workshop 2014 Proceedings, Banff, Canada, 2014 pp.540-547.
    https://arc.lib.montana.edu/snow-science/item.php?id=2103
    
    Args:
        hhi (float): hand hardness index (e.g., F=1.0, 4F=2.0, 1F=3.0, P=4.0, K=5.0)
        gt (string): Grain type from Fierz classification 
                     ('PP', 'PPgp', 'DF', 'RG', 'RGxf', 'FC', 'FCxr', 'DH', 'MFcr')
        
    Returns:
        ufloat: density of the snow layer in kg/m³ with standard error as uncertainty
    '''
    if gt == 'PP':
        rho, unc, R2 = 41.3 + 40.3*hhi, 27, 0.35
    elif gt == 'PPgp':
        rho, unc, R2 = 61.8 + 46.4*hhi, 43, 0.55
    elif gt == 'DF':
        rho, unc, R2 = 62.5 + 37.4*hhi, 31, 0.50
    elif gt == 'RGxf':
        rho, unc, R2 = 85.0 + 46.3*hhi, 40, 0.58
    elif gt == 'FC':
        rho, unc, R2 = 103.0 + 50.6*hhi, 47, 0.53
    elif gt == 'FCxr':
        rho, unc, R2 = 68.8 + 58.6*hhi, 46, 0.50
    elif gt == 'DH':
        rho, unc, R2 = 214.0 + 19.0*hhi, 48, 0.12
    elif gt == 'MFcr':
        rho, unc, R2 = 235.0 + 15.1*hhi, 58, 0.027
    elif gt == 'RG':
        rho, unc, R2 = 91.8 * np.exp(0.270*hhi), 0.2, 0.55
    else:
        raise ValueError("Grain type not valid: " + gt)
    
    return ufloat(rho, unc)


def get_hhi_from_rho_gs_kim_2014(rho, gs, gt):
    ''' 
    Estimation of Hand hardness index (hhi) from density (ρ) and grain size (gs, mm)
    according to Eq. (4) in Kim & Jamieson (2014):
    
        h = A*ρ + B*gs + C
    
Args:
        rho (float): density in kg/m³
        gs (float): grain size in mm
        gt (string): Grain type subset ('Facets', 'FCxr', 'RG')
    
    Returns:
        float: estimated hardness index (no uncertainty)
    '''
    
    if gt == 'Facets':
        hhi, unc, R2 = 0.0101*rho - 0.277*gs + 0.685, 1, 0.53
    elif gt == 'FCxr':
        hhi, unc, R2 = 0.00839*rho - 0.381*gs + 1.56, 1, 0.51
    elif gt == 'RG':
        hhi, unc, R2 = 0.00830*rho - 0.0985*gs + 1.48, 1, 0.56
    else:
        raise ValueError("Grain type not valid for Eq.(4): " + gt)
    
    return ufloat(hhi,unc)


def get_rho_from_hhi_gs_gt_kim_2014(hhi, gs, gt):
    ''' 
    Estimation of snow density (ρ) from Hand hardness index (hhi) and grain size (gs, mm)
    according to Eq. (5) in Kim & Jamieson (2014):
    
        ρ = A*h + B*gs + C
    
    Args:
        hhi (float): hand hardness index
        gs (float): grain size (mm)
        gt (string): Grain type subset 
                     ('Facet', 'FCxr', 'PP', 'PPgp', 'DF', 'MF')
    
    Returns:
        float: estimated density (kg/m³)
    '''
    
    if gt == 'Facet':
        rho, unc, R2 = 51.9*hhi + 19.7*gs + 82.8, 46, 0.53
    elif gt == 'FCxr':
        rho, unc, R2 = 60.4*hhi + 27.7*gs + 36.7, 45, 0.50
    elif gt == 'PP':
        rho, unc, R2 = 40.0*hhi - 7.33*gs + 52.8, 25, 0.39
    elif gt == 'PPgp':
        rho, unc, R2 = 38.8*hhi + 18.8*gs + 35.7, 33, 0.64
    elif gt == 'DF':
        rho, unc, R2 = 37.9*hhi - 8.87*gs + 71.4, 31, 0.52
    elif gt == 'MF':
        rho, unc, R2 = 34.9*hhi + 11.2*gs + 124.5, 63, 0.17
    else:
        raise ValueError("Grain type not valid for Eq.(5): " + gt)
    
    return ufloat(rho, unc)





