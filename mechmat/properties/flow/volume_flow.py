from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded
from mechmat.principal import core
from mechmat.properties.geometry.geometry import Surface, Segment


class VolumeFlow(Surface, Segment):
    def __init__(self, **kwargs):
        super(VolumeFlow, self).__init__(**kwargs)

        self.set_guard('volumeflow', ureg.m ** 3 / ureg.s)
        self.link_attr('volumeflow', core.mul, segment='distance', surface='cross_section', dt=1. * ureg.s)

    volumeflow = Guarded()
