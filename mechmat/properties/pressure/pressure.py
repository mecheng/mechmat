from math import inf

from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded


class Pressure(Chainable):
    r"""
    Pressure
    """
    def __init__(self, **kwargs):
        super(Pressure, self).__init__(**kwargs)

        self.set_guard('pressure', ureg.Pa, [0., inf])

    pressure = Guarded()
