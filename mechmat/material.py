from mechmat.properties.geometry import Geometry
from mechmat.properties.mass import Mass
from mechmat.properties.thermal import Thermal
from mechmat.properties.pressure import Pressure
from mechmat.properties.viscosity import Viscosity
from mechmat.properties.shearing import Shearing
from mechmat.properties.flow import Flow
from mechmat.core.chainable import Chainable
import dill as _dill

__all__ = ['material_factory']


def material_factory(*args, flow=False, **kwargs):
    r"""
    Material instance facotry

    Args:
        *args: Chainable sub-propperties
        flow: is the material a continium flowing :math:`\frac{\text{d}m}{}`
        **kwargs:

    Returns:

    """
    Material = material_type_factory(*args, flow=flow)
    return Material()(**kwargs)


def material_type_factory(*args, flow=False):
    if flow:
        class FlowMaterial(Material, Thermal, Pressure, Flow, Shearing, Viscosity, *args):
            def __init__(self, **kwargs):
                super(FlowMaterial, self).__init__(**kwargs)

        FlowMaterial.dtypes = args
        FlowMaterial.flow = flow

        return FlowMaterial
    else:
        class StaticMaterial(Material, Thermal, Pressure, Geometry, Mass, *args):
            def __init__(self, **kwargs):
                super(StaticMaterial, self).__init__(**kwargs)

        StaticMaterial.dtypes = args
        StaticMaterial.flow = flow
        return StaticMaterial


class _InitializedMaterial(object):
    def __call__(self, *args):
        obj = _InitializedMaterial()
        obj.__class__ = material_type_factory(*args[0], flow=args[1])
        return obj


class Material(Chainable):
    def __init__(self, **kwargs):
        super(Material, self).__init__(**kwargs)
        self._logistic_properties += ['name', 'short_name', 'CAS']

    def __reduce__(self):
        return (_InitializedMaterial(), (self.dtypes, self.flow), self.__dict__)

    dtypes = ()

    flow = False

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

    @staticmethod
    def dump(instance, filename):
        with open(filename, 'wb') as f:
            _dill.dump(instance, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            mat = _dill.load(f)
        return mat
