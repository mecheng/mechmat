# -*- coding: utf-8 -*-
from yaml import dump, load

from .linked import MetaLinked
from .subject import Subject

"""Main module."""

__all__ = ['Material']


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

    def __repr__(self):
        state = {}
        for prop in self._state:
            state[prop] = getattr(self, prop)
        return '{} with state {}>'.format(str(type(self))[:-2], state)

    def dump(self):
        return dump(self)

    def load(self, data):
        self = load(data)
