from mechmat.core.chainable import Chainable, Guarded
from mechmat import ureg
from mechmat.properties.geometry.volume import Volume
from mechmat.properties.geometry.surface import Surface
from mechmat.properties.geometry.vector import Vector, Segment
from mechmat.principal import core, geometry


class Geometry(Vector, Segment, Surface, Volume):
    def __init__(self, **kwargs):
        super(Geometry, self).__init__(**kwargs)

        self.link_attr('volume', core.mul, segment='distance', surface='cross_section')
        self.link_attr('coordinate', geometry.halfway, point_1='point_1', point_2='point_2')
