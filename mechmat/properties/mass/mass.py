from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg
from mechmat.principal import core, density


class Mass(Chainable):
    def __init__(self, **kwargs):
        super(Mass, self).__init__(**kwargs)

        self.set_guard('mass', ureg.kg)
        self.link_attr('mass', core.mul, density='density', volume='volume')

        self.set_guard('density', ureg.kg / ureg.m ** 3)
        self.link_attr('density', core.reciprocal, value='specific_volume')
        self.link_attr('density', density.from_specific_weight, specific_weight='specific_weight')

        self.set_guard('specific_volume', ureg.m ** 3 / ureg.kg)
        self.link_attr('specific_volume', core.reciprocal, value='density')

        self.set_guard('specific_weight', ureg.N / ureg.m ** 3)


    mass = Guarded()

    density = Guarded()

    specific_volume = Guarded()

    specific_weight = Guarded()
