from math import inf

from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg
from mechmat.principal import thermal


class Thermal(Chainable):
    def __init__(self, **kwargs):
        super(Thermal, self).__init__(**kwargs)

        self.set_guard('temperature', ureg.degC, [-273.15, inf], 'Temperature of the material')
        self.set_guard('temperature_melt', ureg.degC, [-273.15, inf], 'Melting temperature of the material')
        self.set_guard('temperature_vapor', ureg.degC, [-273.15, inf])

        self.set_guard('specific_heat_capacity', ureg.J / (ureg.kg * ureg.K))
        self.link_attr('specific_heat_capacity', thermal.specific_heat_capacity, thermal_conductivity='thermal_conductivity', density='density',
                       thermal_diffusivity='thermal_diffusivity')

        self.set_guard('thermal_diffusivity', ureg.m ** 2 / ureg.s)
        self.link_attr('thermal_diffusivity', thermal.thermal_diffusivity, thermal_conductivity='thermal_conductivity', specific_heat_capacity='specific_heat_capacity',
                       density='density')

        self.set_guard('thermal_conductivity', ureg.W / (ureg.m * ureg.K))
        self.link_attr('thermal_conductivity', thermal.thermal_conductivity, thermal_diffusivity='thermal_diffusivity', specific_heat_capacity='specific_heat_capacity',
                       density='density')

        self.set_guard('thermal_expansion_coeff', ureg.um / (ureg.m * ureg.K))

    temperature = Guarded()
    r"""Temperature of a material """

    temperature_melt = Guarded()

    temperature_vapor = Guarded()

    specific_heat_capacity = Guarded()

    thermal_diffusivity = Guarded()

    thermal_conductivity = Guarded()

    thermal_expansion_coeff = Guarded()
