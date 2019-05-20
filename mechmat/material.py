from math import inf

from mechmat.linked import Linked, Guard
from mechmat.principal import specific_weight, density, specific_volume
from . import ureg


class Material(Linked):
    def __init__(self, **kwargs):
        super(Material, self).__init__(**kwargs)

        self.set_guard('density', ureg.kg / ureg.m ** 3, [0., inf])
        self.link_attr('density', density.from_specific_volume, specific_volume='specific_volume')
        self.link_attr('density', density.from_specific_weight, specific_weight='specific_weight')

        self.set_guard('specific_volume', ureg.m ** 3 / ureg.kg, [0., inf])
        self.link_attr('specific_volume', specific_volume.from_density, density='density')

        self.set_guard('specific_weight', ureg.N / ureg.m ** 3, [0., inf])
        self.link_attr('specific_weight', specific_weight.from_density, density='density')

        self.set_guard('specific_heat', ureg.J / (ureg.kg / ureg.K), [0., inf])

        self.set_guard('pressure', ureg.Pa, [0., inf])

        self.set_guard('temperature', ureg.degC, [-273.15, inf])

        self.set_guard('enthalpie', ureg.J, [0., inf])

        self.set_guard('molar_weight', ureg.kg / ureg.mol, [0., inf])

        self.set_guard('mass', ureg.kg, [0., inf])

        self.set_guard('mass_flow', ureg.kg / ureg.s)

        self.set_guard('volume', ureg.m ** 3, [0., inf])

        self.set_guard('volume_flow')

        self.set_guard('dt', ureg.s)

        self._logistic_properties += ['name', 'short_name', 'CAS', 'category']

    _version = 1
    """int: version of the material class. Bump this value up for big changes in the class which aren't compatible with 
        earlier release. """

    category = None
    r""":class:`~Category` The Material category"""

    name = None
    r"""str: The common name of the material"""

    CAS = None
    r"""str: Chemical Abstracts Service number"""

    @property
    def short_name(self):
        r"""
        str: Short name for the material. When it is not user specified, the :attr:`~name` is used. When this consists
        of multiple words, the short name is build from all first letters. When the name consist of a single word, the
        first two letters are used """
        if hasattr(self, '_short_name'):
            return self._short_name
        else:
            if self.name is None:
                return None
            words = self.name.split(' ')
            if len(words) > 1:
                return ''.join([w[0] for w in words])
            return self.name[:2]

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    def __repr__(self):
        state = {}
        for prop in self._logistic_properties:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        for prop in self._state:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        return '{} with state {}>'.format(str(type(self))[:-2], state)

    density = Guard()

    specific_volume = Guard()

    specific_weight = Guard()

    specific_heat = Guard()

    pressure = Guard()

    temperature = Guard()

    enthalpie = Guard()

    molar_weight = Guard()

    mass = Guard()

    mass_flow = Guard()

    volume = Guard()

    volume_flow = Guard()

    dt = Guard()
