# -*- coding: utf-8 -*-
from copy import deepcopy
from enum import Enum
from yaml import dump, load
from pytablewriter import MarkdownTableWriter, HtmlTableWriter, LatexTableWriter

from .linked import MetaLinked, Linked
from .subject import Subject

"""Main module."""

__all__ = ['Material']


class Category(Enum):
    """ Categories of different materials """

    UNDEFINED = 0
    METAL = 1
    PLASTIC = 2
    FLUID = 3
    GAS = 4
    BINGHAM = 5
    PSEUDOPLASTIC = 6
    GRANULAR = 7
    POWDER = 8


class Material(metaclass=MetaLinked):
    r""""
    All materials inherit from this class. This class describes the basic properties, which all mater have, such as a
    *density*, *specific weight*, and *temperature*.

    """

    def __init__(self, **kwargs):
        for key in self._linked.keys():
            if not hasattr(self, '_Subject__{}'.format(key)):
                setattr(self, '_Subject__{}'.format(key), Subject(key))
        for key in self._linked.keys():
            if hasattr(self._linked[key], '_depended_on'):
                for dep in self._linked[key]._depended_on:
                    getattr(self, '_Subject__{}'.format(dep)).register(getattr(self, '_Subject__{}'.format(key)))
        for key, value in kwargs.items():
            if key in self._state or key in self._logistic_properties:
                setattr(self, key, value)

    _state = list()
    _logistic_properties = ['name', 'short_name', 'CAS', 'category']
    _linked = dict()

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

    def _tbl_writer(self, writer):
        writer.headers = ['Material Attribute', 'Value']
        tbl = []
        if isinstance(writer, MarkdownTableWriter) or isinstance(writer, LatexTableWriter):
            value_str = '$ {:L} $'
        else:
            value_str = '{}'
        for prop in self._logistic_properties:
            if getattr(self, prop) is not None:
                tbl.append([prop.replace('_', ' '), str(getattr(self, prop))])
        for prop in self._state:
            if getattr(self, prop) is not None:
                tbl.append([prop.replace('_', ' '), value_str.format(getattr(self, prop))])
        writer.value_matrix = tbl
        writer.margin = 1
        return writer

    def _repr_markdown_(self):
        writer = self._tbl_writer(MarkdownTableWriter())
        return writer.write_table()

    def _repr_html_(self):
        writer = self._tbl_writer(HtmlTableWriter())
        return writer.write_table()

    def _repr_latex_(self):
        writer = self._tbl_writer(LatexTableWriter())
        return writer.write_table()

    def __call__(self, **kwargs):
        state = deepcopy(self)
        for key, value in kwargs.items():
            if key in state._state or key in state._logistic_properties:
                setattr(state, key, value)
        return state

    def dump(self):
        r""""
        Returns a YAML dump of the material
        """
        return dump(self)

    def load(self, data):
        r""""
        Restores a YAML dump on the material
        """
        # Todo: use _version
        self = load(data)

    density = Linked('kg/m**3')
    r""":class:`.Linked` Density :math:`\rho` in :math:`[M^{1} L^{-3}]`"""

    specific_weight = Linked('N/m**3')
    r""":class:`.Linked` Specific weight :math:`\gamma` in :math:`[M^{1} L^{-2} t^{-2}]`"""

    specific_volume = Linked('m**3/kg')
    r""":class:`.Linked` Specific volume :math:`v` in :math:`[L^{3} M^{-1}]`"""

    temperature = Linked('degC')
    r""":class:`.Linked` Temperature :math:`T` in :math:`[T]`"""

    specific_heat_at_const_pressure = Linked('J/(kg*K)')
    r""":class:`.Linked` Specific heat at constant pressure :math:`c_p` in :math:`[L^{2} T^{-1} t^{-2}]`"""

    thermal_conductivity = Linked('W/(m*K)')
    r""":class:`.Linked` Thermal conductivity :math:`k` in :math:`[L^{1} M^{1} T^{-1} t^{-3}]`"""

    thermal_diffusivity = Linked('m**2/s')
    r"""":class:`.Linked` Thermal diffusivity :math:`\alpha` in :math:`[L^{2} t^{-1}]`"""
