from math import inf, isnan
from copy import copy
import logging

from numpy import any

from pint import DimensionalityError

from . import ureg
from .errors import OutOfRangeError


class Linked:
    def __init__(self, unit='dimensionless', rng=[-inf, inf], linked_properties={}):
        self.key = ''
        self.subject_key = ''
        self.property = ''
        self.unit = ureg.parse_units(unit)
        self.rng = rng * self.unit
        self._linked_properties = linked_properties
        self._args = dict(
            zip(list(linked_properties.keys()), [set(args.values()) for args in linked_properties.values()]))
        self._depended_on = list(set([y for x in self._args.values() for y in x]))

    def __get__(self, instance, owner):
        if hasattr(instance, self.key):
            value = getattr(instance, self.key)
            return value
        else:
            return None

    def __set__(self, instance, value):
        upd = set()
        if isinstance(value, set):
            upd = value
            value = getattr(instance, self.property)
            sorted_fun = Linked.get_sorted_functions(upd, self._args)
            for func in sorted_fun:
                kwargs = copy(self._linked_properties[func])
                for arg in kwargs.keys():
                    kwargs[arg] = getattr(instance, kwargs[arg])
                if any([x is None for x in kwargs.values()]):
                    continue
                value = func(**kwargs)
                logging.debug('Property {} calculated'.format(self.property))
                break

        if type(getattr(instance, self.property)) != type(value) or (
            getattr(instance, self.property) != value and value is not None):
            try:
                if isinstance(value, ureg.Quantity):
                    value = value.to(self.unit)
            except DimensionalityError as e:
                raise DimensionalityError(e.units1, e.units2, e.dim1, e.dim2,
                                          'Wrong dimensions when setting {} with value {}'.format(
                                              self.property, value))
            if not Linked.in_range(value, self.rng):
                raise OutOfRangeError(value, self.rng, self.property)
            setattr(instance, self.key, value)
            if self.property not in upd:
                upd.add(self.property)
                getattr(instance, self.subject_key).send(instance, upd)

    @staticmethod
    def in_range(value, rng):
        if isinstance(value, ureg.Quantity):
            return any(((rng[0].m <= value.m) & (rng[1].m >= value.m))) or any(isnan(value.m))
        else:
            return any(((rng[0].m <= value) & (rng[1].m >= value))) or any(isnan(value))

    @staticmethod
    def argument_weight(visited, arg):
        return len(visited.intersection(arg)) / len(arg)

    @staticmethod
    def get_sorted_functions(visited, args):
        return [func[0] for func in sorted(args.items(), key=lambda value: Linked.argument_weight(visited, value[1]))]


class MetaLinked(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        if not hasattr(cls, '_linked'):
            setattr(cls, '_linked', dict())
        if not hasattr(cls, '_state'):
            setattr(cls, '_state', list())
        for key, attr in attr_dict.items():
            if isinstance(attr, Linked):
                attr.property = key
                type_name = type(attr).__name__
                attr.key = '_{}__{}'.format(type_name, key)
                attr.subject_key = '_Subject__{}'.format(key)
                if key[0] != '_' and key not in getattr(cls, '_state'):
                    getattr(cls, '_state').append(key)
                getattr(cls, '_linked')[key] = attr
