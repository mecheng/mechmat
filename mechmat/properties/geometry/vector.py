from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg
from mechmat.principal import geometry


class Vector(Chainable):
    def __init__(self, **kwargs):
        super(Vector, self).__init__(**kwargs)

        self.set_guard('coordinate', ureg.m)

    coordinate = Guarded()


class Segment(Chainable):
    def __init__(self, **kwargs):
        super(Segment, self).__init__(**kwargs)

        self.set_guard('point_1', ureg.m)
        self.set_guard('point_2', ureg.m)
        self.set_guard('distance', ureg.m)
        self.link_attr('distance', geometry.distance, point_1='point_1', point_2='point_2')

    point_1 = Guarded()

    point_2 = Guarded()

    distance = Guarded()
