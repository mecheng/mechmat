from mechmat import ureg
from mechmat.principal import core
from mechmat.properties.flow.mass_flow import MassFlow
from mechmat.properties.flow.volume_flow import VolumeFlow


class Flow(MassFlow, VolumeFlow):
    def __init__(self, **kwargs):
        super(Flow, self).__init__(**kwargs)

        self.link_attr('massflow', core.mul, density='density', volumeflow='volumeflow')
        self.link_attr('volumeflow', core.div, massflow='massflow', density='density')


