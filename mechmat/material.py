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
    def __init__(self):
        for key in self._linked.keys():
            if not hasattr(self, '_Subject__{}'.format(key)):
                setattr(self, '_Subject__{}'.format(key), Subject(key))
        for key in self._linked.keys():
            if hasattr(self._linked[key], '_depended_on'):
                for dep in self._linked[key]._depended_on:
                    getattr(self, '_Subject__{}'.format(dep)).register(getattr(self, '_Subject__{}'.format(key)))

    _state = list()
    _linked = dict()

    category = Category.UNDEFINED

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
        return dump(self)

    def load(self, data):
        self = load(data)
