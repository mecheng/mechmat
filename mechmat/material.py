from mechmat.properties.geometry import Geometry
from mechmat.properties.mass import Mass
from mechmat.properties.thermal import Thermal
from mechmat.properties.pressure import Pressure
from mechmat.properties.flow import Flow
from mechmat.core.chainable import Chainable

__all__ = ['material_factory']


class Base(Chainable):
    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)

        self._logistic_properties += ['name', 'short_name', 'CAS', 'category']

    _version = 1
    """int: version of the material class. Bump this value up for big changes in the class which aren't compatible with 
        earlier release. """

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


def material_factory(flow=False, *args, **kwargs):
    class Material(Base, Thermal, Pressure, *args):
        def __init__(self, **kwargs):
            super(Material, self).__init__(**kwargs)

    if flow:
        class FlowMaterial(Material, Flow):
            def __init__(self, **kwargs):
                super(FlowMaterial, self).__init__(**kwargs)

        return FlowMaterial(**kwargs)
    else:
        class StaticMaterial(Material, Geometry, Mass, args):
            def __init__(self, **kwargs):
                super(StaticMaterial, self).__init__(**kwargs)

        return StaticMaterial(**kwargs)
