# -*- coding: utf-8 -*-
from copy import deepcopy
from enum import Enum
from yaml import dump, load

from .linked import MetaLinked
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

    category = Category.UNDEFINED
    r""":class:`~Category` The Material category"""

    name = ''
    r"""str: The common name of the material"""

    CAS = ''
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
            words = self.name.split(' ')
            if len(words) > 1:
                return ''.join([w[0] for w in words])
            return self.name[:2]

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    def __repr__(self):
        state = {}
        for prop in self._state:
            state[prop] = getattr(self, prop)
        return '{} with state {}>'.format(str(type(self))[:-2], state)

    def __call__(self, **kwargs):
        state = deepcopy(self)
        for key, value in kwargs.items():
            if key in state._state:
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
