# snow_models

Welcome to **snow_models** – a Python package designed for the easy and consistent application of snow- and avalanche-related parameterizations and models. This package provides several models and functions to support research and development in snow mechanics and avalanche forecasting.

## Key Modules

- **`snow_models.mechanical_params`**  
  Parametrizations and conversion functions for mechanical properties of snow.

- **`snow_models.crack_propagation`**  
  Models to estimate crack propagation speeds in weak snow layers.

- **`snow_models.wave_propagation`**  
  Models to compute elastic wave speeds for different types of waves.

## Purpose

This package implements published parameterizations to facilitate further research applications. It is designed to help researchers and practitioners integrate and use these models for snow and avalanche studies in an easy-to-use Python environment.

## Installation

You can install **snow_models** directly from GitHub using `pip`
(make sure git is installed in your active environment (conda install git):

```bash
pip install git+https://github.com/bbergfeld/snow_models.git
```

## Examples

Example usage for Emodulus parametrizations:
```python
from snow_models.mechanical_params import get_E_Mod as emod
snow_density = 200 #kg/m**3
slab_elastic_modulus = emod(snow_density, output_unit="MPa")
print("Emodul based on Gerling et al.: " + str(slab_elastic_modulus.e_gerling_2017_AC()))  # provides the elastic modulus based on the parametrization by Gerling et al 2017
print("Emodul based on Sigrist et al.: " + str(slab_elastic_modulus.e_sigrist_2006()))  # provides the elastic modulus based on the parametrization by Sigrist et al 2006
# more parametrizations are available......


```
View the package to find more usefull functions for other mechanical paramters


Example usage for crack propagation models with uncertainty computation). However you can also provide normal float values:
```python
import snow_models.crack_propagation as cp_models

g = 9.81 #m/s^2
Emod_slab = 10000000 #Pa
slab_thickness = 0.5 #m
collapse_heigth = 0.003 #m
slab_density = 200 #kg/m^3

speed = cp_models.solitary_wave_speed(g, Emod_slab,slab_thickness,collapse_heigth,slab_density)
print(speed)

#%% Or try out to automatically compute uncertainty

from uncertainties import ufloat

# Define the variables with 5% uncertainty (using ufloat)
g = ufloat(9.81, 9.81 * 0.05)  # 9.81 m/s^2 with 5% uncertainty
Emod_slab = ufloat(10000000, 10000000 * 0.05)  # 10,000,000 Pa with 5% uncertainty
slab_thickness = ufloat(0.5, 0.5 * 0.05)  # 0.5 m with 5% uncertainty
collapse_heigth = ufloat(0.003, 0.003 * 0.05)  # 0.003 m with 5% uncertainty
slab_density = ufloat(200, 200 * 0.05)  # 200 kg/m^3 with 5% uncertainty

speed = cp_models.solitary_wave_speed(g, Emod_slab, slab_thickness, collapse_heigth,slab_density)
print(speed)
tdd = cp_models.solitary_wave_touchdown(g, Emod_slab, slab_thickness, collapse_heigth,slab_density)
print(tdd)
```


