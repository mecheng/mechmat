from math import inf

from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg


class Thermal(Chainable):
    def __init__(self, **kwargs):
        super(Thermal, self).__init__(**kwargs)

        self.set_guard('temperature', ureg.degC, [-273.15, inf], 'Temperature of the material')
        self.set_guard('temperature_melt', ureg.degC, [-273.15, inf], 'Melting temperature of the material')
        self.set_guard('temperature_vapor', ureg.degC, [-273.15, inf])
        self.set_guard('specific_heat_capacity', ureg.J / (ureg.kg * ureg.K))

    temperature = Guarded()
    r"""Temperature of a material """

    temperature_melt = Guarded()

    temperature_vapor = Guarded()

    specific_heat_capacity = Guarded()
