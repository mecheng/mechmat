import logging
from copy import deepcopy

from numpy import isnan, any
from pint import DimensionalityError
from pytablewriter import MarkdownTableWriter, HtmlTableWriter, LatexTableWriter

from mechmat import ureg
from .errors import OutOfRangeError
from mechcite import Bibliography


class Message(set):
    r"""
    Linked Message
    """

    def __repr__(self):
        return super(Message, self).__repr__()


class Guarded:
    r"""
    Descriptor guarding Linked attributes
    """

    def __init__(self):
        pass

    def __get__(self, instance, owner):
        return getattr(instance, self.guard_name)

    def __set__(self, instance, value):
        unit = getattr(instance, self.unit_name)
        if isinstance(value, ureg.Quantity) and unit is not None:
            try:
                value = value.to(unit)
            except DimensionalityError as e:
                raise DimensionalityError(e.units1, e.units2, e.dim1, e.dim2,
                                          'Wrong dimensions when setting {} with value {}'.format(
                                              self.name, value))
        rng = getattr(instance, self.rng_name)
        if rng is not None:
            if not Guarded.in_range(value, rng):
                raise OutOfRangeError(value, rng, self.name)
        Guarded.cite_value(value)
        setattr(instance, self.guard_name, value)

    def __del__(self):
        pass

    def __set_name__(self, owner, name):
        self.name = name
        self.guard_name = '_Guard_{}'.format(name)
        self.rng_name = '_Guard_{}_rng'.format(name)
        self.unit_name = '_Guard_{}_unit'.format(name)
        setattr(owner, self.guard_name, None)
        setattr(owner, self.rng_name, None)
        setattr(owner, self.unit_name, None)

    _bib = Bibliography()

    @staticmethod
    def in_range(value, rng):
        r"""
        is value in specified range

        Args:
            value: value to be tested
            rng: tuple or list to be tested against

        Returns:
            true when in range otherwise false
        """
        if isinstance(value, ureg.Quantity):
            return any(((rng[0].m <= value.m) & (rng[1].m >= value.m))) or any(isnan(value.m))
        else:
            return any(((rng[0].m <= value) & (rng[1].m >= value))) or any(isnan(value))

    @staticmethod
    def cite_value(value):
        if hasattr(value, '_cite'):
            Guarded._bib.cite(getattr(value, '_cite'))


