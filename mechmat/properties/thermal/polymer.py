from math import inf

from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg


class ThermalPolymer(Chainable):
    def __init__(self, **kwargs):
        super(ThermalPolymer, self).__init__(**kwargs)

        self.set_guard('temperature_glass_transition', ureg.degC, [-273.15, inf])

    temperature_glass_transition = Guarded()
