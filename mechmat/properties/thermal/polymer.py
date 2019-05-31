from math import inf

from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg
from mechmat.principal import thermal_polymer


class ThermalPolymer(Chainable):
    def __init__(self, **kwargs):
        super(ThermalPolymer, self).__init__(**kwargs)

        self.set_guard('temperature_glass', ureg.degC, [-273.15, inf])
        self.link_attr('temperature_glass', thermal_polymer.temperature_glass, temperature_melt='temperature_melt')

        self.link_attr('temperature_melt', thermal_polymer.temperature_melt, temperature_glass='temperature_glass')

    temperature_glass = Guarded()