class Chainable:
    r""""
    A linked attribute class
    """

    def __init__(self, **kwargs):
        self._depended_on = {}
        self._linked_attributes = {}
        self._linked_attributes_args = {}
        self._state = []
        self._logistic_properties = []

    def __setattr__(self, key, value):
        upd = Message()
        if isinstance(value, Message):  # Chain Message received
            if (self, key) in value:
                return
            upd = value
            value = None
            sorted_transforms = self._get_sorted_functions(upd, self._linked_attributes_args[key])
            for transform in sorted_transforms:
                kwargs = {}
                for arg, attr in self._linked_attributes[key][transform].items():
                    logging.debug(attr)
                    kwargs[arg] = getattr(attr[0], attr[1])
                    if kwargs[arg] is None:
                        break
                if kwargs[arg] is None:
                    continue
                value = transform(**kwargs)
                if value is not None:
                    continue
            if value is not None:
                super(Chainable, self).__setattr__(key, value)
                logging.debug('Transform set for {} -> {} with {}'.format(id(self), key, value))
                self._send(key, upd)
        else:
            super(Chainable, self).__setattr__(key, value)
            logging.debug('User set for {} -> {} with {}'.format(id(self), key, value))
            self._send(key, upd)

    def __delattr__(self, item):
        super(Chainable, self).__delattr__(item)

    def __repr__(self):
        state = {}
        for prop in self._logistic_properties:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        for prop in self._state:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        return '<{} with state {}>'.format(str(self.__class__).split('.')[-1][:-2], state)

    def __call__(self, **kwargs):
        state = deepcopy(self)
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        return state

    def __dir__(self):
        _dir = list(super(Chainable, self).__dir__())
        for hide in self._hidden_dir:
            _dir.remove(hide)
        return [d for d in [d for d in _dir if '_Guard_' not in d] if '_const_' not in d]

    _hidden_dir = ['_linked_attributes', '_linked_attributes_args', '_depended_on', '_logistic_properties', '_state', '_version', '_hidden_dir']

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
                try:
                    tbl.append([prop.replace('_', ' '), value_str.format(getattr(self, prop))])
                except:
                    tbl.append([prop.replace('_', ' '), '{}'.format(getattr(self, prop))])
        writer.value_matrix = tbl
        writer.margin = 1
        return writer

    def _repr_markdown_(self):
        writer = self._tbl_writer(MarkdownTableWriter())
        return writer.dumps()

    def _repr_html_(self):
        writer = self._tbl_writer(HtmlTableWriter())
        return writer.dumps()

    def _repr_latex_(self):
        writer = self._tbl_writer(LatexTableWriter())
        return writer.dumps()

    def _send(self, key, upd):
        if (self, key) in self._depended_on:
            upd.add((self, key))
            for cls, attr in self._depended_on[(self, key)]:
                logging.debug(cls)
                setattr(cls, attr, upd)

    def _argument_weight(self, visited, arg):
        return len(visited.intersection(arg)) / len(arg)

    def _get_sorted_functions(self, visited, args):
        return [transform[0] for transform in sorted(args.items(), key=lambda value: self._argument_weight(visited,
                                                                                                           value[1]))]

    def set_guard(self, attr, unit=None, rng=None, doc=None):
        r"""
        Set the guard descriptor unit and range, this is usually set in the __init__() function

        Args:
            attr (str): The guard attribute to be set
            unit (ureg.Unit): The unit in which guarded inputs are to be converted
            rng (tuple, list, np.array): The range [low, high] against which to test
            doc (str): dosctring
        """
        if attr not in self._state and attr[0] != '_':
            self._state.append(attr)
        self._state.sort()
        setattr(self, '_Guard_{}_unit'.format(attr), unit)
        setattr(self, '_Guard_{}_doc'.format(attr), '{}. {} should be given in {}'.format(doc, attr, unit))
        if rng is not None and not isinstance(rng, ureg.Quantity) and unit is not None:
            setattr(self, '_Guard_{}_rng'.format(attr), rng * unit)
        else:
            setattr(self, '_Guard_{}_rng'.format(attr), rng)

    def link_attr(self, attr, transform, **kwargs):
        r"""
        Link a Linked attribute against another Linked attribute.

        Args:
            attr (str): Attribute name
            transform: The function which provides the transform.
            **kwargs: the transform function keywords where the value is either a str (if the attribute can be obtained
             from the own instance) or a tuple containing the other instance and attribute name.
        """
        if attr not in self._linked_attributes:
            self._linked_attributes[attr] = {}
            self._linked_attributes_args[attr] = {}
        self._linked_attributes[attr][transform] = {}
        self._linked_attributes_args[attr][transform] = set()

        for arg, depend in kwargs.items():

            cls = self
            dep = depend
            if hasattr(depend, '__iter__') and isinstance(depend[0], Chainable):
                cls = depend[0]
                dep = depend[1]
            if not isinstance(dep, str) or not hasattr(cls, dep):
                dep_name = '_const_{}'.format(hash((cls, dep)))
                setattr(cls, dep_name, dep)
                dep = dep_name
            if hasattr(cls, '_depended_on'):
                if (cls, dep) not in getattr(cls, '_depended_on'):
                    getattr(cls, '_depended_on')[(cls, dep)] = set()
                getattr(cls, '_depended_on')[(cls, dep)].add((self, attr))
            self._linked_attributes[attr][transform][arg] = (cls, dep)
            self._linked_attributes_args[attr][transform].add((cls, dep))

    def unlink_attr(self, attr, transform):
        # Todo implement
        for key, value in self._linked_attributes[attr][transform].items():
            pass

        del self._linked_attributes[attr][transform]
        del self._linked_attributes_args[attr][transform]

    def linked_transforms(self, attr):
        return dict(zip(self._linked_attributes[attr].keys(),
                        [list(x.keys()) for x in list(self._linked_attributes['density'].values())]))
