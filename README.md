# snow_models

Welcome to **snow_models**, a python package for easy and consistent use of snow and avalanche related parametrizations (mostly on density).
it holds 3 scripts with various published models: 
snow_models.mechanical_params --> parametrizations and conversion functionality for mechanical parameters
snow_models.crack_propagation --> models to compute for crack propagation speeds in weak snow layers
snow_models.wave_propagation --> models to compute elastic wave speeds for different kind of waves


This package implements published parametrizations for further research applications. 

Example usage for Emodulus parametrizations:
```python
from snow_models.mechanical_params import get_E_Mod as emod
snow_density = 200 #kg/m**3
slab_elastic_modulus ) = emod(snow_denstity, output_unit="MPa")
print("Emodul based on Gerling et al.: " + str(slab_elastic_modulus.e_gerling_2017_AC)))  # provides the elastic modulus based on the parametrization by Gerling et al 2017
print("Emodul based on Sigrist et al.: " + str(slab_elastic_modulus.e_sigrist_2006)))  # provides the elastic modulus based on the parametrization by Sigrist et al 2006
# more parametrizations are available......
```
View the package to find more usefull functions for other mechanical paramters


Example usage for crack propagation models:
```python
import snow_models.crack_propagation as cp_models
g = 9.81 #m/s^2
Emod_slab = 10000000 #Pa
slab_thickness = 0.5 #m
collapse_heigth = 0.003 #m
slab_density = 200 #kg/m^3

cp_models.solitary_wave_speed(g, Emod_slab,slab_thickness,collapse_heigth,slab_density)

# more parametrizations are available......
```
View the package to find more usefull functions for other mechanical paramters

