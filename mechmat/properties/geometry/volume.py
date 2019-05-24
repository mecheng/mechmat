from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg


class Volume(Chainable):
    def __init__(self, **kwargs):
        super(Volume, self).__init__(**kwargs)
        self.set_guard('volume', ureg.m ** 3)

    volume = Guarded()
