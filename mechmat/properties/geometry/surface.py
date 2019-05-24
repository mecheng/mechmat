from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg


class Surface(Chainable):
    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)

        self.set_guard('cross_section', ureg.m ** 2)

    cross_section = Guarded()
