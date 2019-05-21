from numpy import e

from mechmat import ureg


def arrhenius(temperature, arrhenius_activation_energy, temperature_ref):
    return e ** (arrhenius_activation_energy / ureg.R * (1. / temperature - 1. / temperature_ref)).to('dimensionless').m


def zero_shear_viscosity(arrhenius, zero_shear_viscosity_ref):
    return arrhenius * zero_shear_viscosity_ref


def relaxation_time(relaxation_time_ref, arrhenius):
    return arrhenius * relaxation_time_ref


def viscosity_dynamic(shear_rate, zero_shear_viscosity, relaxation_time, shear_thinning_const):
    return zero_shear_viscosity / (1. + relaxation_time * shear_rate) ** shear_thinning_const
