from numpy import e
from mechcite import cite
from mechmat import ureg


@cite('osswald_polymer_2006')
def arrhenius_shift(temperature, arrhenius_activation_energy, temperature_ref):
    return e ** (arrhenius_activation_energy / ureg.R * (1. / temperature - 1. / temperature_ref)).to('dimensionless').m

@cite('cross_rheology_1965')
def zero_shear_viscosity(arrhenius, zero_shear_viscosity_ref):
    return arrhenius * zero_shear_viscosity_ref

@cite('cross_rheology_1965')
def relaxation_time(relaxation_time_ref, arrhenius):
    return arrhenius * relaxation_time_ref

@cite('cross_rheology_1965')
def viscosity_dynamic(shear_rate, zero_shear_viscosity, relaxation_time, shear_thinning_const):
    return zero_shear_viscosity / (1. + relaxation_time * shear_rate) ** shear_thinning_const
