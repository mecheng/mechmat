from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded
from mechmat.principal import core
from mechcite import cite
from math import inf


class Viscosity(Chainable):
    def __init__(self, **kwargs):
        super(Viscosity, self).__init__(**kwargs)

        self.set_guard('viscosity_dynamic', ureg.Pa * ureg.s)
        self.link_attr('viscosity_dynamic', core.mul, viscosity_kinematic='viscosity_kinematic', density='density')

        self.set_guard('viscosity_kinematic', ureg.m ** 2 / ureg.s)
        self.link_attr('viscosity_kinematic', core.div, viscosity_dynamic='viscosity_dynamic', density='density')

    viscosity_dynamic = Guarded()

    viscosity_kinematic = Guarded()
