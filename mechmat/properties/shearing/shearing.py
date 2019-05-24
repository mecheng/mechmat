from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded


class Shearing(Chainable):
    def __init__(self, **kwargs):
        super(Shearing, self).__init__(**kwargs)

        self.set_guard('shear_rate', ureg.s ** -1)

    shear_rate = Guarded()
